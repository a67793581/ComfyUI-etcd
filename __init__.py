# 定义包的版本
__version__ = '0.1.0'

import os
import time

from dotenv import load_dotenv

import etcd3

# 定义常量
RpcPrefix = "/project/http/%s/%s/%s:%s"
# 加载 .env 文件
load_dotenv()


def RpcName() -> str:
    """
    :return:
    """
    ip = os.getenv('IP')
    port = os.getenv('PORT')
    name = os.getenv('NAME')
    return RpcPrefix % (os.getenv('ENV', 'local'), name, ip, port)


def Registered():
    """
    :return:
    """
    host = os.getenv('HOST')
    etcd = etcd3.client(host=host)
    # "id":"maliang-core-dev-bc6589677-k9jqw",
    # "name":"/project/rpc/dev/clotho-ma_liang",
    # "addr":"10.185.128.58:8082",
    # "version":"",
    # "weight":0,
    # "metadata":{"dubbo-services":"proto.ma_liang.MaLiangApi","env":"dev"},
    # "endpoints":["grpc://10.185.128.58:8082","http://10.185.128.58:9000"
    print(etcd.put(RpcName(), ))
    print(etcd.get(RpcName()))


Registered()
time.sleep(60 * 3)
