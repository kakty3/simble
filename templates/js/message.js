function deletePost(id){
	$.ajax({
		type: "POST",
		data: 'id=' + id,
		url: '../delete',
		success: function(data) {
			if (data == 0) {
				//alert('succes!');
				$('#' + id).fadeOut(500);
				//location.reload(true);
			}
			else alert('error!');
		}
	});
}


function newPost(input){
	alert(input);
	$.ajax({
		type: "POST",
		data: input,
		url: '../post',
		success: function(data) {
			if (data == 0) {
				alert('succes!');
				//$('#' + id).fadeOut(500);
				//location.reload(true);
			}
			else alert('error!');
		}
	});
}
