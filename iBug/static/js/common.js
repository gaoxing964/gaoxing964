//当滚动条的位置处于距顶部100像素以下时，跳转链接出现，否则消失
$(function () {
    $('.datetimepicker').datetimepicker({
        format:"Y/m/d",
        timepicker:false
    });
	$(window).scroll(function(){
	if ($(window).scrollTop()>100){
	$("#back-to-top").fadeIn(1500);
	}
	else
	{
	$("#back-to-top").fadeOut(1500);
	}
	});
	//当点击跳转链接后，回到页面顶部位置
	$("#back-to-top").click(function(){
	$('body,html').animate({scrollTop:0},1000);
	return false;
	});
});

function detailFormatter(index, row) { 
    var html = [];
    $.each(row, function (key, value) {
      html.push('<p><b>' + key + ':</b> ' + value + '</p>');
    });
    return html.join('');
}

function rowStyle(row, index) { 
     
    row.create_time = echangedate(row.create_time);
    if(row.is_solved==0){
        row.is_solved='否';
    }else{
        row.is_solved='是';
    }
    
    return { classes: "", css: {"color": "", "font-size": ""}
        };
}
/**
 * 将时间戳转换为年月日
 */
function echangedate(sdate){
      var mystime = new Date(sdate * 1000); 
       var addstime = mystime.getFullYear() +'/' + fullnum(Number(mystime.getMonth()) + 1) + '/' + fullnum(mystime.getDate()); 
         return addstime
}

function fullnum(obj){
    if(Number(obj) < 10){
        return '0' + obj;
    }else{
        return obj;
    }
} 

function changebg(obj,cl){
    var bgcolor; 
    if(cl=="0"){bgcolor="#F5F5F5";}else{bgcolor="#FFFFFF";}
    obj.style.backgroundColor=bgcolor;
} 
function altRows(){
	//if(document.getElementsByTagName){  
		
		//var table = document.getElementById(id);  
		var rows = $("#bug_list_table tbody tr")
		 
		for(i = 0; i < rows.length; i++){          
			if(i % 2 == 0){
				rows[i].className = "evenrowcolor";
			}else{
				rows[i].className = "oddrowcolor";
			}      
		}
	//}
}
function load_project(url){
    $.ajax({
                method: "get",
                url: "/api/platform",
                //data: {data:combine_special_test_data},
                cache: false,
                dataType:"json",
                success: function(responData){  
                    var innerhtml = '<option value=""></option>';
                    for(var n=0;n<responData.data.length;n++){
                        innerhtml+='<option >'+responData.data[n]+'</option>'; 
                    }
                    $("#special_test_parents_project").html(innerhtml);
                    if(url=="search"){
                    	$(".chzn-select").chosen();
                        $("#special_test_parents_project_chzn").css({"width":"270px"});
                        $(".search-field").find('input').css({"height":"15px"}); 
                    }else if(url=="setting"){

                    }
                    
                },
                error: function(msg){

                }
          });       
}
/**
 * 将表单内的元素按照name属性封装为json实体
 */
$.fn.serializeObject = function() {
	var o = {};
	var a = this.serializeArray();
	$.each(a, function() {
		if (o[this.name]) {
			if (!o[this.name].push) {
				o[this.name] = [o[this.name]];
			}
			o[this.name].push(this.value || '');
		} else {
			o[this.name] = this.value || '';
		}
	});
	return o;
};

/**
 * 将json实体反序列化为表单内的元素值
 */
$.fn.deserializeObject=function(jsonObj){
	for(var i in jsonObj){
		var item=$(this).find('[name="'+i+'"]');
		if(item.length<1){
			continue;
		}
		str=jsonObj[i];
		if(str==undefined || str==null){
			str=''
		}else if(typeof(str)=='string'){
			str=$.trim(str);
		}
		if($(item.get(0)).attr('type')=='radio'){
			continue;
		}else if(item.get(0).tagName=='INPUT' || item.get(0).tagName=='SELECT'){
			item.val(str);
		}else if(item.get(0).tagName=='TEXTAREA'){
			item.html(str).val(str);
		}else{
			item.html(str);
		}
	}
};

