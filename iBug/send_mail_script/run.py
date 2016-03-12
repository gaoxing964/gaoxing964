# -*- coding: utf-8 -*-

# author: liang.han
# date : 2014-12-25    merry christmas
# mail : liang.han@spreadtrum.com,cnfync@163.com

import sched
import time
import os
import datetime

from send_email_tomq import *

class Task(object):
    """docstring for task"""
    def __init__(self, delay,priority,action,argument):
        self.delay = delay           #执行周期，以秒为单位
        self.priority = priority    #优先级
        self.action = action        #回调方法
        self.argument = argument    #回调方法参数

    def set_scheduler(self,scheduler):
        self.scheduler = scheduler

    def start(self):
        self.action()
        self.scheduler.enter(self.delay,self.priority,self.start,self.argument)

class Task_Queue(object):
    """docstring for task_queue"""
    def __init__(self):
        self.scheduler =  sched.scheduler(time.time,time.sleep)
        self.tasks = []

    def push(self, task):
        self.tasks.append(task)

    def start(self):
        for task in self.tasks:
            task.set_scheduler(self.scheduler)
            task.start()

        self.scheduler.run()


if __name__ == "__main__":
    def send_mail():

        from email.mime.text import MIMEText
        import urllib2
        import sys

        reload(sys)
        sys.setdefaultencoding("utf-8")

        current = int(time.strftime('%H%M'))
        if current > 2356 and current<2359:
            f = urllib2.urlopen("http://localhost:5000/api/bug_count_for_email")
            response = f.read()
            response = json.loads(response)

            for project in response["data"]:

                if len(project["current_open_bugs"]) ==0 :
                    continue

                html = build_summary_content_html(project)
                to= project["special_test_pm"] #发送给谁
                Subject=" %s  %s 专项测试汇总通知邮件" % (str(datetime.date.today()),project["special_test_name"],) #邮件主题
                cc= project["special_test_cc_list"]
                bcc=project["special_test_cc_list"]

                part2 = MIMEText(html, 'html')
                content=part2.get_payload()#邮件内容
                send(to,cc,bcc,Subject,content)

    queue = Task_Queue()
    task_for_bakup_fae_database = Task(120,1,send_mail,())
    queue.push(task_for_bakup_fae_database)

    queue.start()




