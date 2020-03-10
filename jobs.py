#
# test script
# curl -i -X POST -H "'Content-type':'appon/x-www-form-urlencoded', 'charset':'utf-8', 'Accept': 'text/plain'" -d '{"id":"job5","func": "test:job1","args":"(\"aaa\",\"aaadd\")","trigger":"interval","seconds":60}' http://127.0.0.1:5000/addjob
#
from flask import Flask
from flask_apscheduler import APScheduler
from apscheduler.jobstores.mongodb import MongoDBJobStore
from flask import request
import os
import time
from app.lib.log_handle import Log
app = Flask(__name__)
scheduler = APScheduler()


class Config(object):
    JOBS = []
    SCHEDULER_JOBSTORES = {
        'default': MongoDBJobStore(database='apscheduler', collection='jobs',host='mongodb://%s:%s@%s:%s/' % ('root', 'chjsec_', '192.168.47.146', '27017'))
    }

    SCHEDULER_EXECUTORS = {
        'default': {'type': 'threadpool', 'max_workers': 20}
    }

    SCHEDULER_JOB_DEFAULTS = {
        'coalesce': True,
        'max_instances': 3
    }

    SCHEDULER_API_ENABLED = True


def job1(a, b):
    1/0
    print(str(a) + ' ' + str(b) + '   ' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))


def job2(a):
    py = 'python wx_post_test.py ' + a
    os.system(py)


def jobfromparm(**jobargs):
    id = jobargs['id']
    func = jobargs['func']
    args = (jobargs['args'].split(","))
    trigger = jobargs['trigger']
    seconds = int(jobargs['seconds'])
    print('add job: ', id)
    job = scheduler.add_job(func=func, id=id, args=args, trigger=trigger, seconds=seconds, replace_existing=True)
    return 'sucess'


@app.route('/pause')
def pausejob():
    scheduler.pause_job('job1')
    return "Success!"


@app.route('/resume')
def resumejob():
    scheduler.resume_job('job1')
    return "Success!"


@app.route('/addjob', methods=['GET', 'POST'])
def addjob():
    data = request.get_json(force=True)
    print(data)
    job = jobfromparm(**data)
    return 'sucess'


@app.route('/test')
def test():
    data = {
        "id": "test_job",
        "func": "jobs:job1",
        "args": "a,b",
        "trigger": "interval",
        "seconds": "30"
    }
    print(data)
    job = jobfromparm(**data)
    return 'sucess'


if __name__ == '__main__':
    # app = Flask(__name__)
    app.config.from_object(Config())

    # it is also possible to enable the API directly
    # scheduler.api_enabled = True
    scheduler = APScheduler()
    scheduler.init_app(app)
    scheduler._logger = Log()
    scheduler.start()
    app.run(host='0.0.0.0')
    # app.run()
