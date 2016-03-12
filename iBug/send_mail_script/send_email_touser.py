#coding: utf-8
import pika
import random
import sys
import json

class Focus_send_email():

    def filter_userlist(self,to_string): #筛选
        try:
            tolist=to_string.split(',')
            userlist=""  #用来存放筛选好的人员列表
            for item in tolist:
                if "@" not in item:
                    userlist+=item+','
                elif "spreadtrum" in item:
                    userlist+=item+','
        except:
            userlist=""

        print "="*80
        print "info:"+userlist
        return userlist


    def send_mail(self,to_string,cc_string,bcc_string,sub,content,ip):
        if ip!="10.0.6.166":#判断是否为正式库。正式库可以任意发送。非正式库筛选掉客户邮件
            if to_string is not None and to_string is not "":  #筛选to
                to_string=self.filter_userlist(to_string)
            if cc_string is not None and cc_string is not "": #筛选cc
                cc_string=self.filter_userlist(cc_string)
            if bcc_string is not None and bcc_string is not "": #筛选bcc
                bcc_string=self.filter_userlist(bcc_string)

        print "-"*80
        print "info  send_mail:"+str(cc_string)

        if to_string is not "": #发送列表不为""
            import smtplib
            import re
            from email.MIMEText import MIMEText
            from smtplib import SMTP
            fromUser = "iSupport"
            mail_host = "10.0.1.200"
            mail_postfix = "@spreadtrum.com"
            me = fromUser + "<" + fromUser + mail_postfix + ">"
            msg = MIMEText(content.encode('utf-8'), _subtype='html', _charset='utf-8')

            All_LIST = []
            TOList = []
            CCList = []

            cc_string=cc_string.strip()
            if cc_string :
                for a_cc in cc_string.split(',') :
                    if a_cc.strip()!="":
                        if (a_cc.strip()+mail_postfix) not in CCList :
                            CCList.append(a_cc.strip()+mail_postfix)

            if (fromUser.strip()+mail_postfix) not in CCList :
                CCList.append(fromUser.strip()+mail_postfix)

            to_string = to_string.strip()
            if to_string:
                to_string = re.split(r'[;,\s]+', to_string)
            else:
                to_string = []

            if len(to_string) == 0:
                return

            if to_string :
                for a_to in to_string :
                    if '@' not in a_to:
                        if (a_to.strip() + mail_postfix) not in TOList :
                            TOList.append(a_to.strip() + mail_postfix)
                    else:
                        if a_to.strip()  not in TOList :
                            TOList.append(a_to.strip())

            for aa in TOList:
                if aa not in All_LIST :
                    All_LIST.append(aa)

            for aa in CCList:
                if aa not in All_LIST :
                    All_LIST.append(aa)


            msg['Subject'] = sub
            msg['From'] = me
            msg['To'] = ','.join(TOList)
            msg['Cc'] = ','.join(CCList)
            s = SMTP(mail_host, 587)
            s.starttls()
            s.login("iSupport", "cqa$$123")

            try:
                s.sendmail(me, All_LIST, msg.as_string())
            except Exception,e :
                raise e

if __name__ == "__main__":

    #链接rabbitmq服务器start
    credentials = pika.PlainCredentials('xiaohui.geng', 'xiaohui.geng')  #登录凭据
    #这里可以连接远程IP，请记得打开远程端口
    parameters = pika.ConnectionParameters('10.0.0.130',5672,'/',credentials)  #登录参数
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel() #通道
    #链接rabbitmq服务器end

    channel.queue_declare(queue='psit_ibug_queue', durable=True)  #队列声明
    print ' [*] Waiting for messages. To exit press CTRL+C'
    def callback(ch, method, properties, body):  #回调
        print " [x] Received %r" % (body,)
        send_email=Focus_send_email()
        msg=json.loads(body, encoding="utf-8")


        send_email.send_mail(msg["to"],msg["cc"],msg["bcc"],msg["Subject"],msg["content"],msg["ip"])
        # time.sleep(5)
        ch.basic_ack(delivery_tag = method.delivery_tag)   #消息确认就是当工作者完成任务后，会反馈给rabbitmq
    channel.basic_qos(prefetch_count=1)  #公平调度,基本服务质量
    channel.basic_consume(callback,     #基本消耗
                            queue='psit_ibug_queue',
                            no_ack=False) #no_ack=False 工作者ctrl+c退出后，正在执行的任务也不会丢失，rabbitmq会将任务重新分配给其他工作者。
    channel.start_consuming()  #开始消耗



