//var globalSpecial_Test_data;
var $table = $("#bug_list_table");
var $bug_statistics = $("#bug_statistics_table");
$(function() {

	get_Special_Test_list();
	get_alluser();
	// 將頁面中的新增按鈕放入工具條中  
	initBtn_new();
	initHelpStyle();
});

// 將頁面中的新增按鈕放入工具條中   
function initBtn_new() {
	$('#bug_list .bootstrap-table>.fixed-table-toolbar>.btn-group:eq(0)').append($('#btn_new'));
}

var query_param = {};

function queryHandler(param) {
	param["parents_id"] = query_param["parents_id"];

	param["author"] = query_param["author"];
	param["owner"] = query_param["owner"];
	param["is_solved"] = query_param["is_solved"];
	//console.log(param);
	return param
}

function All_Bug_List() {
	$("#all_bug").css("background", "#FFA900");
	$("#my_bug,#my_todo_bug").css("background", "#E5E5E5");
	query_param["owner"] = '';
	query_param["author"] = '';
	query_param["is_solved"] = ''
	query_param["url"] = "/api/bugs_info";
	if (!query_param["parents_id"]) {
		query_param["url"] = "";
	}
	$table.bootstrapTable("refresh", query_param);

}
var author;

function My_SubmitedHandler() {
	$("#my_bug").css("background", "#FFA900");
	$("#all_bug,#my_todo_bug").css("background", "#E5E5E5");
	query_param["owner"] = '';
	query_param["is_solved"] = '';
	author = $("#passed-username").attr("data")
	query_param["author"] = author;
	//query_param["url"]="/api/bugs_info";
	if (!query_param["parents_id"]) {
		query_param["url"] = "";
	}
	$table.bootstrapTable("refresh", query_param);

}
var owner;

function My_TodosearchHandler() {
	$("#my_todo_bug").css("background", "#FFA900");
	$("#all_bug,#my_bug").css("background", "#E5E5E5");
	query_param["author"] = '';
	query_param["is_solved"] = 0;
	owner = $("#passed-username").attr("data");
	query_param["owner"] = owner;
	if (!query_param["parents_id"]) {
		query_param["url"] = "";
	}
	$table.bootstrapTable("refresh", query_param);

}

var globalrow = [];

function operateFormatter(value, row, index) {
	globalrow.push(row);
	var username = $("#passed-username").attr("data");
	if (username) {
		if (username == row.author || username == row.owner) {
			if (row.is_solved == "是") {

				return [
					'<a class="edit" href="#BugModal" title="Edit" onclick="edit_bug(' + row.id + ',/edit/);">',
					'<i class="glyphicon glyphicon-edit icon-edit"></i>',
					'</a> &nbsp;&nbsp;',
					'<a class="copy" href="#BugModal" title="copy" onclick="edit_bug(' + row.id + ',/copy/);">',
					'<i class="icon-file"></i>',
					'</a>&nbsp;&nbsp;&nbsp;',
					'<a class="copy" href="#BugModal" title="delete" onclick="delete_bug(' + row.id + ');">',
					'<i class="icon-remove"></i>',
					'</a>'
				].join('');

			} else {
				return [
					'<a class="edit" href="#BugModal" title="Edit" onclick="edit_bug(' + row.id + ',/edit/);">',
					'<i class="glyphicon glyphicon-edit icon-edit"></i>',
					'</a> &nbsp;&nbsp;',
					'<a class="copy" href="#BugModal" title="copy" onclick="edit_bug(' + row.id + ',/copy/);">',
					'<i class="icon-file"></i>',
					'</a>&nbsp;&nbsp;',
					'<a class="" href="javascript:void(0)" title="close" onclick="close_bug(' + row.id + ')">',
					'<i class="icon-off"></i>',
					'</a>&nbsp;&nbsp;&nbsp;',
					'<a class="copy" href="#BugModal" title="delete" onclick="delete_bug(' + row.id + ');">',
					'<i class="icon-remove"></i>',
					'</a>'

				].join('');
			}
		}
	} else {
		return '';
	}

}

function edit_bug(id, op) {
	$("#bugs_info_id").val(id);
	$("#BugModal").show();
	if (op == "/copy/") {
		$("#myModalLabel").html('Copy and Add bug');
	} else {
		$("#myModalLabel").html('Modify bug');
	}

	for (var j = 0; j < globalrow.length; j++) {
		if (id == globalrow[j].id) {

			if (globalrow[j].is_solved == '是') {
				globalrow[j].is_solved = '1';
			} else {
				globalrow[j].is_solved = '0'
			}
			$("#modal_form").deserializeObject(globalrow[j]);

		}
		if (id == globalrow[j].id) {
			var owner = globalrow[j].owner.split(',');
			for (var n = 0; n < owner.length; n++) {
				$("#owner option[value='" + owner[n] + "']").attr("selected", "selected");
			}
		}
		$(".chzn-select").trigger("liszt:updated");
	}
}

