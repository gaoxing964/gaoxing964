
$(function(){  
    //load_project('search');
    createDiv();
    
})
$(document).bind("click",function(e){ 
    	var target = $(e.target); 
    	if(target.closest(".special_div").length == 0){ 
    	$("#descDiv").hide(); 
    	}
});

 

function queryHandler(param){  
         
		param["project_start_time"] = query_param["project_start_time"];
	    param["project_end_time"] = query_param["project_end_time"]; 
        param["author"] = query_param["author"];
        param["owner"] = query_param["owner"]; 
        param["parents_category"] = query_param["parents_category"]; 
        param["special_test_parents_project"] = query_param["special_test_parents_project"]; 
         
        param["is_solved"] = query_param["is_solved"];
        param["special_test_name"] = query_param["special_test_name"]; 
        return param
         
}


var $table=$("#bug_list_table");
var query_param={};
function search_all_bugs(){
	 
    var start_date = $("#start_datetimepicker").val(); 
    var end_date = $("#end_datetimepicker").val();
    var special_test_parents_project = $("#special_test_parents_project").val();
    var special_test_name = $("#special_test_name").val();
    var owner = $("#owner").val();
    var author = $("#author").val();
    var parents_category = $("#parents_category").val();
    var is_solved = $("#is_solved").val();
    var project_start_time = start_date = (new Date(start_date).getTime()/1000);
    var project_end_time = end_date = (new Date(end_date).getTime()/1000);
     
    query_param["project_start_time"]= project_start_time;
    query_param["project_end_time"]= project_end_time;
    query_param["owner"]= owner;
    query_param["author"]= author;
    query_param["parents_category"]= parents_category;
    query_param["special_test_name"]= special_test_name;
    query_param["special_test_parents_project"]= special_test_parents_project;
    query_param["author"]= author;
    query_param["is_solved"]= is_solved;
	query_param["url"]="/api/search";
	
    $table.bootstrapTable("refresh",query_param);
        
}

function createDiv(){
	$("#descDiv").remove();
	//首先创建div   
	var descDiv = document.createElement('div');  
	document.body.appendChild(descDiv);  
	//获取输入框dom元素    
	var text = document.getElementById('special_test_parents_project');  
	//计算div的确切位置
	var seatX = text.offsetLeft + text.offsetWidth;
	//横坐标   
	var seatY = text.offsetTop + text.offsetHeight;
	//纵坐标  
	//给div设置样式，比如大小、位置  
	var cssStr = "z-index:5;width:250px;height:300px;overflow-x: auto;overflow-y: auto;background-color:#FFFFFF;border:1px solid #FFB366;position:absolute;left:"     + (seatX-220) + 'px;top:' + seatY + 'px;'; 
	//将样式添加到div上，显示div  
	descDiv.style.cssText = cssStr;  
	//descDiv.innerHTML = '这是一个测试的div显示的内容';  
	descDiv.id = 'descDiv';
	descDiv.className = 'special_div';  
	descDiv.style.display = 'none';
	$.ajax({
        method: "get",
        url: "/api/platform", 
        cache: false,
        dataType:"json",
        success: function(responData){  
            var innerhtml = '<table width="100%">';
            for(var n=0;n<responData.data.length;n++){
            innerhtml+='<tr class="special_div" onmouseOver="javascript:changebg(this,0)"  onmouseOut="javascript:changebg(this,1)" style="backgroud-color:#FFFFFFheight:25px;"><td><input type="checkbox" name="chk" onclick="get_project()"  style="margin-left:5px;margin-top:-2px" id='+responData.data[n]+' value='+responData.data[n]+' />&nbsp;'+responData.data[n]+'</td></tr>'; 
            }
            innerhtml+='</table>';
            $("#descDiv").html(innerhtml); 
        },
        error: function(msg){

        }
  });
	 
}

function get_project(){ 
    	var aa = document.getElementsByName("chk");         
    	var ss = "";               
    	for (var i = 0; i < aa.length; i++) {             
    		if (aa[i].checked) {                   
    			ss += aa[i].value+',';              
    			}             
    		}            
    	$("#special_test_parents_project").val(ss); 
}

function special_test_list(){
	$("#descDiv").show();
	
}
 