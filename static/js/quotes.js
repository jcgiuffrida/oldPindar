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
				quote.find('.btn-comments').removeClass('active');
				quote.find('.object-action .edit').fadeIn('fast');
				quote.find('.object-action').slideDown();
			}
		};

		var flag = function(){
			if (quote.find('.object-action .flag-submit').is(':visible')){
				quote.trigger('clear.quotify');
			} else {
				quote.trigger('clear.quotify');
				quote.find('.btn-comments').removeClass('active');
				quote.find('.object-action .flag-submit').fadeIn('fast');
				quote.find('.object-action').slideDown();
			}
		};

		var comments = function(){
			if (quote.find('.object-action .comments').is(':visible')){
				quote.trigger('clear.quotify');
			} else {
				quote.trigger('clear.quotify');
				var commentsdiv = $('<div class="list-group col-md-8"></div>');
				$.ajax({
					url: '/Pindar/default/getcomments?QuoteID='+quote.data('id'),
					type: 'GET',
					contentType: 'application/json',
					dataType: 'json',
					success: function(response) {
						// use fa icons to indicate to user what's going on
						if (response.status===200){
							comments = $('<div class="list-group col-md-8 col-md-offset-2"></div>');
							for (q in response.comments){
								c = response.comments[q];
								comment = '<li class="list-group-item"><p>' + c.text + '</p>';
								comment += '<p class="small"><a href="/Pindar/default/users/' + c.user + '">' + 
									c.user + '</a>, ' + c.timestamp + '</p></li>';
								comments.append(comment);
							}
							addcomment = '<li class="list-group-item mycomment"><form role="form"><div class="form-group">';
							addcomment += '<textarea class="form-control" id="commentfield" placeholder="Add your own comment..."></textarea>';
							addcomment += '</div><div class="form-group"><button class="btn btn-primary submit" type="button">Submit</button>';
							addcomment += ' <button class="btn btn-primary cancel" type="button">Cancel</button></div></form></li>';
							comments.prepend(addcomment);
							quote.find('.comments').html(comments);
							quote.find('.object-action .comments').fadeIn('fast');
							quote.find('.object-action').slideDown();
						} else {
							console.log(response);
							quote.find('.comments').html(response.msg);
						}
					},
					error: function(request, errorType, errorMessage) {
						// don't do anything with server errors yet
						quote.find('.comments').html('something went wrong');
					},
					timeout: 3000,
					beforeSend: function(){
						quote.find('.btn-comments i').removeClass('fa-comments').addClass('fa-spinner fa-spin');
					},
					complete: function(){
						quote.find('.btn-comments i').removeClass('fa-spinner fa-spin').addClass('fa-comments');
					}
				});
				
			}
		}

		quote.on('hide.quotify', hide);
		quote.on('clear.quotify', clear);
		quote.on('edit.quotify', edit);
		quote.on('flag.quotify', flag);
		quote.on('comments.quotify', comments);

		quote.on('click', '.button-edit', function(e){
			e.preventDefault();
			quote.trigger('edit.quotify');
		});

		quote.on('click', '.btn-comments', function(e){
			e.preventDefault();
			quote.trigger('comments.quotify');
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

		// cancel buttons
		quote.find('.object-action').on('click', '.cancel', function(e){
			e.preventDefault();
			quote.trigger('clear.quotify');
			quote.find('.btn-comments').removeClass('active');
		});

		// form to submit flag
		quote.find('.flag-submit').on('click', '.submit', function(e){
			e.preventDefault();
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
		});

		// submit a comment
		quote.on('click', '.mycomment .submit', function(e){
			e.preventDefault();
			if (user===0){
				alert("You must log in to do that!")
				var current = window.location;
				window.location.href = "/Pindar/default/user/login?_next=" + current;
			} else {
				var text = $(this).closest('.mycomment').find('textarea').val();
				var button = quote.find('.btn-comments');
				var submitButton = $(this);
				$.ajax({
					url: '/Pindar/default/addcomment?Text='+text+'&QuoteID='+quote.data('id'),
					type: 'POST',
					contentType: 'application/json',
					dataType: 'json',
					success: function(response) {
						if (response.status===200){
							var c = response.mycomment;
							comment = '<li class="list-group-item"><p>' + c.text + '</p>';
							comment += '<p class="small"><a href="/Pindar/default/users/' + c.user + '">' + 
							c.user + '</a>, ' + c.timestamp + '</p></li>';
							quote.find('.mycomment').fadeOut();
							quote.find('.comments .list-group').prepend(comment).fadeIn();
							var count = parseInt(button.find('span').html());
							button.find('span').html(count + 1);
						} else {
							submitButton.closest('.mycomment').append('<p class="text-warning">' + response.msg + '</p>');
							submitButton.html('Submit');
						}
					},
					error: function(request, errorType, errorMessage) {
							submitButton.html('<i class="fa fa-warning"></i>').removeClass('btn-primary').addClass('btn-warning');
					},
					timeout: 3000,
					beforeSend: function(){
						submitButton.html('<i class="fa fa-spinner fa-spin"></i> Working...');
					},
				});
			}

		})




		



		

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







