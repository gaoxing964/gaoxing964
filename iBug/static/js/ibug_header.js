$(function(){
		$(".menu li a").wrapInner( '<span class="out"></span>');
		$(".menu li a").each(function() {
			$('<span class="over">' +  $(this).text() + '</span>').appendTo(this);
		});
		$(".menu li a").hover(function() {
			$(".out",this).stop().animate({'top':'60px'},300);
			$(".over",this).stop().animate({'top':'0px'},300);
		},function() {
			$(".out",this).stop().animate({'top':'0px'},300);
			$(".over",this).stop().animate({'top':'-60px'},300);
		});
        check_login();
	})
    
var loginedTemplate = "<span style='color:#B0D7F3;font-weight:700'><%= username %> has logged  &nbsp;&nbsp;<a href='javascript:logout()' style='color:#ECF044'>logout</a>";

  function check_login(){
    var username = $("#passed-username").attr("data");
    if(username){
      var content = _.template(loginedTemplate)({"username":username});
      $("#login-container").html(content);
      
    }else{
      var _t=   "<font size='3px' color='#FFFFFF' ></font><input type='text' style='width:20%' name='uname' id='uname'";
          _t+=  "placeholder='username'></input> ";
          _t+=  "<font size='3px' color='#FFFFFF' ></font><input type='password' style='width:20%' name='pw' id='pw' ";
          _t+=  "placeholder='password'></input> ";
          _t+=  "<button class='btn' name='login' id='btn-login' style='margin-top:-10px'>login</button>";

          $("#login-container").html(_t);
          $("#btn-login").click(login);$("#myTab").hide();$(".ul_div").hide();//
    }
    
  }

  function login () {
    var username = $("#uname").val(),password=$("#pw").val();
    if(!username || !password) return

    $.ajax({
        method: "POST",
        url: "/login",
        dataType:"json",
        data: { name: username, pw: password }
      }).done(function(response) {
          //console.log(response);
          if(response.status!=200){
            alert(response.message);
            return
          }
          var username = $("#uname").val();
          var content = _.template(loginedTemplate)({"username":username});

          $("#login-container").html(content);
          $("#myTab").show();$(".ul_div").show(); $("#login_name").val(username);
          location.reload();

      });
  }

  function logout () {

    $.ajax({
        method: "GET",
        url: "/logout",
        dataType:"json"
      }).done(function(response) {
          //console.log(response);
          if(response.status!=200){
            alert(response.message);
            return
          }
           var _t=   "<input type='text' name='uname' id='uname'";
          _t+=  "placeholder='username'></input> ";
          _t+=  " <input type='password' name='pw' id='pw' ";
          _t+=  "placeholder='password'></input> ";
          _t+=  "<button  name='login' id='btn-login' >login</button>";

          $("#login-container").html(_t);
          $("#btn-login").click(login);

          location.href = "/";
      });
  }