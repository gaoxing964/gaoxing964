var query_param = {};

function queryHandler(param) {
	param["parents_id"] = query_param["parents_id"];

	param["author"] = query_param["author"];
	param["owner"] = query_param["owner"];
	param["is_solved"] = query_param["is_solved"];
	//console.log(param);
	return param

}
