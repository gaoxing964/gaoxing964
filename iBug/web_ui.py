#-*- coding:utf-8 -*-
import json
import time
import os
import urllib
from flask import Flask, render_template, request, send_from_directory,redirect,url_for
import flask.ext.login as flask_login
#from flup.server.fcgi import WSGIServer
import ldap
import datetime

from model import *
from base import *
import service
from send_mail_script.send_email_tomq import  build_create_bug_info_content_html, send



app = Flask(__name__)
app.secret_key = '!QAZ@WSX#EDC$RFV'  # Change this!
login_manager = flask_login.LoginManager()
login_manager.init_app(app)
users = {'cnfync@163.com': {'pw': '123456'}}

ldappath = "ldap://spreadtrum.com"
baseDN = "DC=spreadtrum,DC=com"
ldapuser = "CN=3GPPSvc,OU=ServiceAccount,DC=spreadtrum,DC=com"
ldappass = "3GPP@1234"

ALLOWED_EXTENSIONS = set(['.xlsx','.xls'])


@app.route("/")
def index():
    current_user = flask_login.current_user.get_id()
    if not current_user:
        current_user = ""
    return render_template("ibug_home.html", uname = current_user)

@app.route("/Home")
def Home():
    current_user = flask_login.current_user.get_id()
    if not current_user:
        current_user = ""
    return render_template("ibug_home.html", uname = current_user)

@app.route("/Search")
def search():
    current_user = flask_login.current_user.get_id()
    if not current_user:
        current_user = ""
    return render_template("ibug_search.html", uname = current_user)

@app.route("/Setting")
def Setting():
    current_user = flask_login.current_user.get_id()
    if not current_user:
        current_user = ""
    return render_template("ibug_setting.html", uname = current_user)

@app.route("/Rank")
def Rank():
    current_user = flask_login.current_user.get_id()
    if not current_user:
        current_user = ""
    return render_template("ibug_rank.html", uname = current_user)

@app.route("/Help")
def Help():
    current_user = flask_login.current_user.get_id()
    if not current_user:
        current_user = ""
    return render_template("ibug_help.html", uname = current_user)

@app.route("/ibug/upload")
def ibug():
    id = request.args.get("pid","")
    print id
    current_user = flask_login.current_user.get_id()
    if not current_user:
        current_user = ""
    return render_template("ibug_upload.html", parrent_id = id)

@app.route("/ibug/init_upload", methods=['POST'])
def init_upload():
    current_user = flask_login.current_user.get_id()
    if not current_user:
        current_user = ""

    args = request.form['data']
    #print args
    return render_template("ibug_upload.html", parrent_id = args)

@app.route("/api/platform")
def get_platform():
    result = {"state": 200, "data": "", "message": ""}
    data = service.get_project_name()
    result["data"] = data

    return json.dumps(result)

@app.route("/api/Alluser")
def get_Alluser():
        result = {"state":400, "data":"", "message":""}
        try:
            Alluser = service.get_Alluser()
            result["state"] = 200
            result["data"] = Alluser
        except Exception,e:
            result["state"] = 500
            result["message"] = str(e)
            #self.log.error(str(e))
        return json.dumps(result)

@app.route("/api/Special_Test_list")
def get_Special_Test_list():
    result = {"state": 200, "data": "", "message": ""}
    data = service.get_Special_Test()
    result["data"] = data 
    return json.dumps(result)

@app.route("/api/bug_count")
def bug_count_handler():
    result = {"state": 400, "data": "", "message": ""}
    data = []

    #args = {"special_test_name":"test","offset":0,"limit":2,"status":"1"}
    status = request.args.get("status","")
    limit = request.args.get("limit","10")
    offset = request.args.get("offset","0")

    _t = {    "status":status,
                "limit":limit,
                 "offset":offset }

    args = {}
    for k,v in _t.items():
        if v:
            args[k] = v

    data,total = service.bug_count(args)

    return json.dumps({"total":total,"rows":data})


