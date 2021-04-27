import sys
import re
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

import tensorswitch as ts
import tensorflow as tf
from tensorflow.tools.graph_transforms import TransformGraph

import numpy as np
import datetime
import yaml
import argparse

from xlearn import train_util

vocabulary_size = 40000*10000
embedding_size = 8
max_emb_ids_size_1 = 50
max_emb_ids_size_2 = 50
batch_size = 64
prefetch = 128
learning_rate = 0.0001
learning_rate_mf = 0.05

avg_decay_rate = 0.9999
ada_decay_rate = 0.9999
ada_epsilon = 1e-8
mom_decay_rate = 0.99

rv_feas_len = 78
slotsS_str = "1,2,3,4,5,6,7"
slotsM_str = "8,9"
slotsL_str = "10,11,12"
show_index_len = 22

slotsS = slotsS_str.split(",")
slotsM = slotsM_str.split(",")
slotsL = slotsL_str.split(",")

slots_sizeS = len(slotsS)
slots_sizeM = len(slotsM)
slots_sizeL = len(slotsL)

hidden_layer_sizes = [512]
dense_input_size = (slots_sizeS + slots_sizeM + slots_sizeL) * embedding_size + rv_feas_len
init_layer_sizes = [dense_input_size] + hidden_layer_sizes  # [174,512]
mlp_activation_names = ["none","relu"]

multi_tar_layer_sizes = [200,1]
multi_tar_layer_sizes = [init_layer_sizes[-1]] + multi_tar_layer_sizes  # [512,200,1]
multi_tar_activation_names = ["none","relu","none"]


