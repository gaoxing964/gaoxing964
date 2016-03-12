var globalSpecial_Test_data;
/**这段代码用于存储新的选项 **/
var special_test_parents_project_arrays = ['Whale', 'Whale2', 'SharkL', 'TShark3', 'SC9830I'];

$(function() {
	Load_Special_Test(function() {});
	load_project('setting');
	get_alluser();
});

/**  这段代码在common.js中也有  在这边定义是为了保持页面的兼容行  初始化专项所属项目的代码    **/
function load_project(url) {
	$.ajax({
		method: "get",
		url: "/api/platform",
		//data: {data:combine_special_test_data},
		cache: false,
		dataType: "json",
		success: function(responData) {
			var innerhtml = '<option value=""></option>';
			for (var n = 0; n < responData.data.length; n++) {
				innerhtml += '<option value="' + responData.data[n] + '" >' + responData.data[n] + '</option>';
			}
			/**这段代码用于增加新的选项 **/
			(function() {
				for (var j = 0; j < special_test_parents_project_arrays.length; j++) {
					innerhtml += '<option value="' + special_test_parents_project_arrays[j] + '" >' + special_test_parents_project_arrays[j] + '</option>';
				}
			})();
			$("#special_test_parents_project").html(innerhtml);
			if (url == "search") {
				$(".chzn-select").chosen();
				$("#special_test_parents_project_chzn").css({
					"width": "270px"
				});
				$(".search-field").find('input').css({
					"height": "15px"
				});
			} else if (url == "setting") {

			}
		},
		error: function(msg) {

		}
	});
}


function Load_Special_Test(callback) {
	var status = $("#status").val();
	var creator = $("#creators").val();
	var special_test_name = $("#special_test_name").val();
	if (special_test_name == undefined || special_test_name == "undefined") {
		special_test_name = '';
	}
	if (creator == undefined || creator == "undefined") {
		creator = '';
	}
	$.ajax({
		type: "get",
		url: "api/special_test_receipts?special_test_name=" + $("#Special_names").val() + "&status=" + $("#status").val() + "&creator=" + creator,
		cache: false,
		dataType: "json",
		success: function(responData) {
			var Special_data;
			Special_data = responData;
			globalSpecial_Test_data = Special_data.rows;
			var innerhtml = '';
			if ((Special_data.rows).length > 0) {
				for (var i = 0; i < (Special_data.rows).length; i++) {
					if (Special_data.rows[i].status == 1) {
						Special_data.rows[i].status = "open";
					} else {
						Special_data.rows[i].status = "close";
					}
					innerhtml += '<tr onmouseOver="javascript:changebg(this,0)"  style="backgroud-color:#FFFFFF" onmouseOut="javascript:changebg(this,1)"><td align="center">' + (Special_data.rows)[i].id + '<td>' + (Special_data.rows)[i].creator + '</td></td><td>' + (Special_data.rows)[i].special_test_name + '</td> <td align="center">' + (Special_data.rows)[i].status + '</td>' + '<td align="center">'
						//+'<a class="btn small" href="javascript:void(0)" onclick="open_opration('+i+')" ><i class="icon-align-justify"></i></a>'
						+ '<div class="dropdown clearfix" style="width:50%">' + '        <ul class="" style="list-style-type:none">' + '          <li class="dropdown-submenu">' + '            <a tabindex="-1" href="#"><i class="icon-align-justify"></i></a>' + '            <ul class="dropdown-menu" >'
						//+'              <li><a tabindex="-1" href="javascript:void(0)" onclick=append_Bug('+(Special_data.data)[i].id+',"'+(Special_data.data)[i].special_test_name+'")>追加Bug</a></li>'
						+ '              <li><a tabindex="-1" href="javascript:void(0)" onclick="close_Status(' + (Special_data.rows)[i].id + ')">关闭</a></li>' + '              <li><a tabindex="-1" href="javascript:void(0)" onclick="edit_Special(' + (Special_data.rows)[i].id + ')">编辑专项</a></li>'
						//+'              <li><a tabindex="-1" href="https://isupport.spreadtrum.com/iSupport/apply/itrain_customer?act=download_file&file_id=39" >导出专项Bug</a></li>' 
						+ '              <li><a tabindex="-1" href="javascript:void(0)" onclick="import_Special_Bug(' + (Special_data.rows)[i].id + ')">导入专项Bug</a></li>' + '            </ul>' + '          </li>' + '        </ul>' + '</div>' + '</td>' + '</tr>';
				}
			} else {
				innerhtml += '<tr><td align="center" colspan="5">NO DATA!</td></tr>'
			}
			$("#Special_left").find('[class="Special_datatable"]').html(innerhtml);
			callback();
		},
		error: function() {

		}
	});

}

function show_search_div() {
	$("#search_div").toggle();
}


function search_Special() {

	Load_Special_Test(function() {});

}

$("#add_Special_test").click(function() {
	$("#cerate_Special_div").show();
	$("#append_bug_div,#bug_list,#import_bug_div").hide();
	$("#Special").html("创建专项");
	$("#reset_button").trigger("click");
});

function import_Special_Bug(id) {

	$("#import_bug_div").show();
	$("#cerate_Special_div,#append_bug_div,#bug_list").hide();
	$("#parrentid").val(id);
	$("#iframe_div").html("");
	$("#iframe_div").html('<iframe id="ibug_ifram" name="ibug_upload" scrolling="auto" src="/ibug/upload?pid=' + id + '" frameborder="no" border="no" style="margin-left:20px;width:500px;border: 0px;"> </iframe> ');
	//$("#ibug_ifram").contents().find("#parents_id").val(id);

}

