$(document).ready(function(){
	$('.object').quotify();
	$('.object').trigger('clear.quotify');
});


$.fn.quotify = function(){
	this.each(function(){
		var quote = $(this);
		

		var hide = function(){
			quote.find('.object-action>div').fadeOut();
			quote.find('.object-action').slideUp();
		}

		var clear = function(){
			quote.find('.object-action>div').fadeOut();
			quote.find('.object-action').slideUp();
		}

		// allow editing
		var edit = function(){
			if (quote.find('.object-action .edit').is(':visible')){
				quote.trigger('clear.quotify');
			} else {
				quote.trigger('clear.quotify');
				quote.find('.object-action .edit').fadeIn('fast');
				quote.find('.object-action').slideDown();
			}
		};

		var flag = function(){
			if (quote.find('.object-action .flag-submit').is(':visible')){
				quote.trigger('clear.quotify');
			} else {
				quote.trigger('clear.quotify');
				quote.find('.object-action .flag-submit').fadeIn('fast');
				quote.find('.object-action').slideDown();
			}
		};

		quote.on('hide.quotify', hide);
		quote.on('clear.quotify', clear);
		quote.on('edit.quotify', edit);
		quote.on('flag.quotify', flag);

		quote.on('click', '.button-edit', function(e){
			e.preventDefault();
			quote.trigger('edit.quotify');
		});
		
		// drop-down to flag quote
		quote.on('click.quotify', '.btn-flag a', function(e){
			e.preventDefault();
			var selection = $(this);
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
				quote.find('.flag-submit').data('type', type);
				quote.trigger('flag.quotify');
			}
		});

		// form to submit flag
		quote.find('.flag-submit').on('click', 'button', function(e){
			e.preventDefault();
			if ($(this).hasClass('cancel')){
				quote.trigger('clear.quotify');;
			} else {
				var form = $(this).closest('.flag-submit');
				var button = quote.find('.btn-flag>.btn');
				$.ajax({
					url: '/Pindar/default/flag?Type='+form.data('type')+'&FlagNote='+
						form.find('textarea').val()+'&QuoteID='+quote.data('id'),
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
							console.log(response);
							alert(response.msg);
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
						quote.trigger('clear.quotify');
						button.find('ul').hide();
						button.html('<i class="fa fa-circle-o-notch fa-spin"></i> <i class="fa fa-caret-down"></i>');
					}
				});
			}
			
		});

		quote.find('.btn-rate').on('click', 'span.star', function(e){
			e.preventDefault();
			var button = $(this).closest('.btn-rate').find('button');
			if (user === 0){
				alert("You must log in to do that!")
				var current = window.location;
				window.location.href = "/Pindar/default/user/login?_next=" + current;
			} else {
				$.ajax({
					url: '/Pindar/default/rate?Rating='+$(this).data('star')+'&QuoteID='+
						quote.data('id'),
					type: 'POST',
					contentType: 'application/json',
					dataType: 'json',
					success: function(response) {
						if (response.status===200){
							button.removeClass('btn-default').addClass('btn-success');
							button.html('Rate <i class="fa fa-caret-down"></i>');
						} else {
							button.html('Rate <i class="fa fa-exclamation-circle"></i>').
								removeClass('btn-default').addClass('btn-warning').addClass('disabled'); 
							console.log(response);
							alert(response.msg);
						}
					},
					error: function(request, errorType, errorMessage) {
						// don't do anything with server errors yet
						button.html('Rate <i class="fa fa-exclamation-circle"></i>').
								removeClass('btn-default').addClass('btn-warning').addClass('disabled');
					},
					timeout: 3000,
					beforeSend: function(){
						button.html('Rate <i class="fa fa-circle-o-notch fa-spin"></i>');
					}
				});
			}
		});
	});
};







