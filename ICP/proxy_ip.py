# coding=utf-8
'''
    IP代理获取
'''

import redis
import requests
import Queue
import threading
import config


proxy_q = Queue.Queue()

pool = redis.ConnectionPool(host = '10.245.146.81' , port = 6379)
redis_conn = redis.Redis(connection_pool = pool)


def get_one_proxy(redis_conn):
    '''
    功能：从redis获取一个代理
    '''

    proxy = redis_conn.lpop("ip_list")
    return proxy



def test_ip_proxy(proxy):
    '''
    功能：测试该代理ip是否可用
    '''
    ip_proxy = {'http':proxy}
    try:
        res = requests.get('http://www.baidu.com', proxies = ip_proxy, timeout = config.proxy_ip_test_timeout)
        if res.content.find('百度一下') != -1:
            print 'available:', proxy
            return True
        else:
            False
    except Exception, e:
        print proxy + '代理测试异常'
        return False


def get_one_available_proxy():
    '''
    测试代理ip的可用性
    '''
    global redis_conn
    global proxy_q

    while True:
        proxy = get_one_proxy(redis_conn)
        print 'test: ', proxy
        test_res = test_ip_proxy(proxy)
        if test_res:
            proxy_q.put(proxy)


def watch():
    pass

if __name__ == '__main__':
    print get_one_proxy(redis_conn)
    # redis_conn
