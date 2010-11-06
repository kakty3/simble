function login(name, pswd){
	$.ajax({
		type: "POST",
		data: 'username=' + name +'&password=' + pswd,
		url: './login',
		success: function(data) {
			if (data == 0) {
				alert('succes!');
				window.location = '/home';
			}
			else alert('error!');
		}
	});
}
