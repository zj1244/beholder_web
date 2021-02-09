# !/usr/bin/env python
# -*- coding: utf-8 -*-
import json, struct, socket
import re
import requests
from datetime import datetime

from log_handle import Log

from app import Mongo
from app import redis_web

try:
    from mailer import Mailer
    from mailer import Message
except ImportError:
    Log().warning("error Missing Mailer")


def send_mail(subject, contents, host, use_ssl, sender, pwd, email_address):
    try:
        message = Message(From=sender,
                          To=email_address, charset="utf-8")
        message.Subject = subject
        message.Html = contents
        if sender[sender.find("@")+1:] in host:
            sender=sender[:sender.find("@")]
        mailer = Mailer(host=host, use_ssl=use_ssl, usr=sender,
                        pwd=pwd)

        mailer.send(message, debug=False)

        Log().info("sender:%s,to=%s" % (sender, email_address))
    except Exception as e:
        Log().exception(e)
        return False
    return True


def get_ip_list(ips):
    ip_list = []
    ips = ips.strip()
    if ips:
        ips = ips.split("\r\n")
        for ip in ips:
            ip_list += format_ip(str(ip))

    return ip_list


def is_last_task(task_name):
    task_count = Mongo.coll['tasks'].find({'name': {"$ne": task_name}}).count()
    if task_count:
        return False
    else:
        return True


def is_ip(ip):
    patt = r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$|^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}-\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$"
    if not re.search(patt, ip):
        return False
    return True


def format_ip(ip_range):
    if "-" in ip_range:
        start_ip, end_ip = ip_range.split('-')

        ip_list = convert_ip_range(start_ip, end_ip)
    else:
        ip_list = [ip_range]
    return ip_list


def delete_ip(task_id=""):
    if task_id:
        redis_web.del_key("scan_" + str(task_id))
        redis_web.zremrangebyscore("ack_scan_" + str(task_id), "-INF", "+INF")
    else:
        scan_keys = redis_web.keys("scan*")
        if scan_keys:
            redis_web.del_key(*scan_keys)
            ack_keys = redis_web.keys("ack_scan_*")
            if ack_keys:
                for ack in ack_keys:
                    redis_web.zremrangebyscore(ack, "-INF", "+INF")


def convert_ip_port_to_details(ip_port_list=None):
    res=[]
    if ip_port_list is None:
        ip_port_list = []
    for i in ip_port_list:
        ip, port = i.split(":")

        c = Mongo.coll["scan_result"].find_one({"ip": ip, "port": int(port)},
                                               sort=[("create_time", -1)])

        res.append({"ip": i, "service": c["service"], "version_info": c["version_info"].strip()})
    return res

def add_ip(task_name, task_ips, task_ports, task_type, cron, white_ip=""):
    mongo_task = Mongo.coll['tasks']
    if mongo_task.find_one({"name": task_name, "task_status": {"$ne": "finish"}}):  # 有没完成的任务就不插入新任务了
        return False
    create_time = datetime.now()
    ips = get_ip_list(task_ips)
    try:
        Log().info("开始插入数据")

        white_ip = get_ip_list(white_ip)
        ips = set(ips) - set(white_ip)
        if not ips:
            return False
        pipe = redis_web.pipe()
        if task_type == "monitor_task":
            task_result = {
                "monitor_result": {"monitor": 0}
            }
        elif task_type == "diff_task":
            task_result = {
                "diff_result": {"diff": 0}
            }

        else:
            task_result = {}

        insert_result = mongo_task.insert_one(
            dict({"name": task_name, "ip": task_ips, "port": task_ports,
                  "task_status": "ready", "create_time": create_time,
                  "task_type": task_type, "cron": cron}, **task_result))

        nmapscan_key = "scan_" + str(insert_result.inserted_id)

        for ip in ips:
            sub_task_dict = {"base_task_id": str(insert_result.inserted_id), "ip": ip, "port": task_ports,
                             "task_status": "ready"}

            pipe.lpush(nmapscan_key, dict2str(sub_task_dict))

        if insert_result:
            pipe.execute()
            Log().info("任务【%s】的数据插入完毕" % task_name)
            mongo_task.update_one({"_id": insert_result.inserted_id},
                                  {"$set": {"task_status": "running"}})
            return True

    except:
        Log().exception("插入数据失败")
        return False


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
    return False


def ip_atoi(ip):
    return struct.unpack('!I', socket.inet_aton(ip))[0]


def ip_itoa(ip):
    return socket.inet_ntoa(struct.pack('!I', ip))


def convert_ip_range(start_ip, end_ip):
    ip_list = []
    start_ip = ip_atoi(start_ip)
    end_ip = ip_atoi(end_ip) + 1
    for ip in range(start_ip, end_ip):
        ip_list.append(ip_itoa(ip))
    return ip_list


def dict2str(dictionary):
    try:
        if type(dictionary) == str:
            return dictionary
        return json.dumps(dictionary)
    except TypeError as e:
        Log().exception("conv dict failed : %s" % e)
