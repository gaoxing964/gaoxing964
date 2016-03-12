#coding:utf-8
import time
import json
import os,sys
import uuid
from flask import Flask, render_template, request, send_from_directory,redirect,url_for
from flask import make_response
import flask.ext.login as flask_login
from flup.server.fcgi import WSGIServer
from werkzeug import secure_filename
import redis
from flask.ext.cache import Cache

from base import *
from model import *
import service
app = Flask(__name__)
app.secret_key = '!QAZ@WSX#EDC$RFV'
login_manager = flask_login.LoginManager()
login_manager.init_app(app)
cache = Cache(config={'CACHE_TYPE': 'simple'})
r = redis.Redis(host='localhost', port=6379, db=0)

################################
##  web route handlers
################################
@app.route('/api/admin/voting', methods=['POST'])
@flask_login.login_required
def api_admin_voting():
    result = {"status":400}
    vote_theme = request.form['vote_theme']
    activity_description = request.form['activity_description']
    starting_time = request.form['starting_time']
    end_time = request.form['end_time']
    max_voter_votes_oneday = request.form['max_voter_votes_oneday']
    max_player_votes_oneday = request.form['max_player_votes_oneday']
    max_to_player_votes = request.form['max_to_player_votes']
    need_attention_weixin = request.form['need_attention_weixin']
    enable = request.form['enable']

    voting_rule = {
        "max_player_votes":max_player_votes_oneday,
        "max_voter_vote_to_player_votes":max_to_player_votes,
        "max_voter_votes":max_voter_votes_oneday,
        "need_attention_weixin":0
    }

    voting_rule = json.dumps(voting_rule)

    timeArray = time.strptime(starting_time, "%Y-%m-%d")
    starting_time = int(time.mktime(timeArray))

    timeArray = time.strptime(end_time, "%Y-%m-%d")
    end_time = int(time.mktime(timeArray))

    voting_model = Voting()
    new_id = voting_model.create(
                vote_theme = vote_theme,
                activity_description = activity_description,
                starting_time = starting_time,
                end_time = end_time,
                voting_rule = voting_rule,
                enable = enable
        )
    result = {"status":200,"data":new_id}
    return  json.dumps(result)

@app.route('/api/admin/player', methods=['POST'])
@flask_login.login_required
def api_admin_player():
    result = {"status":400}
    votingID = request.form['voting_id']
    player_name = request.form['player_name']
    # seted_offset_votes = request.form['seted_offset_votes']

    # if not seted_offset_votes:
    #     seted_offset_votes = 0

    admin = Administrator(id = 20)
    player = Player(player_name = player_name,seted_offset_votes = 0)

    new_id = admin.push_player_to_voting(votingID,player)
    return json.dumps({"status":200,"data":new_id})

@app.route('/api/admin/players/<votingID>')
@flask_login.login_required
def api_get_players(votingID):
    result = {"status":400}

    player_list =service.get_players_by_votingID(votingID)
    player_list.sort(key=lambda x: x["ordered"])

    return json.dumps({"status":200,"data":player_list})

@app.route('/api/admin/votings')
@flask_login.login_required
def api_get_votings():
    limit = request.args.get('limit', '10')
    offset = request.args.get('offset', '0')
    rows , total = service.get_voting_by_condition(offset = offset , limit = limit)
    result = {"rows": rows, "total":total}
    return json.dumps(result)

@app.route('/api/admin/delet_player/<player_id>')
@flask_login.login_required
def api_delete_player(player_id):

    result = service.delete_player(player_id)
    return json.dumps({"status":200,"data":result})

@app.route('/api/admin/delet_voting/<votingID>')
@flask_login.login_required
def api_delete_voting(votingID):

    result = service.delete_voting(votingID)
    return json.dumps({"status":200,"data":result})

