$(document).ready(function(){
  $('.object').quotify();
  $('.object').trigger('clear.quotify');
});


$.fn.quotify = function(){
  this.each(function(){
    
    var quote = $(this);
    var commentAdded = false;
    var numComments = 0;
    if (quote.find('.btn-comments span').length > 0){
      var numComments = parseInt(quote.find('.btn-comments span').html());
    }
    var commentsLoaded = false;
    if (numComments === 0){
      commentsLoaded = true;
    }

    var hide = function(){
      quote.find('.object-results>div').fadeOut();
      quote.find('.object-results').slideUp();
    }

    var clear = function(){
      quote.find('.object-results>div').fadeOut();
      quote.find('.object-results').slideUp();
    }

    // allow editing
    var edit = function(){
      quote.trigger('clear.quotify');
      if (!quote.find('.object-results .edit').is(':visible')){
        quote.find('.btn-comments').removeClass('active');
        quote.find('.object-results .edit').fadeIn('fast');
        quote.find('.object-results').slideDown();
      }
    };

    var flag = function(){
      if (quote.find('.object-results .flag-submit').is(':visible')){
        quote.trigger('clear.quotify');
      } else {
        quote.trigger('clear.quotify');
        quote.find('.btn-comments').removeClass('active');
        quote.find('.object-results .flag-submit').fadeIn('fast');
        quote.find('.object-results').slideDown();
      }
    };

    // cancel buttons
    quote.find('.object-results').on('click', '.cancel', function(e){
      e.preventDefault();
      quote.trigger('clear.quotify');
      quote.find('.btn-comments').removeClass('active');
      if ($(this).closest('.flag-submit').length){
        quote.find('.btn-flag button').removeClass('disabled');
      }
    });

    // handlers
    quote.on('hide.quotify', hide);
    quote.on('clear.quotify', clear);
    quote.on('edit.quotify', edit);
    quote.on('flag.quotify', flag);
    
    quote.on('click', '.button-edit', function(e){
      e.preventDefault();
      quote.trigger('edit.quotify');
    });

    quote.on('click', '.btn-comments', function(e){
      e.preventDefault();
      quote.trigger('getComments.quotify');
    });
    
    quote.on('getComments.quotify', function(){
      quote.trigger('clear.quotify');
      if (!quote.find('.object-results .comments').is(':visible')){
        quote.trigger('loadComments.quotify');
      }
    });
    
    // load comments
    quote.on('loadComments.quotify', function(){
      var comments = $('.comments .list-group');
      quote.find('.object-results .comments').fadeIn('fast');
      quote.find('.object-results').slideDown();
      if (!commentsLoaded){
        $.ajax({
          url: '/Pindar/api/get_comments?QuoteID=' + quote.data('id'),
          type: 'POST',
          contentType: 'application/json',
          dataType: 'json',
          success: function(response) {
            for (q in response.comments){
              c = response.comments[q];
              comment = $('<li class="list-group-item"><p>' + c.text + 
                '</p><p class="small"><a href="/Pindar/default/users/' + 
                c.user + '">' + c.user + '</a>, ' + c.timestamp + 
                '</p></li>');
              comments.append(comment);
            }
            comments.find('li').eq(1).remove();
            commentsLoaded = true;
          },
          error: function(request, errorType, errorMessage) {
            quote.find('.comments div li:last').html(errorType + ": " + 
              errorMessage);
          },
          timeout: 5000,
          beforeSend: function(){
            var loading = $('<li class="list-group-item">' + 
              '<p class="text-center"><i class="fa fa-spinner fa-spin"></i>' +
              '</p></li>').appendTo(comments);
          }
        });
      }
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
          url: '/Pindar/api/comment?Text=' + text + '&QuoteID=' + 
            quote.data('id'),
          type: 'POST',
          contentType: 'application/json',
          dataType: 'json',
          success: function(response) {
            var c = response.mycomment;
            comment = '<li class="list-group-item"><p>' + c.text + '</p>';
            comment += '<p class="small"><a href="/Pindar/default/users/' + 
              c.user + '">' + c.user + '</a>, ' + c.timestamp + '</p></li>';
            quote.find('.mycomment').hide();
            quote.find('.comments .list-group').prepend(comment).show();
            numComments += 1;
            button.find('span').html(numComments).show();
            commentAdded = true;
          },
          error: function(request, errorType, errorMessage) {
              submitButton.closest('.mycomment').
                append('<p class="text-warning">' + errorType + ': ' + 
                  errorMessage + '</p>');
              submitButton.html('Submit');
          },
          timeout: 3000,
          beforeSend: function(){
            submitButton.html('<i class="fa fa-spinner fa-spin"></i> ' + 
              'Working...');
          },
        });
      }
    })
    
    // drop-down to flag quote
    quote.on('click.quotify', '.btn-flag a', function(e){
      e.preventDefault();
      var selection = $(this);
      var type = -1;
      var label = '';
      if ($(this).hasClass('offensive')){
        type = 1;
        label = 'What is offensive about this quote?'
      } else if ($(this).hasClass('incorrect')){
        type = 2;
        label = 'What is incorrect about this quote?'
      } else if ($(this).hasClass('duplicate')){
        type = 3;
        label = 'Of what quote is this a duplicate?'
      } else if ($(this).hasClass('flag')){
        type = 4;
        label = 'What is wrong with this quote?'
      }
      label += ' (Optional)';
      if (type === 3 & user===0){
        // trigger login
        alert("You must log in to do that!")
        var current = window.location;
        window.location.href = "/Pindar/default/user/login?_next=" + current;
      } else {
        // show space for comment
        $('.flag-submit').find('label').text(label);
        quote.find('.flag-submit').data('type', type);
        selection.closest('.btn-flag').find('button').addClass('disabled');
        quote.trigger('flag.quotify');
      }
    });

    // submit a flag
    quote.find('.flag-submit').on('click', '.submit', function(e){
      e.preventDefault();
      var form = $(this).closest('.flag-submit');
      var button = quote.find('.btn-flag>.btn');
      $.ajax({
        url: '/Pindar/api/flag?Type=' + form.data('type') + '&FlagNote=' +
          form.find('textarea').val() + '&QuoteID=' + quote.data('id'),
        type: 'POST',
        contentType: 'application/json',
        dataType: 'json',
        success: function(response) {
          button.removeClass('btn-default').addClass('btn-danger').
            html('<i class="fa fa-flag"></i>');
          button.closest('.btn-flag').attr('title', 'You flagged this quote');
        },
        error: function(request, errorType, errorMessage) {
          console.log(errorType + ': ' + errorMessage);
          button.html('<i class="fa fa-flag"></i> ' + 
            '<i class="fa fa-exclamation-circle"></i>').
            removeClass('btn-default').addClass('btn-warning');
        },
        timeout: 3000,
        beforeSend: function(){
          quote.trigger('clear.quotify');
          button.find('ul').hide();
          button.html('<i class="fa fa-circle-o-notch fa-spin"></i> ' + 
            '<i class="fa fa-caret-down"></i>');
        }
      });
    });

    // rate: dropdown on hover
    quote.find('.btn-rate').hover(function(){
      $(this).find('ul').stop(true, true).slideDown('fast');
    }, function(){
      $(this).find('ul').stop(true, true).slideUp('fast');
    });


    // rate
    quote.find('.btn-rate').on('click', 'span.star', function(e){
      e.preventDefault();
      var button = $(this).closest('.btn-rate').find('button');
      if (user === 0){
        alert("You must log in to do that!")
        var current = window.location;
        window.location.href = "/Pindar/default/user/login?_next=" + current;
      } else {
        var rating = $(this).data('star');
        $.ajax({
          url: '/Pindar/api/rate?Rating=' + $(this).data('star') + 
            '&QuoteID=' + quote.data('id'),
          type: 'POST',
          contentType: 'application/json',
          dataType: 'json',
          success: function(response) {
            button.removeClass('btn-default').addClass('btn-success');
            button.html('Rate <i class="fa fa-caret-down"></i>');
            quote.find('.btn-rate span.star').removeClass('starred');
            for (i = 1; i <= rating; i++){
              quote.find('.btn-rate span.star[data-star=' + i + 
                ']').addClass('starred');
            }
            quote.find('.btn-rate').off('click'); // turn off
          },
          error: function(request, errorType, errorMessage) {
            button.html('Rate <i class="fa fa-exclamation-circle"></i>').
                removeClass('btn-default').addClass('btn-warning').
                  addClass('disabled');
            console.log(errorType + ': ' + errorMessage);
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







