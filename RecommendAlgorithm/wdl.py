
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


def build_model(batch, sparse_table):
    pb_saver = tf.train.Saver()
    ts.get_default_learner().local_storage['pb_saver'] = pb_saver
    rv_feas,single_slots,multi_slots,long_slots,click,cr,show_index,meta_info = batch

    rv_feas = tf.reshape(rv_feas, [-1,rv_feas_len])
    show_index = tf.reshape(show_index, [-1,show_index_len])
    labels = [cr]

    single_count_ratio = np.ones(single_slots.shape.shape.as_list()).ravel() * 200
    multi_count_ratio = np.ones(multi_slots.shape.as_list()).ravel() * 200
    long_count_ratio = np.ones(long_slots.shape.as_list()).ravel() * 200
    count_ratio = single_count_ratio.tolist() + multi_count_ratio.tolist() + long_count_ratio.tolist()

    s_emb_0,m_emb_0,l_emb_0 = sparse_table.embedding_pull(single_slots,multi_slots,long_slots,counting_ratio=count_ratio)
    
    s_emb = tf.reshape(s_emb_0, [-1, slots_sizeS * embedding_size])
    
    m_emb_1 = tf.reduce_sum(m_emb_0, 2)
    m_emb = tf.reshape(m_emb_1, [-1, slots_sizeM * embedding_size])

    l_emb_1 = tf.reduce_sum(l_emd_0, 2)
    l_emb = tf.reshape(l_emb_1, [-1, slots_sizeL * embedding_size])

    with tf.compat.v1.variable_scope('dense'):
        with tf.variable_scope('MLP'):
            # numeric
            mlp_rv_wide1 = tf.layers.dense(rv_feas, units=128, activation=tf.nn.relu, name="wide1")
            mlp_rv_wide2 = tf.layers.dense(mlp_rv_wide1, units=128, activation=tf.nn.relu, name="wide2")

            # categorical
            mlp_cat_deep1 = tf.layers.dense(s_emb, units=128, activation=tf.nn.relu, name="deep1")
            mlp_cat_deep2 = tf.layers.dense(mlp_cat_deep1, units=128, activation=tf.nn.relu, name="deep2")

            mlp_input = tf.concat([rv_feas, mlp_rv_wide2, mlp_cat_deep2], axis=-1, name="mlp_input")
            merge2 = tf.layers.dense(mlp_input, units=64, activation=tf.nn.relu, name="merge2")
            mlp_input_norm = tf.layers.batch_normalization(
                inputs = merge2,
                momentum = mom_decay_rate,
                name = "norm_mlp_input_norm"
                )            
            merge3 = tf.layers.dense(merge2, units=64, activation=tf.nn.relu, name="merge3")
            dropout = tf.nn.dropout(merge3, 0.9, name="keep")

        with tf.variable_scope('Multi_Tar'):
            mlp_out_list = []
            mlp_out_list.append(tf.layers.dense(dropout, units=1, name="output_score"))
        q = map(tf.nn.sigmoid, mlp_out_list)

        cr_metrics = ts.metrics('cr', auc_table_size=1024*1024)
        cr_metrics.add(q[0], labels[0])
        loss_op_cr = tf.reduce_sum(tf.nn.sigmoid_cross_entropy_with_logits(logits=mlp_out_list[0], labels=labels[0]))

        for idx,label in enumerate(labels):
            tf.summary.histogram('label_%s' % idx,label)

        loss_ops = [loss_op_cr]

        for idx, loss_op in enumerate(loss_ops):
            tf.summary.histogram('loss_op_%s' % idx,loss_op)

        loss = sum(loss_ops)
        ts.get_default_learner().local_storage('loss') = loss
        ts.get_default_learner().local_storage['var_list_run'] = [s_emb,m_emb,l_emb,rv_feas,show_index,q,labels,meta_info]

        graph = tf.get_default_graph()
        gamma = graph.get_tensor_by_name('dense/MLP/norm_mlp_input_norm/gamma:0')
        beta = graph.get_tensor_by_name('dense/MLP/norm_mlp_input_norm/bata:0')
        ma = graph.get_tensor_by_name('dense/MLP/norm_mlp_input_norm/moving_mean:0')
        var = graph.get_tensor_by_name('dense/MLP/norm_mlp_input_norm/moving_variance:0')
        ts.get_default_learner().local_storage['debug'] = [mlp_out_list]

        return loss, labels