function formatNum(per,num,length){
	num=num.toPrecision(length)+'';
	var index=num.indexOf('.');
	return per+num.substring(index+1)+num.substring(0,index);
}

/**
	*生成唯一的GUID
	*/
function newGuid(category,length){
    var guid = "";
    //取得自增长ID
    $.ajax({
        type: "get",
        url: '/trac/iSupport/apply/common',
        data: "act=sequence&seqkey="+category+"&_get_token="+new Date().getTime(),
        cache: false,
        async:false,
        //timeout:100,
    success: function(msg){
       guid=formatNum(category,parseInt(msg),length);
    },
    error: function(msg){
        guid = "";
    }
    });
/* 	for (var i = 1; i <= 32; i++){
		var n = Math.floor(Math.random()*16.0).toString(16);
 		guid +=    n;
		if((i==8)||(i==12)||(i==16)||(i==20))
   		guid += "-";
	} */
	return guid;    
}

/**
 * cookie操作
 * 
 * example $.cookie('name', 'value');
 * 设置cookie的值，把name变量的值设为value
 * example $.cookie('name', 'value', {expires: 7, path: '/', domain: 'jquery.com', secure: true});
 * 新建一个cookie 包括有效期 路径 域名等
 * example $.cookie('name', 'value');
 * 新建cookie
 * example $.cookie('name', undefined);
 * 删除一个cookie
 * var account= $.cookie('name');
 * 取一个cookie(name)值给account
 * @param name cookie的键
 * @param value cookie的值
 * @param options cookie的选项
 * @returns
 */
$.cookie = function(name, value, options) {
  if (typeof value != 'undefined') { // name and value given, set cookie
    options = options || {};
    if (value === null) {
      value = '';
      options.expires = -1;
    }
    var expires = '';
    if (options.expires && (typeof options.expires == 'number' || options.expires.toUTCString)) {
      var date;
      if (typeof options.expires == 'number') {
          date = new Date();
          date.setTime(date.getTime() + (options.expires * 24 * 60 * 60 * 1000));
      } else {
          date = options.expires;
      }
      expires = '; expires=' + date.toUTCString(); // use expires attribute, max-age is not supported by IE
    }
    var path = options.path ? '; path=' + options.path : '';
    var domain = options.domain ? '; domain=' + options.domain : '';
    var secure = options.secure ? '; secure' : '';
    document.cookie = [name, '=', encodeURIComponent(value), expires, path, domain, secure].join('');
  } else { // only name given, get cookie
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
      var cookies = document.cookie.split(';');
      for (var i = 0; i < cookies.length; i++) {
        var cookie = jQuery.trim(cookies[i]);
        // Does this cookie string begin with the name we want?
        if (cookie.substring(0, name.length + 1) == (name + '=')) {
            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
            break;
        }
      }
    }
    return cookieValue;
  }
};

/**
 * 合并json对象
 * var a ={"a":"1","b":"2"}
 * var b ={"c":"3","d":"4","e":"5"}
 * var c = extend({}, [a,b]);
 * alert(c.a);
 */
function combineJSON(des,src){
	if(src instanceof Array){
		for(var i = 0, len = src.length; i < len; i++){
			combineJSON(des,src[i]);
		}
	}
	for(var i in src){
		if(isJSON(des[i]) && isJSON(src[i])){
			combineJSON(des[i],src[i]);
		}else{
			des[i] = src[i];
		}
	} 
	return des;
}

/**
 * 判断对象是否json格式
 */
function isJSON(obj){
	return typeof(obj)=='object' && Object.prototype.toString.call(obj).indexOf('[object')==0 && !obj.length;
}

/**
 * 获取json的浅层有效长度
 * @param obj
 * @returns
 */
function getJSONLength(obj){
	if(!isJSON(obj)){
		return undefined;
	}
	var len=0;
	for(var i in obj){
		if(obj[i]!=undefined){
			len++;			
		}
	}
	return len;
}

/**
 * js解析浏览器地址
 */
