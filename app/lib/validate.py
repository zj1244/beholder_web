# -*- coding: UTF-8 -*-
import re
from app import Mongo
from app.lib.common import is_ip, is_number
from json import dumps


class Validate(object):
    def __init__(self, **kwargs):
        self.task_name = "".join(kwargs.get("task_name", ""))
        self.task_ips = "".join(kwargs.get("task_ips", ""))
        self.task_ports = "".join(kwargs.get("task_ports", ""))

        self.cron_time = "".join(kwargs.get("cron_time", ""))
        self.cron_unit = "".join(kwargs.get("cron_unit", ""))

        self.white_ip = "".join(kwargs.get("white_ip", ""))

    def check(self):
        if not Mongo.coll['setting'].find({}).count():
            return  {"status": "error", "content": "请先进行配置"}

        if self.task_name:
            if Mongo.coll['tasks'].find({"name": self.task_name}).count():
                return {"status": "error", "content": "任务名已存在"}
        else:
            return {"status": "error", "content": "任务名为空"}

        white_ip = self.white_ip.split("\r\n")
        if white_ip:
            for ip_line in white_ip:
                if is_ip(ip_line) == False and ip_line != "":
                    return {"status": "error", "content": "错误的IP"}

        if not is_ip(self.task_ips):
            return {"status": "error", "content": "错误的IP"}

        if not re.search(r"^\d{1,5}$|^\d{1,5}-\d{1,5}$|\d{1,5},\d{1,5}", self.task_ports):
            return {"status": "error", "content": "错误的端口"}

        if self.cron_unit in ["hours", "days"]:

            if not self.cron_time:
                return {"status": "error", "content": "非法时间"}
            elif not is_number(self.cron_time):
                return {"status": "error", "content": "非法时间"}

        if self.cron_unit not in ["hours", "days", "no"]:
            return {"status": "error", "content": "非法时间单位"}

        return {"status": "success", "content": "验证通过"}



