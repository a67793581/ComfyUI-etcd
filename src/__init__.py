# 定义包的版本
__version__ = '0.1.0'

import asyncio
import json
import os
import time
import etcd3

# 定义常量
RpcPrefix = "/project/http/%s/%s/%s:%s"


def RpcName() -> str:
    """
    :return:
    """
    ip = os.getenv('IP')
    port = os.getenv('PORT')
    name = os.getenv('NAME')
    return RpcPrefix % (os.getenv('ENV', 'local'), name, ip, port)


def GetEtcd() -> etcd3.Etcd3Client:
    """
    :return:etcd3.Etcd3Client
    """
    host = os.getenv('HOST')
    etcd = etcd3.client(host=host)
    return etcd


def check_key_lease(etcd, key):
    """
    检查键是否绑定了租约
    """
    try:
        value, metadata = etcd.get(key)
        if metadata.lease_id is not None:
            print(f"Key {key} is bound to lease ID: {metadata.lease_id}")
        else:
            print(f"Key {key} is not bound to any lease")
    except Exception as e:
        print(f"Error checking key lease: {e}")


async def Registered(ttl = 2):
    """
    :return:asyncio.Task
    """
    etcd = GetEtcd()
    lease = etcd.lease(ttl)
    etcd.get_lease_info(lease.id)
    etcd.put(RpcName(), json.dumps({
        "ip": os.getenv('IP'),
        "port": os.getenv('PORT'),
        "env": os.getenv('ENV', 'local'),
        "name": os.getenv('NAME'),
    }).encode(), lease)
    check_key_lease(etcd, RpcName())
    try:
        while True:
            await asyncio.sleep(lease.ttl // 2)
            lease.refresh()
            if os.getenv('DEBUG'):
                print(f"Lease {lease.id} refreshed ,timestamp: {time.time()}")
    except asyncio.CancelledError:
        print("Lease refresh task cancelled")
    except Exception as e:
        print(f"Error refreshing lease: {e}")
