import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

### read data

train_dataset = pd.read_csv('../data/train_pm.csv')
test = pd.read_csv('../data/test_pm.csv',header=None)

# train_dataset.columns=['date', 'station', 'testmaterial', '0', '1', '2', '3', '4', '5', '6', '7', '8','9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20','21', '22', '23']
# train_dataset['station'] = 'station'
test.columns=['date','testmaterial', '0', '1', '2', '3', '4', '5', '6', '7', '8']

train_dataset = train_dataset.loc[train_dataset['testmaterial']=='PM2.5']
train_dataset.drop(columns=['date','station','testmaterial'],inplace=True)
test = test.loc[test['testmaterial']=='PM2.5']
test.drop(columns=['testmaterial'],inplace=True)

train_dataset = train_dataset.astype('float')
for c in ['0', '1', '2', '3', '4', '5', '6', '7', '8']:
    test[c] = test[c].astype('float')

print(train_dataset.shape) # (240, 24)
print(test.shape) # (240, 9) +1


### generate training data
# '0', '1', '2', '3', '4', '5', '6', '7', '8' ->'9'
# '1', '2', '3', '4', '5', '6', '7', '8', '9' -> '10'
# '2', '3', '4', '5', '6', '7', '8', '9', '10' -> '11'
# ...
# '14', '15', '16', '17', '18', '19', '20', '21', '22' -> '23'
# 240 * 15 = 3600

cols = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
train = pd.DataFrame(columns=cols)
for i in range(15):
    c = [str(int(x)+i) for x in cols]
    tmp = train_dataset[c]
    tmp.columns = cols
    train = train.append(tmp)
train.reset_index(inplace=True,drop=True)
print(train.shape) # (3600, 10)


### training with gradient decent. y = b + w * x

train,valid = train_test_split(train,test_size=0.3,random_state=4)

x_data = train[['0', '1', '2', '3', '4', '5', '6', '7', '8']].values
tr_x = np.concatenate((np.ones((x_data.shape[0],1)),x_data),axis=1) # b,w
tr_y = train['9'].values
x_valid = valid[['0', '1', '2', '3', '4', '5', '6', '7', '8']].values
va_x = np.concatenate((np.ones((x_valid.shape[0],1)),x_valid),axis=1) # b,w
va_y = valid['9'].values

w = np.zeros(len(tr_x[0]))
iteration = 10000
lr = 0.1
lr_b = 0
lr_w = 0
s_grad = np.zeros(len(tr_x[0]))

loss_train = []
loss_valid = []

for i in range(iteration):
    # b_grad = 0.0
    # w_grad = np.zeros(len(x_data[0]))
    # for n in range(len(x_data)):
    #     b_grad = b_grad - 2.0 * (y_data[n] - (b + np.dot(w,x_data[n]))) * 1.0
    #     w_grad = w_grad - 2.0 * (y_data[n] - (b + np.dot(w,x_data[n]))) * x_data[n]
    # b = b - lr * b_grad
    # w = w - lr * w_grad
    res = np.dot(tr_x, w.transpose())
    loss = res - tr_y
    loss_train.append(sum(loss))
    loss_valid.append(sum(np.dot(va_x, w.transpose()) - va_y))

    grad = np.dot(tr_x.transpose(),loss)
    s_grad = s_grad + grad ** 2
    ada = np.sqrt(s_grad.astype('float'))
    w = w - lr / ada * grad

np.save('model.npy',w)


### plot

x = np.arange(iteration)
plt.plot(x, loss_train, 'o-', ms=3, lw=1.5, color='blue',label='train')
plt.plot(x, loss_valid, 'x-', ms=3, lw=1.5, color='red',label='valid')
plt.legend()
plt.xlim(0,10)
plt.ylim(-20000,0)
plt.xlabel('iteration')
plt.ylabel('loss')
plt.title('iteration-loss')
plt.show()


### predict
c = ['0', '1', '2', '3', '4', '5', '6', '7', '8']
te = np.array(test[c],float)
te = np.concatenate((np.ones((te.shape[0],1)),te),axis=1)
res = []
res = np.dot(te,w.transpose())
test['value'] = res
test[['date','value']].to_csv('submit.csv')