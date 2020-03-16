#!/usr/bin/env python
# coding: utf-8

import os
import sys
from apscheduler.jobstores.mongodb import MongoDBJobStore
from dotenv import find_dotenv, load_dotenv

reload(sys)
sys.setdefaultencoding('utf-8')


class BaseConfig(object):
    WTF_CSRF_ENABLED = True


class ProductionConfig(BaseConfig):
    try:
        load_dotenv(find_dotenv("config.env"))
        ACCOUNT = os.getenv("ACCOUNT", "admin")
        PASSWORD = os.getenv("PASSWORD", "admin")
        MONGO_IP = os.getenv("MONGO_IP", "192.168.47.168")
        MONGO_PORT = int(os.getenv("MONGO_PORT", 27018))
        MONGO_USER = os.getenv("MONGO_USER", "scan")
        MONGO_PWD = os.getenv("MONGO_PWD", "123456")
        MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "portscan")

        REDIS_IP = os.getenv("REDIS_IP", "192.168.47.168")
        REDIS_PORT = os.getenv("REDIS_PORT", "6378")
        REDIS_PWD = os.getenv("REDIS_PWD", "pwd")
    except Exception as e:
        print e
        print "请检查是否把config.env.sample复制成config.env"
        os._exit(0)

    JOBS = []
    SCHEDULER_JOBSTORES = {
        'default': MongoDBJobStore(database='apscheduler', collection='beholder_jobs',
                                   host='mongodb://%s:%s@%s:%s/' % (
                                       MONGO_USER, MONGO_PWD, MONGO_IP, MONGO_PORT))
    }
    SCHEDULER_EXECUTORS = {
        'default': {'type': 'threadpool', 'max_workers': 20}
    }
    SCHEDULER_JOB_DEFAULTS = {
        'coalesce': True,
        'max_instances': 3
    }
    SCHEDULER_API_ENABLED = True
