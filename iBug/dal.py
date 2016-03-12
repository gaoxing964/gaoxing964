#coding: utf-8
import time
import MySQLdb
import MySQLdb.cursors
# from DBUtils.PooledDB import PooledDB

# pool = PooledDB(MySQLdb,5,host = '10.1.151.44',user = 'root',passwd = 'root', db='ibug', cursorclass=MySQLdb.cursors.DictCursor,connect_timeout=10,charset='utf8', init_command='SET NAMES UTF8')


class SpecialTestDAL(object):

    def get(self, _id):
        conn = get_connection()
        cursor = conn.cursor()

        sql = '''select * from sprd_ibug_special_test_receipt  where id = %s   '''
        cursor.execute(sql ,(_id,))
        result = cursor.fetchone()

        conn.close()
        return result

    def get_by_condition(self , _template, _agrs ,condition ):
        conn = get_connection()
        cursor = conn.cursor()
        offset = condition.get("offset","")
        limit = condition.get("limit","")

        sql = '''select SQL_CALC_FOUND_ROWS * from sprd_ibug_special_test_receipt %s order by id desc '''  % (_template , )

        if offset:
            sql = '''select SQL_CALC_FOUND_ROWS * from sprd_ibug_special_test_receipt %s order by id desc  limit %s , %s  '''  \
                    % (_template , int(offset),int(limit))
        # print sql % tuple(_agrs)

        cursor.execute(sql ,tuple(_agrs))
        result = cursor.fetchall()

        page_sql="select FOUND_ROWS() allcount "
        cursor.execute(page_sql)
        total = cursor.fetchone()["allcount"]

        conn.close()

        return result,total


    def add(self, data_model):
        dict_obj = data_model.serialize()
        fields_list = dict_obj.keys()
        values_list = dict_obj.values()
        #print fields_list,values_list
        targs = ["%s" for t in range(len(fields_list))]
        targs = ",".join(targs)

        conn = get_connection()
        cursor = conn.cursor()
        sql = '''insert into sprd_ibug_special_test_receipt  (%s)  values (%s)''' % (",".join(fields_list),targs)

        cursor.execute(sql ,tuple(values_list))
        conn.commit()
        result = cursor.lastrowid
        conn.close()
        return result


    def modify(self,data_model):
        conn = get_connection()
        cursor = conn.cursor()


        _id = data_model["id"]
        del data_model["id"]

        sets = []
        values = []
        for key in data_model.keys():
            if  data_model[key] =="":
                continue
            sets.append("%s = %%s" % key)
            values.append(data_model[key])
        _s = ', '.join(sets)

        sql = "UPDATE  sprd_ibug_special_test_receipt  SET %s WHERE  id = %s" % ( _s, _id,)

        #print sql %  tuple(values)

        result = cursor.execute(sql, tuple(values))
        cursor.close()
        conn.commit()
        conn.close()

        return result
        
        
    def get_project_name(self):
        conn = get_connection_175()
        cursor = conn.cursor()
        sql = 'SELECT id , PLATFORM_ID FROM sprd_ispt_m_platform'
        cursor.execute(sql)
        project_name =cursor.fetchall()

        cursor.close()
        conn.close()

        return [ p["PLATFORM_ID"] for p in project_name]

        
class BugInfoDAL(object):
    def add(self, data_model):
        dict_obj = data_model.serialize()
        fields_list = dict_obj.keys()
        values_list = dict_obj.values()
        #print fields_list,values_list
        targs = ["%s" for t in range(len(fields_list))]
        targs = ",".join(targs)

        conn = get_connection()
        cursor = conn.cursor()
        sql = '''insert into sprd_ibug_bug_info  (%s)  values (%s)''' % (",".join(fields_list),targs)

        cursor.execute(sql ,tuple(values_list))
        conn.commit()
        result = cursor.lastrowid
        conn.close()
        return result

    def get_by_condition(self , _template, _agrs ,condition ):
        conn = get_connection()
        cursor = conn.cursor()
        offset = condition.get("offset",0)
        limit = condition.get("limit",10)

        sql = '''select SQL_CALC_FOUND_ROWS *   from sprd_ibug_bug_info %s order by id desc  limit %s , %s  '''  \
                % (_template , int(offset),int(limit))
        print sql % tuple(_agrs)

        cursor.execute(sql ,tuple(_agrs))
        result = cursor.fetchall()

        page_sql="select FOUND_ROWS() allcount "
        cursor.execute(page_sql)
        total = cursor.fetchone()["allcount"]

        conn.close()

        return result,total


def get_connection():
    # return pool.connection()
    return MySQLdb.connect(host = '10.1.151.44',user = 'root',passwd = 'root', db='ibug', cursorclass=MySQLdb.cursors.DictCursor,connect_timeout=10,charset='utf8', init_command='SET NAMES UTF8')
    #return MySQLdb.connect(host = 'localhost',user = 'root',passwd = 'luoyong0202', db='voting', cursorclass=MySQLdb.cursors.DictCursor,connect_timeout=10,charset='utf8', init_command='SET NAMES UTF8')

def get_connection_175():
    #return pool.connection()
    return MySQLdb.connect(host = '10.0.0.175',user = 'iadmin',passwd = 'itask#ADMIN89', db='isupport', cursorclass=MySQLdb.cursors.DictCursor,connect_timeout=10,charset='utf8', init_command='SET NAMES UTF8')