function delete_bug(id) {
	var t_data = {
		"id": id
	};
	$.ajax({
		method: "POST",
		url: "/api/delete/bug_into",
		data: t_data,
		cache: false,
		dataType: "json",
		success: function(responData) {
			if (confirm("确定删除此Bug？")) {
				alert("删除成功！"); //$("#BugModal").hide();
				$table.bootstrapTable("refresh", query_param);
			} else {
				return false
			}
		},
		error: function(responData) {
			alert(responData.message);
		}
	})
}

function location_to_create() {
	$("#BugModal").show();
	$("#myModalLabel").html("Append New Bug");

	//$("#bug_description").val("");
	//$("#remark").val("");
}
$("#reset_button").click(function() {
	$("#BugModal").hide();

})

function close_bug(id) {
	var t_data = {
		"id": id,
		"is_solved": 1
	};
	var b_data = JSON.stringify(t_data);
	$.ajax({
		method: "POST",
		url: "/api/modify/bug_info",
		data: {
			data: b_data
		},
		cache: false,
		dataType: "json",
		success: function(responData) {
			if (confirm("确定关闭此Bug？")) {
				alert("关闭成功！"); //$("#BugModal").hide();
				$table.bootstrapTable("refresh", query_param);
			} else {
				return false
			}
		},
		error: function(responData) {
			alert(responData.message);
		}
	});
}

function submit_append_bug() {


	var Special_Test_list = $("#special_test_name").val();
	var case_number = $("#case_number").val();
	var bug_description = $("#bug_description").val();
	var parents_category = $("#parents_category").val();
	var owner = $("#owner").val();
	var is_solved = $("#is_solved").val();
	var bug_id = $("#bug_id").val();
	var remark = $("#remark").val();
	var priority = $("#priority").val();

	setCookie("username", Special_Test_list);
	setCookie("case_num", case_number);
	setCookie("bug_des", bug_description);
	setCookie("parents_cate", parents_category);
	setCookie("own", owner);
	setCookie("is_sol", is_solved);
	setCookie("bug", bug_id);
	setCookie("prio", priority);
	setCookie("rem", remark);

	if (!Special_Test_list) {
		alert("请选择专项测试单！");
		return false;
	}
	if (!bug_description) {
		alert("请输入问题描述！");
		return false;
	}
	if (!parents_category) {
		alert("请选择所属模块！");
		return false;
	}
	if (!owner) {
		alert("请填写责任人！");
		return false;
	}
	if (!is_solved) {
		alert("请确认是否已解决！");
		return false;
	}
	/*var re = /^[0-9]+.?[0-9]*$/;   //判断字符串是否为数字     //判断正整数 /^[1-9]+[0-9]*]*$/  
	if(!re.test(bug_id)){
	    alert("Bug ID请输入数字！");
	    return false;
	}*/

	var parrentid = {
		"parents_id": Special_Test_list
	}
	var pageFilter = {};
	try {
		pageFilter = $('#modal_form').serializeObject();
		for (var i in pageFilter) {
			pageFilter[i] = (pageFilter[i] == null) ? null : pageFilter[i] + '';
		}
	} catch (e) {
		pageFilter = {};
	}
	var special_test_data = combineJSON(parrentid, pageFilter);

	var combine_special_test_data = JSON.stringify(special_test_data);
	if ($("#myModalLabel").html() == "Append New Bug" || $("#myModalLabel").html() == "Copy and Add bug") {
		$.ajax({
			method: "POST",
			url: "/Home/bug_into",
			data: {
				data: combine_special_test_data
			},
			cache: false,
			dataType: "json",
			success: function(responData) {
				alert("新增bug成功！");
				$("#BugModal").hide();
				$table.bootstrapTable("refresh", query_param);
				$bug_statistics.bootstrapTable("refresh");
				window.location.href = $('#go_top').attr('href');

				setCookie("username", "");
				setCookie("case_num", "");
				setCookie("bug_des", "");
				setCookie("parents_cate", "");
				setCookie("own", "");
				setCookie("is_sol", "");
				setCookie("bug", "");
				setCookie("prio", "");
				setCookie("rem", "");

			},
			error: function(responData) {
				alert(responData.message);
			}
		});
	} else if ($("#myModalLabel").html() == "Modify bug") { //修改bug
		var bugs_info_id = {
			"id": $("#bugs_info_id").val()
		};
		var t_data = combineJSON(bugs_info_id, pageFilter);

		var b_data = JSON.stringify(t_data);
		$.ajax({
			method: "POST",
			url: "/api/modify/bug_info",
			data: {
				data: b_data
			},
			cache: false,
			dataType: "json",
			success: function(responData) {
				alert("修改成功！");
				$("#BugModal").hide();
				$table.bootstrapTable("refresh", query_param);
				window.location.href = $('#go_top').attr('href');
			},
			error: function(responData) {
				alert(responData.message);
			}
		});
	}
}