window.url = (function() {
    function isNumeric(arg) {
      return !isNaN(parseFloat(arg)) && isFinite(arg);
    }
    
    return function(arg, url) {
        var _ls = url || window.location.toString();

        if (!arg) { return _ls; }
        else { arg = arg.toString(); }

        if (_ls.substring(0,2) === '//') { _ls = 'http:' + _ls; }
        else if (_ls.split('://').length === 1) { _ls = 'http://' + _ls; }

        url = _ls.split('/');
        var _l = {auth:''}, host = url[2].split('@');

        if (host.length === 1) { host = host[0].split(':'); }
        else { _l.auth = host[0]; host = host[1].split(':'); }

        _l.protocol=url[0];
        _l.hostname=host[0];
        _l.port=(host[1] || ((_l.protocol.split(':')[0].toLowerCase() === 'https') ? '443' : '80'));
        _l.pathname=( (url.length > 3 ? '/' : '') + url.slice(3, url.length).join('/').split('?')[0].split('#')[0]);
        var _p = _l.pathname;

        if (_p.charAt(_p.length-1) === '/') { _p=_p.substring(0, _p.length-1); }
        var _h = _l.hostname, _hs = _h.split('.'), _ps = _p.split('/');

        if (arg === 'hostname') { return _h; }
        else if (arg === 'domain') {
            if (/^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$/.test(_h)) { return _h; }
            return _hs.slice(-2).join('.'); 
        }
        //else if (arg === 'tld') { return _hs.slice(-1).join('.'); }
        else if (arg === 'sub') { return _hs.slice(0, _hs.length - 2).join('.'); }
        else if (arg === 'port') { return _l.port; }
        else if (arg === 'protocol') { return _l.protocol.split(':')[0]; }
        else if (arg === 'auth') { return _l.auth; }
        else if (arg === 'user') { return _l.auth.split(':')[0]; }
        else if (arg === 'pass') { return _l.auth.split(':')[1] || ''; }
        else if (arg === 'path') { return _l.pathname; }
        else if (arg.charAt(0) === '.')
        {
            arg = arg.substring(1);
            if(isNumeric(arg)) {arg = parseInt(arg, 10); return _hs[arg < 0 ? _hs.length + arg : arg-1] || ''; }
        }
        else if (isNumeric(arg)) { arg = parseInt(arg, 10); return _ps[arg < 0 ? _ps.length + arg : arg] || ''; }
        else if (arg === 'file') { return _ps.slice(-1)[0]; }
        else if (arg === 'filename') { return _ps.slice(-1)[0].split('.')[0]; }
        else if (arg === 'fileext') { return _ps.slice(-1)[0].split('.')[1] || ''; }
        else if (arg.charAt(0) === '?' || arg.charAt(0) === '#')
        {
            var params = _ls, param = null;
            if(arg.charAt(0) === '?') { params = (params.split('?')[1] || '').split('#')[0]; }
            else if(arg.charAt(0) === '#') { params = (params.split('#')[1] || ''); }
            if(!arg.charAt(1)) { return params; }
            arg = arg.substring(1);
            params = params.split('&');
            for(var i=0,ii=params.length; i<ii; i++)
            {
                param = params[i].split('=');
                if(param[0] === arg) { return param[1] || ''; }
            }
            return null;
        }
        return '';
    };
})();

if(typeof jQuery !== 'undefined') {
    jQuery.extend({
        url: function(arg, url) { return window.url(arg, url); }
    });
}

var code ;
function createCode(){
     code = ""; 
     var codeLength = 4;
     var checkCode = document.getElementById("code"); 
     var random = new Array(0,1,2,3,4,5,6,7,8,9,'A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R',
     'S','T','U','V','W','X','Y','Z','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u',
     'v','w','x','y','z');//
     for(var i = 0; i < codeLength; i++) {//
        var index = Math.floor(Math.random()*62);//?0~62?
        code += random[index];
    }
    checkCode.value = code;
}

function validate(){
    var inputCode = document.getElementById("validCode").value.toUpperCase(); //      
    if(inputCode.length <= 0) {
        return false;
    }       
    else if(inputCode != code.toUpperCase()  ) {
        createCode();
        document.getElementById("validCode").value= "";
        return false;
    }       
    else {
        return true;
    }           
}

function closeColorboxMask(){
	$("#cboxLoadingGraphic,#cboxLoadingOverlay").hide();
}