@app.route("/api/bug_count_for_email")
def bug_count_for_email_handler():
    result = {"state": 200, "data": "", "message": ""}
    data = []

    data = service.bug_count_for_email()
    result["data"] = data
    return json.dumps(result).encode("utf-8")



@app.route("/api/special_test_receipts")
def special_test_receipts_handler():
    result = {"state": 400, "data": "", "message": ""}
    data = []


    special_test_name = request.args.get("special_test_name","")
    creator = request.args.get("creator","")
    status = request.args.get("status","")
    limit = request.args.get("limit","10")
    offset = request.args.get("offset","0")

    _t = {
                "status":status,
                "creator":creator,
                "special_test_name":special_test_name,
                "status":status,
                "limit":limit,
                 "offset":offset }

    args = {}
    for k,v in _t.items():
        if v:
            args[k] = v

    data,total = service.get_special_test_receipts(args)
    return json.dumps({"total":total,"rows":data})


@app.route("/api/special_test_receipts_without_paging")
def special_test_receipts_without_paging_handler():
    result = {"state": 400, "data": "", "message": ""}
    data = []

    #args = {"special_test_name":"test","offset":0,"limit":2,"status":"1"}
    try:
        status = request.args.get("status","")
        args = { "status":status }

        data = service.get_special_test_receipts_without_paging(args)

        return json.dumps({"status":200, "data":data,"message":""})
    except Exception,e:
        app.logger.error(e)
        return json.dumps({"status":500, "data":"","message":str(e)})


@app.route("/api/search")
def search_bugs_info():
    result = {"state": 400, "data": "", "message": ""}
    data = []
    # raise ValueError("this is new bug")

    try:
            #args = request.form['data']
            #args = json.loads(args)
            #print args
            offset = request.args.get("offset","0")
            limit = request.args.get("limit","10")
            parents_id = request.args.get("parents_id","")
            author = request.args.get("author","")
            owner = request.args.get("owner","")
            parents_category = request.args.get("parents_category","")
            special_test_name = request.args.get("special_test_name","")
            is_solved = request.args.get("is_solved","")
            special_test_parents_project = request.args.get("special_test_parents_project","")
            project_start_time = request.args.get("project_start_time","")
            project_end_time = request.args.get("project_end_time","")

            args = dict(offset=offset, limit=limit, parents_id=parents_id, author=author, owner=owner,
                        parents_category=parents_category, special_test_name=special_test_name, is_solved=is_solved,
                        special_test_parents_project=special_test_parents_project, project_end_time=project_end_time,
                        project_start_time=project_start_time)
            print args
            print '----------------piioommmmmmmmm------------'
            data,total = service.search_bugs(args)
            result["state"]=200
            result["data"]=data
            return json.dumps({"total":total,"rows":data})

    except Exception,e:
        app.logger.error(e)
        return json.dumps({"status":500, "data":"","message":str(e)})


@app.route("/api/bugs_info")
def bugs_info_handler():
    result = {"state": 400, "data": "", "message": ""}
    data = []
    # raise ValueError("this is new bug")

    try:
            offset = request.args.get("offset","0")
            limit = request.args.get("limit","10")
            parents_id = request.args.get("parents_id","")
            author = request.args.get("author","")
            owner = request.args.get("owner","")
            is_solved = request.args.get("is_solved","")
            args = {"offset":offset,"limit":limit,"parents_id":parents_id,"author":author,"owner":owner,"is_solved":is_solved}

            
            data,total = service.get_bugs(args)
            result["state"]=200
            result["data"]=data
            return json.dumps({"total":total,"rows":data})

    except Exception,e:
        app.logger.error(e)
        return json.dumps({"status":500, "data":"","message":str(e)})