function get_Special_Test_list() { //获取专项测试
	$.ajax({
		method: "get",
		url: "/api/special_test_receipts_without_paging?status=1",
		cache: false,
		dataType: "json",
		success: function(responData) {
			var innerhtml = '<option value=""></option>';
			for (var n = 0; n < responData.data.length; n++) {
				innerhtml += '<option value=' + responData.data[n].id + '>' + responData.data[n].special_test_name + '</option>';
			}
			$("#special_test_name").html(innerhtml);
		},
		error: function(msg) {

		}

	});

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
			$("#owner").html(innerhtml);
			$(".chzn-select").chosen();
			check_cookie();
		},
		error: function(msg) {

		}
	});
}

function check_cookie() {
	var cookie_data = getCookie();
	for (var i = 0; i < cookie_data.length; i++) {
		var arr = cookie_data[i].split("=");

		if (arr[0] == "username") {
			$("#special_test_name").val(String(arr[1]));
		} else if (arr[0] == "case_num") {
			$("#case_number").val(arr[1]);
		} else if (arr[0] == "bug_des") {
			if (arr[1]) {
				$("#bug_description").val(unescape(arr[1]))
			} else {
				$("#bug_description").val("")
			};
		} else if (arr[0] == "parents_cate") {
			$("#parents_category").val(arr[1]);
		} else if (arr[0] == "own") {
			var owne = '';
			if (arr[1]) {
				owne = arr[1].replace(/%2C/g, ",");
			}
			var owner = owne.split(',');
			for (var n = 0; n < owner.length; n++) {
				$("#owner option[value='" + owner[n] + "']").attr("selected", "selected");
			}
			$(".chzn-select").trigger("liszt:updated");
		} else if (arr[0] == "is_sol") {
			$("#is_solved").val(arr[1]);
		} else if (arr[0] == "bug") {
			$("#bug_id").val(arr[1]);
		} else if (arr[0] == "rem") {
			if (arr[1]) {
				$("#remark").val(unescape(arr[1]))
			} else {
				$("#remark").val("")
			};
		} else if (arr[0] == "prio") {
			$("#priority").val(arr[1]);
		}
	}

}


function setCookie(name, value) {
	var Days = 60; //cookie 将被保存两个月
	var exp = new Date(); //获得当前时间
	exp.setTime(exp.getTime() + Days * 24 * 60 * 60 * 1000); //换成毫秒
	document.cookie = name + "=" + escape(value) + ";expires=" + exp.toGMTString();
}

function getCookie(name) {
	//取出cookie
	var strCookie = document.cookie;
	//cookie的保存格式是 分号加空格 "; "
	var arrCookie = strCookie.split("; ");
	return arrCookie;
}

/** toturial的相关代码  **/

function initHelpStyle() {
	var startBtn = $('<a>').css({
		color: 'red',
		'font-weight': 700,
		'padding-left': '15px'
	}).attr('href', '#').text('toturial').click(function() {
		$('body').pagewalkthrough({
			name: 'introduction',
			steps: [{
				popup: {
					content: '#walkthrough-1',
					type: 'modal'
				},
				onEnter: function() {
					return true;
				},
				onLeave: function() {
					return true;
				}
			}, {
				wrapper: '#login-container',
				popup: {
					content: '#walkthrough-2',
					type: 'tooltip',
					position: 'left'
				},
				onEnter: function() {
					return true;
				},
				onLeave: function() {
					return true;
				}
			}, {
				wrapper: '#btn_new',
				popup: {
					content: '#walkthrough-3',
					type: 'tooltip',
					position: 'left'
				},
				onLeave: function() {
					$('#btn_new').click();
					return true;
				},
				onEnter: function() {
					return true;
				}
			}, {
				wrapper: '#modal_form',
				popup: {
					content: '#walkthrough-4',
					type: 'tooltip',
					position: 'top'
				},onLeave: function() {
					return true;
				},
				onEnter: function() {
					var height = $('#modal_form').position().top;
					window.scrollTo(0, (parseInt(height) - 500));
					return true;
				}
			}, {
				wrapper: '#btnSubmit',
				popup: {
					content: '#walkthrough-5',
					type: 'tooltip',
					position: 'left'
				},
				onLeave: function() {
					$("#BugModal").hide();
					window.scrollTo(0, 0);
					return true;
				},
				onEnter: function() {
					var height = $('#btnSubmit').position().top;
					window.scrollTo(0, parseInt(height) - 200);
					return true;
				}
			}]
		});
		$('body').pagewalkthrough('show');
	});
	$('#login-container').append(startBtn);
}