from apscheduler.jobstores.mongodb import MongoDBJobStore
from dotenv import find_dotenv, load_dotenv

import os


class BaseConfig(object):
    ACCOUNT = 'admin'
    PASSWORD = 'admin'
    WTF_CSRF_ENABLED = False
    WTF_CSRF_CHECK_DEFAULT = False


class ProductionConfig(BaseConfig):
    load_dotenv(find_dotenv())

    MONGO_IP = os.getenv("MONGO_IP")
    MONGO_PORT = int(os.getenv("MONGO_PORT"))
    MONGO_USER = os.getenv("MONGO_USER")
    MONGO_PWD = os.getenv("MONGO_PWD")
    MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")

    REDIS_IP = os.getenv("REDIS_IP")
    REDIS_PORT = os.getenv("REDIS_PORT")
    REDIS_PWD = os.getenv("REDIS_PWD")

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