@flask_login.login_required
@app.route('/api/modify/special_test_receipt', methods=['POST'])
def api_modify_special_test_receipt_handler():
    result = {"state": 400, "data": "", "message": ""}
    data = []

    current_user = flask_login.current_user.get_id()
    if not current_user:
        result["message"] = "Please login first"
        return json.dumps(result)

    #args = {"special_test_name":"test_2","special_test_parents_project": "test_project_2","creator": "liang.han","status":"1"}
    new_id = 0
    try:
        args = request.form['data']
        args = json.loads(args)
         
        current_id = args.get("id")
        print args
        print current_id
        if not current_id:
            raise ValueError("current_id")

        #SpecialTestDataModel.check_property(args)
        domain_obj = SpecialTest(current_id)
        domain_obj.modify(args)
    except Exception,e:
        app.logger.error(e)
        return json.dumps({"status":500, "data":"","message":str(e)})

    return json.dumps({"status":200, "data":"","message":""})

@flask_login.login_required
@app.route('/api/modify/bug_info', methods=['POST'])
def api_modify_bug_info_handler():
    result = {"state": 400, "data": "", "message": ""}
    data = []

    current_user = flask_login.current_user.get_id()
    if not current_user:
        result["message"] = "Please login first"
        return json.dumps(result)

    #args = {"special_test_name":"test_2","special_test_parents_project": "test_project_2","creator": "liang.han","status":"1"}
    try:
        args = request.form['data']
        args = json.loads(args)
        
        current_id = args.get("id")
        if not current_id:
            raise ValueError("current_id")

        domain_obj = BugInfo()
        domain_obj.modify(args)
    except Exception,e:
        app.logger.error(e)
        return json.dumps({"status":500, "data":"","message":str(e)})

    return json.dumps({"status":200, "data":"","message":""})


@flask_login.login_required
@app.route('/api/special_test_receipt', methods=['POST'])
def api_create_special_test_receipt_handler():
    
    result = {"state": 400, "data": "", "message": ""}
    data = [] 
    current_user = flask_login.current_user.get_id()
    if not current_user:
        result["message"] = "Please login first"
        return json.dumps(result)
    
    #args = {"special_test_name":"test_2","special_test_parents_project": "test_project_2","creator": "liang.han","status":"1"}
    new_id = 0 
    try:
        
        args = request.form['data']
        
        args = json.loads(args)
        args["creator"] = current_user
        args["status"] = '1'
        
        new_id = SpecialTest.create(args)
    except Exception,e:
        app.logger.error(e)
        raise e
        return json.dumps({"status":500, "data":"","message":str(e)})

    return json.dumps({"status":200, "data":new_id,"message":""})

    
@flask_login.login_required
@app.route('/Home/bug_into', methods=['POST'])
def api_append_bug_into_special_test_receipt_handler():
    import sys
    reload(sys)
    sys.setdefaultencoding("utf-8")

    result = {"state": 400, "data": "", "message": ""}
    data = []

    current_user = flask_login.current_user.get_id()
    if not current_user:
        result["message"] = "Please login first"
        return json.dumps(result)

    #args = {"special_test_name":"test_2","special_test_parents_project": "test_project_2","creator": "liang.han","status":"1"}
    new_id = 0
    try:
        
        args = request.form['data']
        args = json.loads(args)
        args["author"] = current_user
         
        #BugInfoDataModel.check_property(args)
        #print json.dumps(args)
        #data_model = BugInfoDataModel.deserialize(args)
        new_id = SpecialTest.append_new_bug(args)
        new_bug = service.get_bug_by_id(new_id)._dict()

        special_test_name = new_bug.get("special_test_name","")
        bug_description = new_bug.get("bug_description","")
        owner = new_bug.get("owner","")
        Subject = " 【专项测试：%s】 %s  问题已经创建，请及时处理。" % (special_test_name, bug_description)

        content = build_create_bug_info_content_html(new_bug)
        #send(owner,"","", Subject.encode('utf-8'), content.encode('utf-8'))

    except Exception,e:
        app.logger.error(e)
        return json.dumps({"status":500, "data":"","message":str(e)})

    return json.dumps({"status":200, "data":new_id,"message":""})


