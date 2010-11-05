	function deletePost(id){
		$.ajax({
			type: "POST",
			data: 'id=' + id,
			url: '../delete',
			success: function(data) {
				if (data == 0) {
					alert('succes!');
					location.reload(true);
				}
				else alert('error!');
			}
		});
	}

function test() {
	alert('dfdfd');
}
