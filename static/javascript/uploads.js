$("#existingExpNames").change(function(){
	var val = $("#existingExpNames").val();
	console.log(val);
	$("#dirName").val(val);
})