@app.route("/admin/edit_voting/<votingID>")
@flask_login.login_required
def admin_edit_voting(votingID):
    voting =service.get_voting(votingID)
    voting_rule = voting["voting_rule"]
    voting_rule = json.loads(voting_rule)
    voting["max_voter_votes_oneday"] = voting_rule["max_voter_votes"]
    voting["max_player_votes_oneday"] = voting_rule["max_player_votes"]
    voting["max_voter_vote_to_player_votes"] = voting_rule["max_voter_vote_to_player_votes"]
    voting["starting_time"] = time.strftime("%Y-%m-%d ", time.localtime(voting["starting_time"]))
    voting["end_time"] = time.strftime("%Y-%m-%d ", time.localtime(voting["end_time"]))

    return render_template("admin/edit_voting.html" , voting = voting )

@app.route("/admin/add2/<votingID>")
@flask_login.login_required
def admin_add2(votingID):
    voting =service.get_voting(votingID)
    voting_header = "undefined"
    if voting["header"]:
        voting_header_file_name = repr(voting["header"]).split("\\")
        voting_header = voting_header_file_name[-1]

    voting_footer = "" if voting["footer"] == None else  voting["footer"]
    #player_list.sort(key=lambda x: x["ordered"])
    return render_template("admin/add2.html" , id = votingID , voting_header = voting_header  , voting_footer = voting_footer)

@app.route("/admin/upload_voting", methods=['POST','GET'])
@flask_login.login_required
def admin_upload_voting():
    if request.method == 'GET':
        return render_template("admin/upload_voting.html" )
    else:
        file = request.files['file']
        voting_id = request.form['voting_id']

        current_dir_name = os.path.dirname(os.path.abspath(__file__))
        static_dir_name = os.path.join(current_dir_name, "static","voting_images",voting_id)

        if not os.path.exists(static_dir_name):
            os.makedirs(static_dir_name)

        filename = secure_filename(file.filename)
        file_path = os.path.join(static_dir_name, filename)
        file.save(file_path)

        relatively_path = os.path.join( "static","voting_images",voting_id,filename)
        service.modify_voting(header=relatively_path,id=voting_id)
        return render_template("admin/uploaded.html" , filename=filename )

@app.route("/admin/voting/modify", methods=['POST'])
@flask_login.login_required
def admin_modify_voting():
    result = {"status":400}
    voting_id = request.form['voting_id']
    vote_theme = request.form['vote_theme']
    activity_description = request.form['activity_description']
    starting_time = request.form['starting_time']
    end_time = request.form['end_time']
    max_voter_votes_oneday = request.form['max_voter_votes_oneday']
    max_player_votes_oneday = request.form['max_player_votes_oneday']
    max_to_player_votes = request.form['max_to_player_votes']
    need_attention_weixin = request.form['need_attention_weixin']
    enable = request.form['enable']

    voting_rule = {
        "max_player_votes":max_player_votes_oneday,
        "max_voter_vote_to_player_votes":max_to_player_votes,
        "max_voter_votes":max_voter_votes_oneday,
        "need_attention_weixin":0
    }

    voting_rule = json.dumps(voting_rule)

    timeArray = time.strptime(starting_time, "%Y-%m-%d")
    starting_time = int(time.mktime(timeArray))

    timeArray = time.strptime(end_time, "%Y-%m-%d")
    end_time = int(time.mktime(timeArray))


    _t = service.modify_voting(id=voting_id,
                vote_theme = vote_theme,
                activity_description = activity_description,
                starting_time = starting_time,
                end_time = end_time,
                voting_rule = voting_rule,
                enable = enable)


    result = {"status":200,"data":_t}
    return json.dumps(result)

@app.route("/admin/voting/modify_footer", methods=['POST'])
@flask_login.login_required
def admin_modify_voting_footer():
    result = {"status":400}
    voting_id = request.form['voting_id']
    footer_message = request.form['footer_message']

    _t = service.modify_voting(id=voting_id,
                footer = footer_message)

    result = {"status":200,"data":_t}
    return json.dumps(result)

@app.route("/admin/upload_player", methods=['POST','GET'])
@flask_login.login_required
def admin_upload_player():
    if request.method == 'GET':
        return render_template("admin/upload_player.html" )
    else:
        file = request.files['file']
        voting_id = request.form['voting_id']
        player_id = request.form['player_id']

        current_dir_name = os.path.dirname(os.path.abspath(__file__))
        static_dir_name = os.path.join(current_dir_name, "static","voting_images",voting_id,player_id)

        if not os.path.exists(static_dir_name):
            os.makedirs(static_dir_name)

        filename = secure_filename(file.filename)
        file_path = os.path.join(static_dir_name, filename)
        file.save(file_path)

        relatively_path = os.path.join( "static","voting_images",voting_id,player_id,filename)
        service.modify_player(player_image=relatively_path,id=player_id)
        return render_template("admin/uploaded.html" , filename=filename )


