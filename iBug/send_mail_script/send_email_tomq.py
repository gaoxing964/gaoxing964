#coding: utf-8
import pika
import random
import sys
import json
import socket
import datetime
from email.mime.text import MIMEText

def send(to,cc,bcc,Subject,content):
    _t = MIMEText(content, 'html')
    content = _t.get_payload()#邮件内容

    #链接rabbitmq服务器start
    credentials = pika.PlainCredentials('xiaohui.geng', 'xiaohui.geng')
    #这里可以连接远程IP，请记得打开远程端口
    parameters = pika.ConnectionParameters('10.0.0.130',5672,'/',credentials)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    #链接rabbitmq服务器end

    #新建消息队列。durable表示队列任务不会消失
    channel.queue_declare(queue='psit_ibug_queue', durable=True) #rabbitmq不允许使用不同的参数来重新定义存在的队列。重新定义一个队列：

    #推送给队列的消息
    #msg的参数 start
    hostname = socket.gethostname()  #name
    ip = socket.gethostbyname(hostname)  #IP
    #msg的参数 end


    message={"to":to,"cc":cc,"bcc":bcc,"Subject":Subject,"content":content,"ip":ip}
    message=json.dumps(message)


    channel.basic_publish(exchange='',            #基本发布
                            routing_key='psit_ibug_queue',
                            body=message,
                            properties=pika.BasicProperties(delivery_mode = 2, ),#消息持久化存储
                            )
    print " [x] Sent %r" % (message,)
    connection.close()  #关闭


def build_create_bug_info_content_html(bug_info):

    special_test_name = bug_info.get("special_test_name","")
    special_test_parents_project = bug_info.get("special_test_parents_project","")
    case_number = bug_info.get("case_number","")
    bug_description = bug_info.get("bug_description","")
    parents_category = bug_info.get("parents_category","")
    owner = bug_info.get("owner","")
    is_solved = bug_info.get("is_solved","")
    bug_id = bug_info.get("bug_id","")
    remark = bug_info.get("remark","")
    author = bug_info.get("author","")
    priority = bug_info.get("priority","")

    html = """\
    <html>
      <head></head>
      <body>
       <div style="margin-left:30px;font-size:16px;">
              <h3>Dear %s:</h3>
                <div style="margin-left:30px;">
               <p>问题详情如下：</p>
               <p>---------------------------------------------</p>
               %s
               <p>---------------------------------------------</p>
               </div>

               <p style="margin-left:30px;">请及时处理，谢谢。</p>
               <p style="margin-left:30px;font-size:12px;color:#666">邮件由PSIT iQuality系统发送，请勿回复</p>
          </div>
      </body>
    </html>
    """

    _template = """
          <table >
                <tr>
                  <td style="text-align:right;">CASE编号: </td>
                  <td >%s</td>
                </tr>

                <tr>
                  <td style="text-align:right;">作者: </td>
                  <td >%s</td>
                </tr>

                <tr>
                  <td style="text-align:right;">问题描述:</td>
                  <td >%s</td>
                </tr>

                <tr>
                  <td style="text-align:right;">所属模块: </td>
                  <td >%s</td>
                </tr>

                <tr>
                  <td style="text-align:right;">是否已解决: </td>
                  <td >%s</td>
                </tr>

                <tr>
                  <td style="text-align:right;">优先级: </td>
                  <td >%s</td>
                </tr>

                <tr>
                  <td style="text-align:right;">BugID:</td>
                  <td >%s</td>
                </tr>

                <tr>
                  <td style="text-align:right;">备注: </td>
                  <td >%s</td>
                </tr>

                <tr>
                  <td style="text-align:right;">项目: </td>
                  <td >%s</td>
                </tr>

                <tr>
                  <td style="text-align:right;">专项测试: </td>
                  <td >%s</td>
                </tr>
          </tbody></table><br><br>
     """    %  (case_number, author, bug_description, parents_category, is_solved, priority, bug_id, remark, special_test_parents_project, special_test_name)

    html = html % (owner, _template.encode('utf-8').strip())

    return html


def build_summary_content_html(project):
    html = """\
    <html>
      <head></head>
      <body>
       <div style="margin-left:30px;font-size:16px;">
              <h3>Dear all:</h3>
                <div style="margin-left:30px;">
               <p>昨天专项测试处理情况如下：</p>
               %s
               </div>

               <p style="margin-left:30px;">请及时处理，谢谢。</p>
               <p style="margin-left:30px;font-size:12px;color:#666">邮件由PSIT iQuality系统发送，请勿回复</p>
          </div>
      </body>
    </html>
    """

    _template = """

                <table style="border:1px solid #9bcffd;">
                  <tbody><tr><td colspan="2" style="background: #9BCFFD;padding:10px;font-weight:700;">%s  专项未解决问题列表</td></tr>
                  %s
                </tbody></table>
           <br><br>
     """

    _template_inner = """
                <tr><td style="border:1px solid #9bcffd;padding:10px;">%s</td>
                <td style="border:1px solid #9bcffd;padding:10px;">%s</td></tr>
     """

    _table_html = []
    _tr = []

    if len(project["current_open_bugs"]) ==0 :
        return ""

    for current_open_bugs in project["current_open_bugs"]:
        _tr.append(_template_inner % (  current_open_bugs["bug_description"], current_open_bugs["owner"]))
    _tr_html = u"".join(_tr).encode('utf-8').strip()
    _table_html.append(_template % ( project["special_test_name"], _tr_html))

    html = html % (u"".join(_table_html).encode('utf-8').strip())

    return html


#  topic  模糊对应 fanout 全部发   direct 一一对应
if __name__ == "__main__":
    from email.mime.text import MIMEText
    import urllib2
    import sys

    reload(sys)
    sys.setdefaultencoding("utf-8")

    f = urllib2.urlopen("http://localhost:5000/api/bug_count_for_email")
    response = f.read()
    response = json.loads(response)

    for project in response["data"]:

        if len(project["current_open_bugs"]) ==0 :
            continue

        html = build_content(project)
        to= project["special_test_pm"] #发送给谁
        Subject=" %s  %s 专项测试汇总通知邮件" % (str(datetime.date.today()),project["special_test_name"],)                     #邮件主题
        cc= project["special_test_cc_list"]
        bcc=project["special_test_cc_list"]

        part2 = MIMEText(html, 'html')
        content=part2.get_payload()#邮件内容
        send(to,cc,bcc,Subject,content)

