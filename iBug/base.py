#coding:utf-8
import time
import sys
reload(sys)
sys.setdefaultencoding('utf8')


class SpecialTestDataModel(object):
    def __init__(self):
        self._id = None
        self._special_test_name = None       #'专项测试名称'
        self._special_test_parents_project = None     # '专项所属项目'
        self._special_test_pm = None    #'PM'
        self._special_test_cc_list = None     #'CC List',
        self._research_coding_developer = None         #'集成测试开发人',
        self._integration_testing_developer = None         #'集成测试开发人',
        self._coding_developer = None         #'研发代码开发人',
        self._case_number_prefix = None         #'CASE编号前缀',
        self._unit_test_case_amount = None         #'单元测试CASE数',
        self._integration_testing_case_amount = None          #'集成测试CASE数',
        self._coding_row = None          # '研发代码行',
        self._starting_time = None          # '专项开始时间',
        self._intend_end_time = None          #'专项计划完成时间',
        self._creator = None          #'创建人',
        self._status = None          # '状态',

    #############################################
    ##   GET Property
    #############################################
    @property
    def id(self):
        return self._id

    @property
    def special_test_name(self):
        return self._special_test_name

    @property
    def special_test_parents_project(self):
        return self._special_test_parents_project

    @property
    def special_test_pm(self):
        return self._special_test_pm

    @property
    def special_test_cc_list(self):
        return self._special_test_cc_list

    @property
    def research_coding_developer(self):
        return self._research_coding_developer

    @property
    def integration_testing_developer(self):
        return self._integration_testing_developer

    @property
    def coding_developer(self):
        return self._coding_developer

    @property
    def case_number_prefix(self):
        return self._case_number_prefix

    @property
    def unit_test_case_amount(self):
        return self._unit_test_case_amount

    @property
    def integration_testing_case_amount(self):
        return self._integration_testing_case_amount

    @property
    def coding_row(self):
        return self._coding_row

    @property
    def starting_time(self):
        return self._starting_time

    @property
    def intend_end_time(self):
        return self._intend_end_time

    @property
    def creator(self):
        return self._creator

    @property
    def status(self):
        return self._status


    #############################################
    ##   SET Property
    #############################################
    @id.setter
    def id(self,value):
        self._id = value

    @special_test_name.setter
    def special_test_name(self,value):
        if not value :
            raise ValueError("special_test_name")
        self._special_test_name = value

    @special_test_parents_project.setter
    def special_test_parents_project(self,value):
        if not value :
            raise ValueError("special_test_parents_project")
        self._special_test_parents_project = value

    @special_test_pm.setter
    def special_test_pm(self,value):
        self._special_test_pm = value

    @special_test_cc_list.setter
    def special_test_cc_list(self,value):
        self._special_test_cc_list = value

    @research_coding_developer.setter
    def research_coding_developer(self,value):
        self._research_coding_developer = value

    @integration_testing_developer.setter
    def integration_testing_developer(self,value):
        self._integration_testing_developer = value

    @coding_developer.setter
    def coding_developer(self,value):
        self._coding_developer = value

    @case_number_prefix.setter
    def case_number_prefix(self,value):
        self._case_number_prefix = value

    @unit_test_case_amount.setter
    def unit_test_case_amount(self,value):
        self._unit_test_case_amount = value

    @integration_testing_case_amount.setter
    def integration_testing_case_amount(self,value):
        self._integration_testing_case_amount = value

    @coding_row.setter
    def coding_row(self,value):
        self._coding_row = value

    @starting_time.setter
    def starting_time(self,value):
        self._starting_time = value

    @intend_end_time.setter
    def intend_end_time(self,value):
        self._intend_end_time = value

    @creator.setter
    def creator(self,value):
        self._creator = value

    @status.setter
    def status(self,value):
        self._status = value


    #############################################
    ##   Uitilty
    #############################################
    @staticmethod
    def deserialize(data_model):
        _self = SpecialTestDataModel()
        keys = [ k for k,v in SpecialTestDataModel.__dict__.iteritems() if (type(v) is property) ]
        for k in keys:
            setattr(_self,k,data_model.get(k,""))
        return _self

    def serialize(self):
        json_str = [ (k,str(getattr(self, k))) for k,v in SpecialTestDataModel.__dict__.iteritems() if (type(v) is property) and \
        (not getattr(self, k) == None )  and (not getattr(self, k) == "" ) ]
        return dict(json_str)

    @staticmethod
    def check_property(data_model):
         
        keys = SpecialTestDataModel.__dict__.keys()
        for k in data_model.keys():
            if k == "offset":
                continue
            if k == "limit":
                continue
            if k not in keys:
                raise AttributeError(k)


class BugInfoDataModel(object):
    def __init__(self):
        self._id = None
        self._case_number  = None
        self._author = None
        self._create_time = int(time.time())
        self._bug_description = None
        self._parents_category = None
        self._owner = None
        self._is_solved = None
        self._bug_id = None
        self._remark = None
        self._parents_id = None


    #############################################
    ##   GET Property
    #############################################
    @property
    def id(self):
        return self._id

    @property
    def case_number(self):
        return self._case_number

    @property
    def author(self):
        return self._author

    @property
    def create_time(self):
        return self._create_time


    @property
    def bug_description(self):
        return self._bug_description

    @property
    def parents_category(self):
        return self._parents_category

    @property
    def owner(self):
        return self._owner

    @property
    def is_solved(self):
        return self._is_solved

    @property
    def bug_id(self):
        return self._bug_id

    @property
    def remark(self):
        return self._remark

    @property
    def parents_id(self):
        return self._parents_id

    #############################################
    ##   SET Property
    #############################################

    @id.setter
    def id(self,value):
        self._id = value

    @case_number.setter
    def case_number(self,value):
        self._case_number = value

    @create_time.setter
    def create_time(self,value):
        pass

    @author.setter
    def author(self,value):
        if not value :
            raise ValueError("author")
        self._author = value


    @bug_description.setter
    def bug_description(self,value):
        if not value :
            raise ValueError("bug_description")

        self._bug_description = value

    @parents_category.setter
    def parents_category(self,value):
        if not value :
            raise ValueError("parents_category")

        self._parents_category = value

    @owner.setter
    def owner(self,value):
        if not value :
            raise ValueError("owner")

        self._owner = value

    @is_solved.setter
    def is_solved(self,value):
        if not value :
            raise ValueError("is_solved")

        self._is_solved = value

    @bug_id.setter
    def bug_id(self,value):
        self._bug_id = value

    @remark.setter
    def remark(self,value):
        self._remark = value

    @parents_id.setter
    def parents_id(self,value):
        if not value :
            raise ValueError("parents_id")
        self._parents_id = value

    #############################################
    ##   Uitilty
    #############################################
    @staticmethod
    def deserialize(data_model):
        _self = BugInfoDataModel()
        keys = [ k for k,v in BugInfoDataModel.__dict__.iteritems() if (type(v) is property) ]
        for k in keys:
            setattr(_self,k,str(data_model.get(k,"")))
        return _self

    def serialize(self):
        json_str = [ (k,str(getattr(self, k))) for k,v in BugInfoDataModel.__dict__.iteritems() if (type(v) is property) and \
        (not getattr(self, k) == None )  and (not getattr(self, k) == "" ) ]
        return dict(json_str)

    @staticmethod
    def check_property(data_model):
        keys = BugInfoDataModel.__dict__.keys()
        for k in data_model.keys():
            if k == "offset":
                continue
            if k == "limit":
                continue
            if k not in keys:
                raise AttributeError(k)