@app.route("/api/admin/player/modify", methods=['POST'])
@flask_login.login_required
def admin_player_modify():
    result = {"status":400}
    # try:
    _id = request.form['id']
    player_details = request.form['player_details']
    player_name = request.form['player_name']
    order =  request.form['order']

    if player_details :
        _t = service.modify_player(id = _id,player_details= player_details)
    else :
        if order:
            order = int(order)
        _t = service.modify_player(id = _id,player_name= player_name,ordered = order)
    result = {"status":200,"message":_t}
    # except Exception ,e :
    #     result = {"status":500,"message":str(e)}

    return  json.dumps(result)

@login_manager.user_loader
def user_loader(id):
    user = User()
    user.id = id
    return user


class User(flask_login.UserMixin):
    pass

def login_validate(username,password):
  users = {"admin":"Ly19880202","user":"fjfhypm"}
  try:
      for u in users:
        if username == u and password == users[u]:
            return True

      return False
  except Exception,e:
      return False


@app.route('/login', methods=['POST','GET'])
def login():
    if request.method == 'GET':
        return render_template("admin/login.html" )
    else:
        name = request.form['name']
        if login_validate(name, request.form['pw']):
            user = User()
            user.id = name
            #print user.id
            flask_login.login_user(user)
            return redirect(url_for('admin_index'))
        else:
            return json.dumps({"status":400,"data":"","message":"username or password error!"})



@app.route('/logout')
@flask_login.login_required
def logout():
    flask_login.logout_user()
    return redirect(url_for('login'))



@app.route("/admin/index")
@flask_login.login_required
def admin_index():
    #print "at admin_index:"+"&"*30
    #print  flask_login.current_user.get_id()
    return render_template("admin/index.html" )

@app.route("/admin/index_v1")
@flask_login.login_required
def admin_index_v1():
    return render_template("admin/index_v1.html" )

@app.route("/admin/add")
@flask_login.login_required
def admin_add():
    return render_template("admin/add.html" )

@app.route("/admin/list")
@flask_login.login_required
def admin_list():
    return render_template("admin/list.html",voting_list = service.get_all_voting() )

@app.route("/admin/login")
def admin_login():
    return render_template("admin/login.html" )

@app.route("/admin/navlist")
@flask_login.login_required
def admin_navlist():
    return render_template("admin/navlist.html" )

@app.route("/admin/statistics")
@flask_login.login_required
def admin_statistics():
    return render_template("admin/statistics.html" )

@app.route("/admin/weixin")
@flask_login.login_required
def admin_weixin():
    return render_template("admin/weixin.html" )


################################
##  web route handlers
################################
@app.route("/")
def default():

    return __render(render_template("web/default.html" ))

@app.route("/index")
def index():
    #raise
    voting_list = []

    if r.get("get_all_voting"):
        voting_list = json.loads(r.get("get_all_voting"))
    else:
        _t = service.get_all_voting()
        for item in _t:
            if not (item["enable"] == 1):
                continue

            if not item["header"]:
                item["header"] = "static/web/images/1.jpg"

            voting_list.append(item)


    r.set("get_all_voting",json.dumps(voting_list))
    r.expire("get_all_voting",300)



    return __render(render_template("web/index.html"  , voting_list =voting_list , _t = str(time.time() )))

