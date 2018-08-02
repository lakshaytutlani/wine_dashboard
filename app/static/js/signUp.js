$(function(){
	$('#btnSignUp').click(function(){
		
		$.ajax({
			url: '/signUp',
			data: $('form').serialize(),
			type: 'POST',
			success: function(response){
				bootbox.alert(response);
                
			},
			error: function(error){
				bootbox.alert(error);
			}
		});
	});
});