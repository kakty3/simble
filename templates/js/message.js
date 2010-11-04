	function deletePost(id){
		$.ajax({
			type: "POST",
			data: 'id=' + id,
			url: '../delete',
			success: function(data) {
				alert('succes!');
				location.reload(true);
			}
		});
	}

function test() {
	alert('dfdfd');
}