@app.route("/list/<votingID>")
def list_handler(votingID):
    #raise
    voting = None
    player_list = []

    # voting = service.get_voting(votingID)
    # if not voting["header"]:
    #     voting["header"] = "static/web/images/1.jpg"

    key = "get_voting:%s" % (votingID,)
    if r.get(key):
         print "info:get_voting"
         voting = json.loads(r.get(key))
    else:
        voting = service.get_voting(votingID)
        if not voting["header"]:
            voting["header"] = "static/web/images/1.jpg"

        r.set(key,json.dumps(voting))
        r.expire(key,300)


    _t = service.get_players_by_votingID(votingID)
    for item in _t:
        if not item["player_image"]:
            item["player_image"] = "static/web/images/1.jpg"

        player_list.append(item)


    player_list.sort(key=lambda x: x["ordered"])

    # key = "get_player_list:%s" % (votingID,)
    # if r.get(key):
    #      print "info:get_player_list"
    #      player_list = json.loads(r.get(key))
    # else:
    #     _t = service.get_players_by_votingID(votingID)
    #     for item in _t:
    #         if not item["player_image"]:
    #             item["player_image"] = "static/web/images/1.jpg"

    #         player_list.append(item)

    #     player_list.sort(key=lambda x: x["ordered"])
    #     r.set(key,json.dumps(player_list))
    #     r.expire(key,9)


    return __render(render_template("web/list.html", voting = voting, player_list = player_list))

def __render(render):
    resp = make_response(render)
    voterID = request.cookies.get('voterID')
    if not voterID:
        _id = uuid.uuid1()
        _expires = time.time() + 60*60*24*20
        resp.set_cookie('voterID', str(_id) ,expires=_expires)
    return resp


@app.route("/about/<playerID>")
def about_handler(playerID):
    player = None

    player = service.get_player(playerID)
    if not player["player_image"]:
        player["player_image"] = "static/web/images/1.jpg"

    # key = "get_player:%s" % (playerID,)
    # if r.get(key):
    #     print "info:get_player"
    #     player =  json.loads(r.get(key))
    # else:
    #     player = service.get_player(playerID)
    #     if not player["player_image"]:
    #         player["player_image"] = "static/web/images/1.jpg"

    #     r.set(key,json.dumps(player))
    #     r.expire(key,24)

    return __render(render_template("web/about.html" , player =player))


#@cache.cached(timeout=5000)
@app.route("/test/<playerID>")
def test_handler(playerID):
    player = None

    key = "get_player:%s" % (playerID,)
    if r.get(key):
        print "info:get_player"
        player =  json.loads(r.get(key))
    else:
        player = service.get_player(playerID)
        if not player["player_image"]:
            player["player_image"] = "static/web/images/1.jpg"

        r.set(key,json.dumps(player))
        r.expire(key,10)

    return json.dumps(player)


# @app.route("/test/<playerID>")
# def test_handler(playerID):
#     template = "<h3>500</h3>"
#     key = "template:%s" % ("test",)
#     if r.get(key):
#         print "info:template"
#         template =   r.get(key)
#     else:
#         template =   render_template("web/test.html")
#         r.set(key,template)
#         r.expire(key,4000)

#     return __render(template)

@app.route('/api/voting/all')
def get_all_voting():
    #raise
    return  json.dumps(service.get_all_voting())


@app.route('/vote', methods=['POST'])
def take_part_in():
    result = {"status":400}
    #print request.remote_addr

    voterID = request.cookies.get('voterID')
    if not voterID:
        result["message"] = "非法请求"
        return  json.dumps(result)

    weixin_id = request.form['weixin_id']
    player_id = request.form['player_id']

    player = None

    key = "get_player_object:%s" % (player_id,)
    if r.get(key):
        print "info:get_player_object"
        player =  json.loads(r.get(key))
    else:
        player = service.get_player_object(player_id)
        if not player:
            return  json.dumps(result)

        r.set(key,json.dumps(player))
        r.expire(key,12)

    voting_id = player["votingID"]

    voter = Voter(weixin_id)
    try:
        voter.take_part_in(voting_id=voting_id,player_id=player_id)
        result = {"status":200}
    except VoteLimitError ,e:
         result = {"status":500,"message":e.value}

    return  json.dumps(result)


if __name__ == "__main__":
    #app.debug = True
     # app.run()

    try:
        pid = os.fork()
        if pid > 0:
            sys.exit(0)
    except OSError:
        report( "unable to fork: %s" % sys.exc_info()[1])
        raise

    from werkzeug.contrib.fixers import ProxyFix
    app.wsgi_app = ProxyFix(app.wsgi_app)

    WSGIServer(app, bindAddress=('127.0.0.1', 8848)).run()




