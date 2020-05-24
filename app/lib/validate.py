# -*- coding: UTF-8 -*-
import re
from app import Mongo
from app.lib.common import is_ip, is_number
from json import dumps


class TaskValidate(object):
    def __init__(self, **kwargs):
        self.task_name = "".join(kwargs.get("task_name", ""))
        self.task_ips = "".join(kwargs.get("task_ips", "")).strip()
        self.task_ports = "".join(kwargs.get("task_ports", ""))
        self.job_time = "".join(kwargs.get("job_time", ""))
        self.job_unit = "".join(kwargs.get("job_unit", ""))
        self.white_ip = "".join(kwargs.get("white_ip", ""))
        self.result = {}

    def check_ip(self, ips):
        ip_list = ips.split("\r\n")
        for ip_line in ip_list:
            if is_ip(ip_line) is False and ip_line != "":
                self.result = {"status": "error", "content": "错误的IP"}

        return self.result

    def check_port(self):
        if not re.search(r"^\d{1,5}$|^\d{1,5}-\d{1,5}$|\d{1,5},\d{1,5}", self.task_ports):
            self.result = {"status": "error", "content": "错误的端口"}
        return self.result

    def check_job_time(self):
        if self.job_unit in ["hours", "days"]:

            if not self.job_time:
                self.result = {"status": "error", "content": "非法时间"}
            elif not is_number(self.job_time):
                self.result = {"status": "error", "content": "非法时间"}
        return self.result

    def check_setting(self):
        if not Mongo.coll['setting'].find({}).count():
            self.result = {"status": "error", "content": "请先进行配置"}
        return self.result

    def check_task_name(self):
        if self.task_name:
            if Mongo.coll['tasks'].find({"name": self.task_name}).count():
                self.result = {"status": "error", "content": "任务名称不能重复，请修改"}
        elif not self.task_name.strip():
            self.result = {"status": "error", "content": "任务名称不能为空"}
        return self.result

    def check_job_unit(self):
        if self.job_unit not in ["hours", "days", "no"]:
            self.result = {"status": "error", "content": "非法时间单位"}
        return self.result

    def check(self, form):

        if self.check_ip(self.task_ips):
            return self.result

        if self.check_ip(self.white_ip):
            return self.result

        if self.check_port():
            return self.result

        if self.check_job_time():
            return self.result

        if self.check_setting():
            return self.result

        if self.check_job_unit():
            return self.result

        if form == "add_task":
            if self.check_task_name():
                return self.result

        return {"status": "success", "content": "验证通过"}
