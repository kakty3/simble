function login(name, pswd){
	$.ajax({
		type: "POST",
		data: 'username=' + name +'&password=' + pswd,
		url: '../login',
		success: function(data) {
			if (data == 0) {
				alert('succes!');
				location.reload(true);
			}
			else alert('error!');
		}
	});
}