@flask_login.login_required
@app.route('/api/delete/bug_into', methods=['POST'])
def api_delete_bug_handler():
    result = {"state": 400, "data": "", "message": ""}
    old_bug_id = 0

    current_user = flask_login.current_user.get_id()
    if not current_user:
        result["message"] = "Please login first"
        return json.dumps(result)

    try:
        print 'rrrrrrrrrrrr============='
        _id = request.form['id']

        print _id
        old_bug_id = service.delete_bug_by_id(_id)

    except Exception,e:
        app.logger.error(e)
        return json.dumps({"status":500, "data":"","message":str(e)})

    return json.dumps({"status":200, "data":old_bug_id,"message":""})


@app.route('/api/inport_bug_info', methods=['POST','GET'])
def inport_bug_info():
    print request.method
    if request.method == "GET":
        return '''
                        <!doctype html>
                        <title>Upload new File</title>
                        <h1>Upload new File</h1>
                        <form action="/api/inport_bug_info" method=post enctype=multipart/form-data>
                          <p><input type=file name=file><input type=hidden name=parents_id value=20>
                             <input type=submit value=Upload>
                        </form>
                        '''

    file = request.files['file']
    
    parents_id = request.form['parents_id']
    
    old_filename, file_extension = os.path.splitext(file.filename)

    filename = "bugs_%s" % int(time.time()) + file_extension
    file_path = os.path.join('upload_folder', filename)
    data = []

    if not parents_id:
        result = {"state": 400, "data": "", "message": "need parents_id"}
        return json.dumps(result)

    if file_extension in ALLOWED_EXTENSIONS:
        file.save(file_path)
    else:
        result = {"state": 400, "data": "", "message": "need excel file"}
        #return json.dumps(result)
        return '''
                        <!doctype html>
                        <title>Upload new File</title>
                        <h1>Error!</h1>

                        '''
    #http://docs.jinkan.org/docs/flask/patterns/fileuploads.html
    excel_list = service.convert_excel(file_path = file_path)
    data = service.add_from_excel(excel_list,parents_id)
    #return json.dumps({"status":200, "data":data,"message":""})
    return '''
                        <!doctype html>
                        <title>Upload new File</title>
                        <h1>Success!</h1>

                        '''
    
    

 
def allowed_file(filename):
    return '.' in filename and  filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

#############################################
##   logging
#############################################
class User(flask_login.UserMixin):
    pass


@login_manager.user_loader
def user_loader(id):
    # if id not in users:
    #     return

    user = User()
    user.id = id
    return user


def login_validate(username,password):
  try:
      con = ldap.initialize(ldappath)
      con.set_option(ldap.OPT_REFERRALS, 0)
      con.simple_bind_s(ldapuser,ldappass)
      ad_username = username.replace("."," ")

      ad_logined_user = con.search_s( baseDN, ldap.SCOPE_SUBTREE, '(cn='+ad_username+')', ['mobile','givenName','msRTCSIP-PrimaryUserAddress'] )

      uid = ad_logined_user[0][0]
      con.simple_bind_s(uid,password)

      return True
  except Exception,e:
      return False


@app.route('/login', methods=['POST'])
def login():
    try:
        name = request.form['name']
        if login_validate(name, request.form['pw']):
            user = User()
            user.id = name
            print user.id
            flask_login.login_user(user)
            return json.dumps({"status":200,"data":"","message":"login success!"})
        else:
            return json.dumps({"status":400,"data":"","message":"username or password error!"})
            #return redirect(url_for('protected'))
    except Exception,e:
        app.logger.error(e)
        return json.dumps({"status":400,"data":"","message":"username or password error!"+str(e)})


@app.route('/logout')
def logout():
    flask_login.logout_user()
    return json.dumps({"status":200, "data":"", "message":"logout success!"})


if __name__ == "__main__":
    app.debug = True

    if app.debug is not True:
        import logging
        from logging.handlers import RotatingFileHandler
        file_handler = RotatingFileHandler('python.log', maxBytes=1024 * 1024 * 100, backupCount=20)
        file_handler.setLevel(logging.ERROR)
        app.logger.setLevel(logging.ERROR)
        app.logger.addHandler(file_handler)

    app.run(host='0.0.0.0',port=5000)
    #WSGIServer(app, bindAddress=('0.0.0.0', 8000)).run()
