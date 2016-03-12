#coding:utf-8
import time
import dal_proxy as dal

def get_special_test_receipts(condition):
    dao = dal.SpecialTestDAL()
    return dao.get_by_condition(condition)

def get_special_test_receipts_without_paging(condition):
    dao = dal.SpecialTestDAL()
    return dao.get_by_condition_without_paging(condition)

def bug_count(condition):
    dao = dal.SpecialTestDAL()
    return dao.bug_count(condition)

def bug_count_for_email():
    dao = dal.SpecialTestDAL()
    return dao.bug_count_for_email()

def add_from_excel(data_list,parents_id):
    dao = dal.BugInfoDAL()
    return dao.add_from_excel(data_list,parents_id)


def get_bugs(condition):
     

    dao = dal.BugInfoDAL()
    return dao.get_by_condition(condition)

def add_from_excel(data_list,parents_id):
    dao = dal.BugInfoDAL()
    return dao.add_from_excel(data_list,parents_id)

def get_bug_by_id(id):
    dao = dal.BugInfoDAL()
    return dao.get(id)

def delete_bug_by_id(id):
    dao = dal.BugInfoDAL()
    return dao.delete(id)

def search_bugs(condition):
     

    dao = dal.BugInfoDAL()
    return dao.search(condition)


def get_project_name():
    dao = dal.SpecialTestDAL()
    return dao.get_project_name()


def get_Alluser():
    dao = dal.SpecialTestDAL()
    return dao.get_Alluser()

def search_bug_by_parents_info(condition):
    dao = dal.SpecialTestDAL()
    parents_row = dao.get_by_condition_without_paging(condition)

    parents_id = []
    for row in parents_row:
      parents_id.append(row["id"])

    dao = dal.BugInfoDAL()
    return dao.get_by_parents_ids(condition, parents_id)


def convert_excel(file_path):
      result = []
      import xlrd
      data = xlrd.open_workbook(file_path)
      table = data.sheet_by_index(0)
      table_head_row = table.row_values(0)

      if not len(table_head_row) == 11:
        raise ImportError("Excel file format error")

      nrows = table.nrows
      for i in range(1, nrows ):
          row = table.row_values(i)
          case_number = row[1]
          author = row[2]
          bug_description = row[4]
          parents_category = row[5]
          owner = row[6]
          is_solved = row[7]
          priority = row[8]
          bug_id = row[9]
          remark = row[10]

          is_solved = is_solved.strip()
          is_solved = 1 if is_solved.find(u"是") > -1 else 0

          args = dict(case_number = case_number,
                          author = author,
                          bug_description = bug_description,
                          parents_category = parents_category,
                          owner = owner,
                          is_solved = is_solved,
                          priority = priority,
                          bug_id = bug_id,
                          remark = remark  )
          result.append(args)

      return result





