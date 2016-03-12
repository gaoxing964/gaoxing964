#coding: utf-8
import json
import time
import MySQLdb
from sqlalchemy import create_engine, func ,desc, or_
from sqlalchemy.orm import sessionmaker, relationship

from models import SpecialTestReceipt, BugInfo


engine = create_engine('mysql://iQuser:IQ$User55%@localhost/debug?charset=utf8', echo=True)
Session = sessionmaker(bind=engine)


class SpecialTestDAL(object):


    def get(self, _id):
        session = Session()
        return session.query(SpecialTestReceipt).filter_by(id=_id).first()

    def delete(self, _id):
        session = Session()
        obj = session.query(SpecialTestReceipt).filter_by(id=_id).first()
        session.delete(obj)
        session.commit()
        return _id


    def open_project(self):
        session = Session()
        all_open_project = session.query(SpecialTestReceipt).filter_by(status=1).all()
        return [project.id for project in all_open_project]


    def get_by_condition(self, condition ):
        offset = condition.get("offset","0")
        limit = condition.get("limit","10")
        special_test_name = condition.get("special_test_name","")

        del condition["limit"]
        del condition["offset"]

        if special_test_name:
            del condition["special_test_name"]

        filters = {}
        for key, val in condition.items():
            if val:
                filters[key] = val

        session = Session()
        q = session.query(SpecialTestReceipt).filter_by(**condition).order_by(desc(SpecialTestReceipt.id))
        if special_test_name:
            q = q.filter(SpecialTestReceipt.special_test_name.like('%' + special_test_name + '%'))

        number = q.count()

        result = [row._dict() for row in q.offset(offset).limit(limit).all()]
        session.close()

        return result, number


    def bug_count(self, condition ):
        offset = condition.get("offset","0")
        limit = condition.get("limit","10")

        del condition["limit"]
        del condition["offset"]

        filters = {}
        for key, val in condition.items():
            if val:
                filters[key] = val

        session = Session()
        q = session.query(SpecialTestReceipt).filter_by(**condition).order_by(desc(SpecialTestReceipt.id)).filter_by(status=1)
        number = q.count()

        _result = [row._dict() for row in q.offset(offset).limit(limit).all()]
        parents_ids = [obj["id"] for obj in _result]
        print parents_ids

        q = session.query(BugInfo, func.count(BugInfo.parents_id)).filter(BugInfo.parents_id.in_(parents_ids)).group_by(BugInfo.parents_id)
        all_bugs = q.all()
        print all_bugs

        q = session.query(BugInfo, func.count(BugInfo.parents_id)).filter(BugInfo.is_solved==0).filter(BugInfo.parents_id.in_(parents_ids)).group_by(BugInfo.parents_id)
        open_bugs = q.all()

        result = []
        for item in _result:
            item["current_all_bugs"] = 0
            item["current_open_bugs"] = 0

            current_all_bugs = [ count_result[1] for  count_result in all_bugs if count_result[0].parents_id == item["id"]]
            current_open_bugs = [ count_result[1] for  count_result in open_bugs if count_result[0].parents_id == item["id"]]

            if len(current_all_bugs) > 0:
                item["current_all_bugs"] = current_all_bugs[0]

            if len(current_open_bugs) > 0:
                item["current_open_bugs"] = current_open_bugs[0]

            result.append(item)
        session.close()

        return result, number


    def bug_count_for_email(self):

        session = Session()
        q = session.query(SpecialTestReceipt).order_by(desc(SpecialTestReceipt.id)).filter_by(status=1)

        _result = [row._dict() for row in q.all()]
        parents_ids = [obj["id"] for obj in _result]
        print parents_ids

        q = session.query(BugInfo, func.count(BugInfo.parents_id)).filter(BugInfo.parents_id.in_(parents_ids)).group_by(BugInfo.parents_id)
        all_bugs = q.all()
        print all_bugs

        result = []
        for item in _result:
            _t = {}
            _t["current_all_bugs"] = 0
            _t["current_open_bugs"] = None

            current_all_bugs = [ count_result[1] for  count_result in all_bugs if count_result[0].parents_id == item["id"]]

            q = session.query(BugInfo).filter(BugInfo.is_solved==0).filter(BugInfo.parents_id == item["id"] )
            current_open_bugs = q.count()
            open_bugs = [ dict(owner = row.owner, bug_description = row.bug_description) for row in q.all()]
            print open_bugs

            if len(current_all_bugs) > 0:
                _t["current_all_bugs"] = current_all_bugs[0]


            _t["current_open_bugs"] = open_bugs
            _t["special_test_name"] = item["special_test_name"]
            _t["special_test_pm"] = item["special_test_pm"]
            _t["special_test_cc_list"] = item["special_test_cc_list"]

            result.append(_t)
        session.close()

        return result


    def get_by_condition_without_paging(self, condition ):

        filters = {}
        for key, val in condition.items():
            if val:
                filters[key] = val

        session = Session()
        q = session.query(SpecialTestReceipt).filter_by(**filters).order_by(desc(SpecialTestReceipt.id))

        result = [row._dict() for row in q.all()]
        session.close()

        return result


    def add(self, data_model):
        obj = SpecialTestReceipt(
            special_test_name=data_model.get("special_test_name",None),
            special_test_parents_project=data_model.get("special_test_parents_project",None),
            special_test_pm=data_model.get("special_test_pm",None),
            special_test_cc_list=data_model.get("special_test_cc_list",None),
            research_coding_developer=data_model.get("research_coding_developer",None),
            integration_testing_developer=data_model.get("integration_testing_developer",None),
            coding_developer=data_model.get("coding_developer",None),
            case_number_prefix=data_model.get("case_number_prefix",None),
            unit_test_case_amount=data_model.get("unit_test_case_amount",None),
            integration_testing_case_amount=data_model.get("integration_testing_case_amount",None),
            coding_row=data_model.get("coding_row",None),
            starting_time=data_model.get("starting_time",None),
            intend_end_time=data_model.get("intend_end_time",None),
            creator=data_model.get("creator",None),
            status=1,
            create_time=int(time.time())
            )

        session = Session()
        session.add(obj)
        session.commit()

        result = obj.id
        session.close()

        return result



    def modify(self,data_model):
        _id = data_model["id"]
        del data_model["id"]

        session = Session()
        obj = session.query(SpecialTestReceipt).filter_by(id=_id).first()

        for key, val in data_model.items():
            if val:
                setattr(obj, key, val)

        bug_objs = session.query(BugInfo).filter_by(parents_id=_id).all()
        bug_objs.special_test_name = data_model["special_test_name"]
        bug_objs.special_test_parents_project = data_model["special_test_parents_project"]

        session.commit()
        session.close()

        return


    def get_project_name(self):
        conn = get_connection_175()
        cursor = conn.cursor()
        sql = 'SELECT id , PLATFORM_ID FROM sprd_ispt_m_platform'
        cursor.execute(sql)
        project_name =cursor.fetchall()

        cursor.close()
        conn.close()

        return [ p["PLATFORM_ID"] for p in project_name]

    def get_Alluser(self):
        import urllib2
        import json
        print 'rrrrrrr'
        response = urllib2.urlopen('http://imanage.spreadtrum.com/imanage/home/pm?act=GetUsersByDep1&depName=Comm%20sys')

        result = response.read()

        result = json.loads(result, encoding="utf-8")
        print 'aaaaaaaa'

        alluser = ''.join(result["data"])
        re_user = str(alluser).replace("'","").replace(r"\n","").replace(r" ",".").lower()
        final_result = re_user.split(',')
        final_result.sort()
        return final_result


