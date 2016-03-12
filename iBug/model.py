#coding: utf-8
import json
import datetime
import time

import dal_proxy as dal


class SpecialTest(object):

    def __init__(self,id):
        self.id = id
        self.dao = dal.SpecialTestDAL()

    @staticmethod
    def create(data_model):
        dao = dal.SpecialTestDAL()
        return dao.add(data_model)

    @staticmethod
    def append_new_bug(data_model):
        dao = dal.BugInfoDAL()
        return dao.add(data_model)

    def get(self):
        return self.dao.get(self.id)

    def modify(self, data_model):
        return self.dao.modify(data_model)


class BugInfo(object):
    def modify(self, data_model):
        dao = dal.BugInfoDAL()
        return dao.modify(data_model)
















