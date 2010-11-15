function messageOut(){
	$(this).children().slice(2).hide()
}


function messageIn(){
	$(this).children().slice(2).show()
}

$(document).ready(function(){
	$('.message').hover(messageIn, messageOut)	
})
