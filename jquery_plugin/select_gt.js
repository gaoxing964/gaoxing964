$.fn.selectGt = (function() {
	var ready = false;
	var domID = 'selectUserContainer';
	var displayName = 'displayNone';
	var that = this;
	var cssText = '';
	cssText = cssText + '  .displayNone { display:none } '
	cssText = cssText + '#' + domID + ' { position:absolute; z-index:9; background:white;} ';
	cssText = cssText + '#' + domID + ' li:hover { cursor:pointer; background:#E0E0E0;}';
	cssText = cssText + '#' + domID + ' li {padding-left:10px;}';
	cssText = cssText + '#' + domID + ' ul{ margin-left:0px;list-style:none;margin-left: 0px;padding-left: 0px;margin-top: 0px;margin-bottom: 0px;}';
	
	var createStyle = function(styleText) {
		var style = document.createElement('style');
		style.type = 'text/css';
		try {
			style.appendChild(document.createTextNode(styleText));
		} catch (ex) {
			style.stylesheet.cssText = styleText;
		}
		var head = document.getElementsByTagName('head')[0];
		head.appendChild(style);
	}
	var MAX_ITEM = 10;
	var timeSet;
	var timeRange = 200;

	return function(datas, url) {

		var that = this;

		var initFun = function() {
			var div = $('<div>');
			div.addClass(displayName);
			div.attr('id', domID);
			div.append($('<ul>'));
			$('body').append(div);
			createStyle(cssText);
		}
		if (!ready) {
			initFun();
		}
		ready = true;

		var showFun = function() {
			var left = $(that).offset().left;
			var top = $(that).offset().top;
			var width = $(that).width();
			var height = $(that).height();
			$('#' + domID).removeClass('displayNone');
			$('#' + domID).css({
				'left': left + 'px',
				top: top + (height+6) + 'px',
				width: width + 'px'
			});
		}
		var hideFun = function() {
			$('#' + domID).addClass('displayNone');
		}

		var listFun = function(dataLocal) {
			var d = dataLocal;
			$('#' + domID).find('ul').html('');
			var i = 0;
			d.forEach(function(item) {
				if (i > MAX_ITEM) {
					return;
				}
				i++;
				var li = $('<li>').attr('value', item.value).text(item.label);
				li.click(function() {
					var us = $(that).val();
					us = us.split(',');
					us = us.map(function(u) {
						return $.trim(u);
					});
					if (us.length) {
						us.pop();
					}
					us = us.filter(function(u) {
						if ($.trim(u)) {
							return true;
						}
					});
					us.push($(this).attr('value'));
					us = us.join(',');
					$(that).val(us);
					$(that).trigger('input');
					hideFun();
				});
				$('#' + domID).find('ul').append(li);
			});
		}

		$(this).keyup(function() {
			showFun();
			var us = $(this).val();
			us = us.split(',');
			var username = us[us.length - 1];
			clearTimeout(timeSet);
			timeSet = setTimeout(function() {
				if (url) {
					$.ajax({
						type: "get",
						url: url,
						data: {
							param: username
						},
						success: function(response) {
							var response = eval('(' + response + ')');
							if (response.state == 200) {
								var datas = response.data.map(function(item) {
									return {
										label: item ,
										value: item 
									}
								});
								var ds = datas.filter(function(item) {
									if (item.label.toLowerCase().indexOf(username) != -1) {
										return true;
									}
								});
								listFun(ds);
							}
						}
					});
				} else {
					var ds = datas.filter(function(item) {
						if (item.label.toLowerCase().indexOf(username) != -1) {
							return true;
						}
					});
					listFun(ds);
				}
			}, timeRange);

		});

		$(this).blur(function() {
			setTimeout(function() {
				hideFun();
			}, 250);
		});

	}
})();