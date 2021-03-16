# 1. 免密登录

远程服务器上git会出现如下问题

![image](https://gitee.com/journey7878/img-bed/raw/master/Programming/git001.png)

为了解决上述问题，需要对服务器进行ssh免密码登录的操作。

首先在服务器终端输入如下指令

```shell
ssh-keygen -t rsa -P '' -f ~/.ssh/id_rsa
cd ~/.ssh
vim id_rsa.pub
```

打开 git --> Settings --> SSH Keys --> 把上面的内容复制过来 --> Add key --> 正常 git clone --> Done


