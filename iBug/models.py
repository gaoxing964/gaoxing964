#!/usr/bin/env python
#-*- coding:utf-8 -*-
import json
import MySQLdb
from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

class SpecialTestReceipt(Base):
    __tablename__ = 'sprd_ibug_special_test_receipt'

    id = Column(Integer,primary_key = True)
    special_test_name = Column(String(200),nullable=False)
    special_test_parents_project = Column(String(100),nullable=False)
    special_test_pm = Column(String(100))
    special_test_cc_list = Column(String(500))
    research_coding_developer = Column(String(100))
    integration_testing_developer = Column(String(100))
    coding_developer = Column(String(100))
    case_number_prefix = Column(String(100))
    unit_test_case_amount = Column(Integer)
    integration_testing_case_amount = Column(Integer)
    coding_row = Column(Integer)
    starting_time = Column(Integer)
    intend_end_time = Column(Integer)
    creator = Column(String(50))
    status = Column(String(50))
    create_time = Column(Integer, nullable=False)

    def __repr__(self):
        return json.dumps(dict(
            id = self.id,
            special_test_name = self.special_test_name if self.special_test_name  else  "",
            special_test_parents_project = self.special_test_parents_project  if self.special_test_parents_project  else  "",
            special_test_pm = self.special_test_pm if self.special_test_pm  else  "",
            special_test_cc_list = self.special_test_cc_list if self.special_test_cc_list  else  "",
            research_coding_developer = self.research_coding_developer if self.research_coding_developer  else  "",
            integration_testing_developer = self.integration_testing_developer if self.integration_testing_developer  else  "",
            coding_developer = self.coding_developer if self.coding_developer  else  "",
            case_number_prefix = self.case_number_prefix if self.case_number_prefix  else  "",
            unit_test_case_amount = self.unit_test_case_amount if self.unit_test_case_amount  else  "",
            integration_testing_case_amount = self.integration_testing_case_amount if self.integration_testing_case_amount  else  "",
            coding_row =  self.coding_row if self.coding_row  else  "",
            starting_time = self.starting_time if self.starting_time  else  "",
            intend_end_time = self.intend_end_time if self.intend_end_time  else  "",
            creator = self.creator if self.creator  else  "",
            status = self.status if self.status  else  "",
            create_time = self.create_time if self.create_time  else  ""
            ))


    def _dict(self):
        return dict(
            id = self.id,
            special_test_name = self.special_test_name if self.special_test_name  else  "",
            special_test_parents_project = self.special_test_parents_project  if self.special_test_parents_project  else  "",
            special_test_pm = self.special_test_pm if self.special_test_pm  else  "",
            special_test_cc_list = self.special_test_cc_list if self.special_test_cc_list  else  "",
            research_coding_developer = self.research_coding_developer if self.research_coding_developer  else  "",
            integration_testing_developer = self.integration_testing_developer if self.integration_testing_developer  else  "",
            coding_developer = self.coding_developer if self.coding_developer  else  "",
            case_number_prefix = self.case_number_prefix if self.case_number_prefix  else  "",
            unit_test_case_amount = self.unit_test_case_amount if self.unit_test_case_amount  else  "",
            integration_testing_case_amount = self.integration_testing_case_amount if self.integration_testing_case_amount  else  "",
            coding_row =  self.coding_row if self.coding_row  else  "",
            starting_time = self.starting_time if self.starting_time  else  "",
            intend_end_time = self.intend_end_time if self.intend_end_time  else  "",
            creator = self.creator if self.creator  else  "",
            status = self.status if self.status  else  "",
            create_time = self.create_time if self.create_time  else  ""
            )


class BugInfo(Base):
    __tablename__ = 'sprd_ibug_bug_info'

    id = Column(Integer,primary_key = True)
    case_number = Column(String(100), nullable=False)
    author = Column(String(50), nullable=False)
    create_time = Column(Integer, nullable=False)
    bug_description = Column(Text, nullable=False)
    parents_category = Column(String(100), nullable=False)
    owner = Column(String(50), nullable=False)
    is_solved = Column(Integer, nullable=False)
    bug_id = Column(String(50), nullable=True)
    remark = Column(Text)
    priority = Column(String(4), nullable=True)

    special_test_name = Column(String(200),nullable=False)
    special_test_parents_project = Column(String(100),nullable=False)
    parents_id = Column(Integer, nullable=False)



    def __repr__(self):
        return json.dumps(dict(
            id = self.id,
            special_test_name = self.special_test_name if self.special_test_name  else  "",
            special_test_parents_project = self.special_test_parents_project if self.special_test_parents_project  else  "",
            parents_id = self.parents_id if self.parents_id  else  "",
            case_number = self.case_number if self.case_number  else  "",
            author = self.author if self.author  else  "",
            create_time = self.create_time if self.create_time  else  "",
            bug_description = self.bug_description if self.bug_description  else  "",
            parents_category = self.parents_category if self.parents_category  else  "",
            owner = self.owner if self.owner  else  "",
            is_solved = self.is_solved if self.is_solved  else  "",
            bug_id = self.bug_id if self.bug_id  else  "",
            remark = self.remark if self.remark  else  "",
            priority = self.priority if self.priority  else  ""
            ))


    def _dict(self):
        return dict(
            id = self.id,
            special_test_name = self.special_test_name if self.special_test_name  else  "",
            special_test_parents_project = self.special_test_parents_project if self.special_test_parents_project  else  "",
            parents_id = self.parents_id if self.parents_id  else  "",
            case_number = self.case_number if self.case_number  else  "",
            author = self.author if self.author  else  "",
            create_time = self.create_time if self.create_time  else  "",
            bug_description = self.bug_description if self.bug_description  else  "",
            parents_category = self.parents_category if self.parents_category  else  "",
            owner = self.owner if self.owner  else  "",
            is_solved = self.is_solved if self.is_solved  else  "",
            bug_id = self.bug_id if self.bug_id  else  "",
            remark = self.remark if self.remark  else  "",
            priority = self.priority if self.priority  else  ""
            )
