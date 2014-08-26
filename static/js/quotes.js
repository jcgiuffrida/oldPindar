
$(document).ready(function(){
	$('.object-action').hide();
	$('.object-action>div').hide();
	$('.object').on('click', '.button-edit', function(){
		$(this).closest('.object').find('.flag-submit').hide();
		$(this).closest('.object').find('.edit').show();
		$(this).closest('.object').find('.object-action').slideToggle();
	});
	$('.btn-flag').on('click', 'a', function(e){
		e.preventDefault();
		var selection = $(this);
		var object = selection.closest('.object');
		var type = -1;
		if ($(this).hasClass('offensive')){
			type = 1;
		} else if ($(this).hasClass('incorrect')){
			type = 2;
		} else if ($(this).hasClass('duplicate')){
			type = 3;
		} else if ($(this).hasClass('flag')){
			type = 4;
		}
		if (type === 3 & user===0){
			// trigger login
			alert("You must log in to do that!")
			var current = window.location;
			window.location.href = "/Pindar/default/user/login?_next=" + current;
		} else {
			var label = '';
			if (type === 1){
				label = 'What is offensive about this quote?'
			} else if (type === 2){
				label = 'What is incorrect about this quote?'
			} else if (type === 3){
				label = 'Of what quote is this a duplicate?'
			} else if (type === 4){
				label = 'What is wrong about this quote?'
			}
			label += ' (Optional)';
			// show space for comment
			$('.flag-submit').find('label').text(label);
			object.find('.edit').hide();
			object.find('.flag-submit').show().data('type', type);
			object.find('.object-action').slideDown();
		}
	});
	$('.flag-submit').on('click', '.cancel', function(e){
		e.preventDefault();
		$(this).closest('.object-action').slideUp();
	});
	$('.flag-submit').on('click', '.submit', function(e){
		e.preventDefault();
		var form = $(this).closest('.flag-submit');
		// annoying but it seems we have to embed all data in the url for ajax requests
		// controller can't find anything in request.post_vars where it's supposed to be
		// also can't figure out how to return "success" or "error" from controller, except manually
		// in the json
		// also, we need to make this crap more extensible by incorporating it into a jquery plugin
		// this is a ridiculous amount of code
		var button = $(this).closest('.object').find('.btn-flag>.btn');
		$.ajax({
			url: '/Pindar/default/flag?Type='+form.data('type')+'&FlagNote='+
				form.find('textarea').val()+'&QuoteID='+form.closest('.object-action').data('id'),
			type: 'POST',
			contentType: 'application/json',
			dataType: 'json',
			success: function(response) {
				// use fa icons to indicate to user what's going on
				if (response.status===200){
					button.removeClass('btn-default').addClass('btn-danger').
						html('<i class="fa fa-flag"></i>').addClass('disabled');
				} else {
					button.html('<i class="fa fa-flag"></i> <i class="fa fa-exclamation-circle"></i>').
						removeClass('btn-default').addClass('btn-warning').addClass('disabled'); 
					// need to tell user what went wrong
				}
			},
			error: function(request, errorType, errorMessage) {
				// don't do anything with server errors yet
				button.html('<i class="fa fa-flag"></i> <i class="fa fa-exclamation-circle"></i>').
					removeClass('btn-default').addClass('btn-warning').addClass('disabled');
			},
			timeout: 3000,
			beforeSend: function(){
				button.closest('.object').find('.object-action').slideUp();
				button.find('ul').hide();
				button.html('<i class="fa fa-circle-o-notch fa-spin"></i> <i class="fa fa-caret-down"></i>');
					// pending icon
			}
		});
		
	});
});