#coding: utf-8
import unittest
import json
from model import *
from base import *
import service

class TestSpecialTest(unittest.TestCase):


  def test_create_special_test_receipt(self):
      args = {"special_test_name":"test_2","special_test_parents_project": "test_project_2","creator": "liang.han","status":"1"}
      SpecialTestDataModel.check_property(args)
      data_model = SpecialTestDataModel.deserialize(args)

      id = SpecialTest.create(data_model)
      self.assertEqual(id, id)


  def test_get_special_test_receipts_by_condition(self):
      args = {"special_test_name":"test","offset":0,"limit":2,"status":"1"}
      SpecialTestDataModel.check_property(args)
      result = service.get_special_test_receipts(args)
      #print result
      self.assertEqual(1, 1)


  def test_edit_special_test_receipt(self):
      args = {"special_test_name":"test.....","status":"0","id":"10"}
      SpecialTestDataModel.check_property(args)

      domain_obj = SpecialTest(args.get("id"))
      domain_obj.modify(args)

      self.assertEqual(1, 1)


  def test_append_bug_into_special_test_receipt(self):
      args = {"author":"liang.han","bug_description":"this is test","parents_category":"22","owner":"junbo.han","is_solved":"1","parents_id":"3"}
      BugInfoDataModel.check_property(args)
      #print json.dumps(args)
      data_model = BugInfoDataModel.deserialize(args)
      new_id = SpecialTest.append_new_bug(data_model)


  def test_upload_old_excel_data(self):
      args = {"parents_id":"2"}
      excel_list = service.convert_excel(file_path = 'excel.xlsx')
      for row in excel_list:
          row["parents_id"] = args.get("parents_id",0)
          BugInfoDataModel.check_property(row)
          data_model = BugInfoDataModel.deserialize(row)
          new_id = SpecialTest.append_new_bug(data_model)
          print new_id


  def test_close_special_test_receipt(self):
      args = {"status":"12","id":"12"}
      SpecialTestDataModel.check_property(args)

      domain_obj = SpecialTest(args.get("id"))
      domain_obj.modify(args)

      self.assertEqual(1, 1)


class TestBugs(unittest.TestCase):


  def test_get_bugs_by_condition(self):
      args = {"author":"liang.han","offset":0,"limit":2}
      BugInfoDataModel.check_property(args)
      result = service.get_bugs(args)
      print result
      self.assertEqual(1, 1)



if __name__ == '__main__':
    unittest.main()