class BugInfoDAL(object):


    def add(self, data_model):
        print '---------yyyyyyyyyyyyyyyyyyyy------'
        print data_model

        parents_id = data_model["parents_id"]
        print parents_id
        special_test_obj = SpecialTestDAL()
        _current = special_test_obj.get(parents_id)
        print _current
        obj = BugInfo(
            parents_id=parents_id,
            special_test_name= _current.special_test_name,
            special_test_parents_project= _current.special_test_parents_project,
            #special_test_pm = _current.special_test_pm,

            case_number=data_model.get("case_number",None),
            author=data_model.get("author",None),
            create_time=int(time.time()),
            bug_description=data_model.get("bug_description",None),
            parents_category=data_model.get("parents_category",None),
            owner=data_model.get("owner",None),
            is_solved=data_model.get("is_solved",None),
            priority=data_model.get("priority",None),
            bug_id=data_model.get("bug_id",None),
            remark=data_model.get("remark",None)
            )

        session = Session()
        session.add(obj)
        session.commit()

        result = obj.id
        session.close()

        return result


    def add_from_excel(self, data_list,parents_id):

        special_test_obj = SpecialTestDAL()
        _current = special_test_obj.get(parents_id)
        print _current
        result = []
        for data_model in data_list:
            obj = BugInfo(
                parents_id=parents_id,
                special_test_name= _current.special_test_name,
                special_test_parents_project= _current.special_test_parents_project,
                #special_test_pm = _current.special_test_pm,

                case_number=data_model.get("case_number",None),
                author=data_model.get("author",None),
                create_time=int(time.time()),
                bug_description=data_model.get("bug_description",None),
                parents_category=data_model.get("parents_category",None),
                owner=data_model.get("owner",None),
                is_solved=data_model.get("is_solved",None),
                priority=data_model.get("priority",None),
                bug_id=data_model.get("bug_id",None),
                remark=data_model.get("remark",None)
                )

            session = Session()
            session.add(obj)
            session.commit()

            print data_model

            result.append(obj.id)
        session.close()

        return result

    def get(self, id):
        session = Session()
        obj = session.query(BugInfo).filter_by(id=id).first()
        return obj


    def delete(self, id):
        session = Session()
        obj = session.query(BugInfo).filter_by(id=id).first()
        session.delete(obj)
        session.commit()
        return id

    def modify(self,data_model):
        _id = data_model["id"]
        del data_model["id"]

        session = Session()
        obj = session.query(BugInfo).filter_by(id=_id).first()

        for key, val in data_model.items():
            if val:
                setattr(obj, key, val)

        session.commit()
        session.close()

        return 1


    def get_by_parents_ids(self, condition, parents_ids):
        offset = condition.get("offset","999999")
        limit = condition.get("limit","0")

        del condition["offset"]
        del condition["limit"]

        session = Session()
        q = session.query(BugInfo).filter(BugInfo.parents_id.in_(parents_ids))
        number = q.count()

        result = [str(row) for row in q.offset(offset).limit(limit).all()]

        session.close()

        return result, number


    def search(self, condition ):
        offset = condition.get("offset","9999999")
        limit = condition.get("limit","0")
        #condition["project_start_time"] = "1454573689"
        #condition["project_end_time"] = "1454306854"

        #for search
        project_start_time = condition.get("project_start_time","")
        project_end_time = condition.get("project_end_time","")

        del condition["offset"]
        del condition["limit"]

        filters = {}
        for key, val in condition.items():
            if val:
                print "info:   %s=%s"  % (key,val)
                filters[key] = val

        session = Session()
        q = session.query(BugInfo)

        if project_start_time:
            q = q.filter(BugInfo.create_time > project_start_time)
            del filters["project_start_time"]

        if project_end_time:
            q = q.filter(BugInfo.create_time < project_end_time)
            del filters["project_end_time"]

        special_test_obj = SpecialTestDAL()
        open_project_ids = special_test_obj.open_project()

        q = q.filter_by(**filters).order_by(desc(BugInfo.id))
        number = q.count()

        result = [ row._dict() for row in q.offset(offset).limit(limit).all()]

        session.close()
        return result, number


    def get_by_condition(self, condition ):
        offset = condition.get("offset","9999999")
        limit = condition.get("limit","0")

        #for search
        owner = condition.get("owner","")

        del condition["offset"]
        del condition["limit"]

        filters = {}
        for key, val in condition.items():
            if val:
                print "info:   %s=%s"  % (key,val)
                filters[key] = val

        session = Session()
        q = session.query(BugInfo)

        if owner:
            del filters["owner"]
            q = q.filter(or_(BugInfo.owner.like('%,' + owner + '%'), BugInfo.owner.like('%' + owner + ',%'), BugInfo.owner ==owner))


        special_test_obj = SpecialTestDAL()
        open_project_ids = special_test_obj.open_project()

        q = q.filter_by(**filters).order_by(desc(BugInfo.id)).filter(BugInfo.parents_id.in_(open_project_ids))



        number = q.count()

        result = [ row._dict() for row in q.offset(offset).limit(limit).all()]

        session.close()
        return result, number


def get_connection_175():
    #return pool.connection()
    return MySQLdb.connect(host = '10.0.0.175',user = 'iadmin',passwd = 'itask#ADMIN89', db='isupport', cursorclass=MySQLdb.cursors.DictCursor,connect_timeout=10,charset='utf8', init_command='SET NAMES UTF8')


if __name__ == "__main__":
    obj = SpecialTestDAL()
    #print obj.get_by_condition_without_paging(dict(status="1",special_test_name="kk"))

    #print obj.add(dict(special_test_name="ccddddkk",special_test_parents_project="testtt111"))
    #print obj.modify(dict(special_test_name="dddd",special_test_parents_project="34sdfsdf",id=146))


    obj = BugInfoDAL()
    # print obj.get_by_parents_ids(dict(offset=0,limit=20),[3,2])