def build_model(batch, sparse_table):
    pb_saver = tf.train.Saver()
    ts.get_default_learner().local_storage['pb_saver'] = pb_saver
    rv_feas,single_slots,multi_slots,long_slots,click,cr,show_index,meta_info = batch

    rv_feas = tf.reshape(rv_feas, [-1,rv_feas_len])
    show_index = tf.reshape(show_index, [-1,show_index_len])
    labels = [click,cr]

    single_count_ratio = np.ones(single_slots.shape.as_list()).ravel() * 200
    multi_count_ratio = np.ones(multi_slots.shape.as_list()).ravel() * 200
    long_count_ratio = np.ones(long_slots.shape.as_list()).ravel() * 200
    count_ratio = single_count_ratio.tolist() + multi_count_ratio.tolist() + long_count_ratio.tolist()

    s_emb_0, m_emb_0, l_emb_0 = sparse_table.embedding_pull(single_slots, multi_slots, long_slots, counting_ratio=count_ratio)
    # s_emb
    s_emb = tf.reshape(s_emb_0, [-1,slots_sizeS * embedding_size])
    # m_emb
    m_emb_1 = tf.reduce_sum(m_emb_0, 2)
    m_emb = tf.reshape(m_emb_1, [-1,slots_sizeM * embedding_size])
    logging.info("m shape: %s, %s", m_emb.shape, slots_sizeM * embedding_size)
    # l_emb
    l_emb_1 = tf.reduce_sum(l_emb_0, 2)
    l_emb = tf.reshape(l_emb_1, [-1, slots_sizeL * embedding_size])
    logging.info("l shape: %s, %s", l_emb.shape, slots_sizeL * embedding_size)

    with tf.compat.v1.variable_scope('dense'):
        with tf.variable_scope('MLP'):
            mlp_input = tf.concat([rv_feas, s_emb, m_emb, l_emb], axis=-1)
            mlp_input_norm = tf.layers.batch_normalization(
                inputs = mlp_input,
                momentum = mom_decay_rate,
                name = "norm_mlp_input_norm"
                )

            params, mlp_out, z_vars, act_vars = train_util.multilayer_perceptron(
                [mlp_input_norm],
                init_layer_sizes,
                mlp_activation_names,
                name_pre="multi_share1_"
                )
            logging.info("mlp_out[-1].shape: %s", mlp_out[-1].shape) #(64*174) * (174*512) = (64,512)

            params_list_0, mlp_out_list_0, z_vars_list_0, act_vars_0 = train_util.multilayer_perceptron(
                mlp_out,
                [512,200],
                ['none','relu'],
                name_pre="multi_share2_"
                )
            logging.info("mlp_out_list_0[-1].shape: %s", mlp_out_list_0[-1].shape) #(64,512) * (512,200) = (64,200)

        with tf.variable_scope('Multi_Tar'):
            n_heads = len(labels)
            input_list = mlp_out_list_0 * n_heads # (n_heads,64,200) ?

            params_list_1, mlp_out_list_1, z_vars_list_1, act_vars_1 = train_util.multilayer_perceptron(
                input_list,
                [200,100],
                ['none','relu'],
                name_pre='multi_tar_1_'
                )
            logging.info("mlp_out_list_1[-1].shape: %s", mlp_out_list_1[-1].shape) #(n_heads,64,200) * (200,100) = (n_heads,64,100)

            mlp_out_list_1_pos = mlp_out_list_1
            mlp_out_list = []
            for i, cur_input in enumerate(mlp_out_list_1_pos):
                cur_input_shape = 100
                show_index_shape = show_index_len
                logging.info('last layer %s input shape: %s, %s' % (i, cur_input_shape, show_index_shape))
                cur_input_1 = tf.concat([cur_input,show_index], axis=-1)
                w = tf.get_variable(
                    "last_layer_W{}".format(i),
                    [cur_input_shape + show_index_shape, 1],
                    initializer=tf.contrib.layers.xavier_initializer(),
                    dtype=tf.float32
                    )
                b = tf.get_variable(
                    "last_layer_b{}".format(i),
                    [1,1],
                    initializer=tf.contrib.layers.xavier_initializer(),
                    dtype=tf.float32
                    )
                mlp_out_list.append(tf.add(tf.matmul(cur_input_1,w),b))

            q = map(tf.nn.sigmoid, mlp_out_list)

            click_metric = ts.metrics('click', auc_table_size=1024*1024)
            cr_metric = ts.metrics('cr', auc_table_size=1024*1024)

            click_metrics.add(q[0], labels[0])
            q[1] = q[1] * q[0] # cr = cvr * ctr
            cr_metrics.add(q[1], labels[1])

            loss_op_click = tf.reduce_sum(tf.nn.sigmoid_cross_entropy_with_logits(logits=mlp_out_list[0], labels=labels[0]))
            loss_op_cr = tf.reduce_sum(tf.keras.backend.binary_crossentropy(target=labels[1], output=q[1]))

            for idx, label in enumerate(labels):
                tf.summary.histogram('label_%s' % idx, label)

            loss_ops = [loss_op_click, loss_op_cr]
            for idx, loss_op in enumerate(loss_ops):
                tf.summary.histogram('loss_op_%s' % idx, loss_op)

            loss = sum(loss_ops)
            ts.get_default_learner().local_storage["loss"] = loss
            ts.get_default_learner().local_storage["var_list_run"] = [s_emb, m_emb, l_emb, rv_feas, show_index, q, labels, meta_info]

            graph = tf.get_default_graph()
            gamma = graph.get_tensor_by_name("dense/MLP/norm_mlp_input_norm/gamma:0")
            beta = graph.get_tensor_by_name("dense/MLP/norm_mlp_input_norm/beta:0")
            ma = graph.get_tensor_by_name("dense/MLP/norm_mlp_input_norm/moving_mean:0")
            var =  graph.get_tensor_by_name("dense/MLP/norm_mlp_input_norm/moving_variance:0")
            ts.get_default_learner().local_storage["debug"] = [mlp_out_list]

            return loss, labels