function close_Status(id) {
	var sdata = {
		"id": id,
		"status": "0"
	}
	var data = JSON.stringify(sdata);
	if (confirm("请确定关于此专项的所有Bug已解决？")) {
		$.ajax({
			method: "POST",
			url: "api/modify/special_test_receipt",
			data: {
				data: data
			},
			cache: false,
			dataType: "json",
			success: function(responData) {
				Load_Special_Test(function() {});
			},
			error: function() {

			}
		})
	}
}

function edit_Special(id) {
	$("#cerate_Special_div").show();
	$("#append_bug_div,#bug_list,#import_bug_div").hide();
	$("#Special").html("编辑专项");
	$("#parrentid").val(id);
	var itemdata = globalSpecial_Test_data;
	var fiterdata = {};
	for (var k = 0; k < itemdata.length; k++) {
		if (itemdata[k].id == id) {
			var end_itemdate = echangedate(itemdata[k].intend_end_time);
			var start_itemdate = echangedate(itemdata[k].starting_time);
			fiterdata = {
				"case_number_prefix": itemdata[k].case_number_prefix,
				"coding_developer": itemdata[k].coding_developer,
				"integration_testing_case_amount": itemdata[k].integration_testing_case_amount,
				"integration_testing_developer": itemdata[k].integration_testing_developer,
				"coding_row": itemdata[k].coding_row,
				"creator": itemdata[k].creator,
				"intend_end_time": end_itemdate,
				"research_coding_developer": itemdata[k].research_coding_developer,
				"special_test_cc_list": itemdata[k].special_test_cc_list,
				"special_test_name": itemdata[k].special_test_name,
				"special_test_parents_project": itemdata[k].special_test_parents_project,
				"special_test_pm": itemdata[k].special_test_pm,
				"starting_time": start_itemdate,
				"status": itemdata[k].status,
				"unit_test_case_amount": itemdata[k].unit_test_case_amount
			}
		}
	}

	$('#cerate_Special_form').deserializeObject(fiterdata);
	var coding_developer = fiterdata.research_coding_developer.split(',');
	var test_cc_list = fiterdata.special_test_cc_list.split(',');
	var test_pm = fiterdata.special_test_pm.split(',');
	var testing_developer = fiterdata.integration_testing_developer.split(',');
	for (var n = 0; n < testing_developer.length; n++) {
		$("#integration_testing_developer option[value='" + testing_developer[n] + "']").attr("selected", "selected");
	}
	for (var n = 0; n < test_pm.length; n++) {
		$("#special_test_pm option[value='" + test_pm[n].toLowerCase() + "']").attr("selected", "selected");
	}
	for (var n = 0; n < test_cc_list.length; n++) {
		$("#special_test_cc_list option[value='" + test_cc_list[n] + "']").attr("selected", "selected");
	}

	for (var n = 0; n < coding_developer.length; n++) {
		$("#research_coding_developer option[value='" + coding_developer[n] + "']").attr("selected", "selected");
	}

	$(".chzn-select").trigger("liszt:updated");
}

function submit_Special_test() {
	var special_test_name = $("#special_test_name").val();
	var special_test_parents_project = $("#special_test_parents_project").val();

	if (!special_test_name) {
		alert("请输入专项测试名称！");
		return false;
	}
	if (!special_test_parents_project) {
		alert("请输入专项测试名称！");
		return false;
	}
	var user = $("#passed-username").attr("data");
	var login_user = {
		"creator": user
	}
	var pageFilter = {};
	try {
		pageFilter = $('#cerate_Special_form').serializeObject();
		for (var i in pageFilter) {
			pageFilter[i] = (pageFilter[i] == null) ? null : pageFilter[i] + '';
		}
	} catch (e) {
		pageFilter = {};
	}


	pageFilter.starting_time = (new Date(pageFilter.starting_time).getTime() / 1000);
	pageFilter.intend_end_time = (new Date(pageFilter.intend_end_time).getTime() / 1000);
	var special_test_data = combineJSON(login_user, pageFilter);
	var combine_special_test_data = JSON.stringify(special_test_data);
	if ($("#Special").html() == "编辑专项") {
		var parrentid = $("#parrentid").val();
		var iddata = {
			"id": parrentid
		};
		var edit_data = combineJSON(special_test_data, iddata);
		$.ajax({
			method: "POST",
			url: "/api/modify/special_test_receipt",
			data: {
				data: JSON.stringify(edit_data)
			},
			cache: false,
			dataType: "json",
			success: function(responData) {
				alert("编辑成功");
				var conditions = {};
				Load_Special_Test(function() {});
				//show_oneSpecial_buglist(responData.data,'');
			},
			error: function() {

			}
		});
	} else if ($("#Special").html() == "创建专项") {
		$.ajax({
			method: "POST",
			url: "/api/special_test_receipt",
			data: {
				data: combine_special_test_data
			},
			cache: false,
			dataType: "json",
			success: function(responData) {
				alert("创建成功");
				Load_Special_Test(function() {
					// show_oneSpecial_buglist(globalSpecial_Test_data.data[0].id,globalSpecial_Test_data.data[0].special_test_name);
				});

			},
			error: function() {

			}
		});
	}

}

function get_alluser() {
	$.ajax({
		method: "get",
		url: "/api/Alluser",

		cache: false,
		dataType: "json",
		success: function(responData) {
			var innerhtml = '<option value=""></option>';
			for (var n = 0; n < responData.data.length; n++) {
				innerhtml += '<option value=' + responData.data[n] + '>' + responData.data[n] + '</option>';
			}
			$("#special_test_pm,#integration_testing_developer,#special_test_cc_list,#research_coding_developer").html(innerhtml);

			$(".chzn-select").chosen({

			});

		},
		error: function(msg) {

		}
	});
}