def model_fn(batch, config):
    logging.info("Model Graph: %s", tf.get_default_graph())
    max_lookup_per_batch = batch_size * (slots_sizeS + slots_sizeM * max_emb_ids_size_1 + slots_sizeL * max_emb_ids_size_2)
    # sparse data
    sparse_opt = ts.train.SparseAdaGrad(
        learning_rate=learning_rate_mf,
        initial_g2sum=0.1,
        initial_range=1e-4,
        embedding_create_threshold=config['model']['embedding_create_threshold'],
        embedding_count_window_size=config['model']['embedding_count_window_size'],
        weight_bounds=[-10,10],
        cold_feature_remove_ttl=config['model']['cold_fea_ttl']
        )
    sparse_table = ts.SparseTable(
        [max_lookup_per_batch, embedding_size],
        'embed',
        optimizer=sparse_opt,
        local_shards=32
        )
    sparse_table.create_table()
    # dense data
    dense_opt = ts.train.DenseAdam(
        learning_rate=learning_rate,
        beta2=ada_decay_rate,
        beta1=mom_decay_rate,
        epsilon=ada_epsilon
        )
    dense_table = ts.DenseTable(optimizer=dense_opt)
    dense_table.create_table()

    # model -> loss
    loss, labels = build_model(batch, sparse_table)

    # gradient
    sparse_grads, dense_grads = ts.compute_gradients(
        loss,
        sparse_vars=[sparse_table.var()],
        dense_vars=tf.global_variables(scope='dense')
        )
    train_op_sparse = sparse_table.apply_gradients(sparse_grads)
    train_op_dense = dense_table.apply_gradients(dense_grads)
    train_op = tf.group(train_op_dense, train_op_sparse)

    #
    tf.summary.scalar("loss", loss)
    merged_summary = tf.summary.merge_all()
    ts.get_default_learner().local_storage['summary'] = merged_summary

    init_op = tf.group(
        tf.global_variables_initializer(),
        tf.local_variables_initializer()
        )

    return init_op, train_op


class LoopEnd(Exception):
    pass

def loop(train_op, loop_fn, config):
    logging.info("Start train")
    with ts.train.MultiDatasetRunner(graph=train_op.graph) as runner:
        loss_op = ts.get_default_learner().local_storage["loss"]
        pred_ops = runner.learner.metrics_ops + [loss_op]
        pred_op = tf.group(*pred_ops)

        _Loop = loop_fn(train_op, pred_op, config)
        looper = _Loop(runner)

        logging.info("Start init")
        looper.init()

        logging.info("Run training")
        start_time = datetime.datetime.now()
        batch_cnt = 0
        batch_start_time = datetime.datetime.now()

        while True:
            try:
                looper.run()
                batch_cnt += 1
                if batch_cnt % 1024 == 0:
                    current_datetime = datetime.datetime.now()
                    delta = current_datetime - start_time
                    global_rates = batch_cnt * 64 / delta.total_seconds() # batch_size=64
                    delta = current_datetime - batch_start_time
                    batch_rates = 1024 * 64 / delta.total_seconds()
                    batch_start_time = datetime.datetime.now()
                    logging.info('Finish 1024 batches, total samples: %s, global rates: %s, batch rates: %s' % (batch_cnt * 64, global_rates, batch_rates))
            except ts.train.EndOfOneDatasetError:
                logging.info("end of one dataset: %s" % runner.passed_ident)
                looper.end_one()
                continue
            except tf.errors.OutOfRangeError:
                logging.info('Out of range')
                looper.end()
                break
            except LoopEnd as le:
                logging.info('Loop end: %s', le)
                looper.end()
                break
            end_time = datetime.datetime.now()
            time_cost = end_time - start_time
            logging.info("cost time: %s" % time_cost)
            logging.info("total samples: %s" % (batch_cnt * 64))


def run(input_fn, loop_fn, mode, resource, peer_id, config):
    # omit ts.init

    metrics = ts.train.MetricsGroup()
    learner = ts.train.MultiThreadingLearner(metrics=metrics)

    def _input_fn():
        return input_fn(config)

    def _model_fn(batch):
        # omit config
        return model_fn(batch, config)

    def _train_fn(train_op):
        with train_op.graph.as_default():
            return loop(train_op, loop_fn, config)
        learner.start(1,_input_fn,_model_fn,_train_fn)
        learner.wait()

def start_from_config(input_fn, loop_fn, config):
    run(input_fn, loop_fn, config['mode'], config['resource'], config['peer_id'], config)