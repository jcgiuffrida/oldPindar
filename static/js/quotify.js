/* 

quotify takes a quotes, authors, or works object output by one of 
the tools.js 'Parse' functions and turns it into a fully functioning object.

*/



$.fn.quotify = function(options){

  var settings = $.extend({ size: 'small', 
    auth: !!user, objectType: 'quote' }, options);

  /********************
          ELEMENT CONSTRUCTORS  
  ********************/

  var constructBtnEditElement = function(){
    var element = '<div class="btn-group">' + 
      '<button class="btn btn-default btn-edit">Edit</button>' + 
      '<button type="button" class="btn btn-default dropdown-toggle"' +
      'data-toggle="dropdown"><span class="caret"></span></button>' + 
      '<ul class="dropdown-menu" role="menu">' + 
      '<li><a href="#" class="btn-edit-history">' + 
      'See past versions</a></li></ul></div>';
    return $(element); };
  var constructBtnFlagElement = function(type, size){
    if (size == 'large'){
      var element = '<div class="btn-group btn-flag">' + 
        '<button type="button" class="btn btn-default dropdown-toggle" ' + 
        'data-toggle="dropdown"><i class="fa fa-flag"></i> ' + 
        '<i class="fa fa-caret-down"></i></button>';
    } else {
      var element = '<div class="btn-group btn-goto-flag">' + 
        '<a class="dropdown-toggle" data-toggle="dropdown">' + 
        '<i class="fa fa-flag"></i></a>';
    }
    element += '<ul class="dropdown-menu" role="menu">' + 
      '<li><a href="#" class="flag" data-type="1">' + 
      'This ' + type + ' is offensive</a></li>' + 
      '<li><a href="#" class="flag" data-type="2">' + 
      'This ' + type + ' is not correct</a></li>' + 
      '<li><a href="#" class="flag" data-type="3">' + 
      'This ' + type + ' is a duplicate</a></li>' + 
      '<li><a href="#" class="flag" data-type="4">' + 
      'Something else...</a></li></ul></div>';
    return $(element); };
  var constructRateElement = function(type, size){
    var element = '<div class="sum-ratings ';
    if (type == 'quote'){
      element += 'pull-left ' + size + '"><div class="ratings-box">' + 
      '<div class="star-ratings-user">' + 
      '<span data-star="5" class="star"></span>' + 
      '<span data-star="4" class="star"></span>' + 
      '<span data-star="3" class="star"></span>' + 
      '<span data-star="2" class="star"></span>' + 
      '<span data-star="1" class="star"></span></div>';
    } else {
      element += 'pull-right ' + size + '"><div class="ratings-box">';
    }
    element += '<div class="star-ratings-top">' + 
      '<span class="star"></span>' + 
      '<span class="star"></span>' + 
      '<span class="star"></span>' + 
      '<span class="star"></span>' + 
      '<span class="star"></span></div>' + 
      '<div class="star-ratings-bottom">' + 
      '<span class="star"></span>' + 
      '<span class="star"></span>' + 
      '<span class="star"></span>' + 
      '<span class="star"></span>' + 
      '<span class="star"></span></div></div>' + 
      '<div class="ratings-count"></div></div>';
    return $(element); };
  var constructBtnCommentsElement = function(size, comment_count){
    if(typeof(comment_count)==='undefined') comment_count = 0;
    if (size == 'large'){
      var element = '<button type="button" class="btn btn-default btn-comments">'+
        '<i class="fa fa-comments"></i> <span class="badge" ';
      if (comment_count == 0){
        element += 'style="display:none;"';
      }
      element += '>' + comment_count + '</span></button>';
    } else {
      var element = '<div><a class="btn-goto-comments">' + 
        '<i class="fa fa-comments"></i></a></div>';
    }
    return $(element); };
  var constructEditHistoryElement = function(){
    var element = '<div class="row edit-history" style="display:none;">' + 
      '<div class="col-md-12"></div></div>';
    return $(element); };
  var constructFlagElement = function(){
    var element = '<div class="row flag-submit" style="display:none;">' + 
      '<div class="col-md-12"><form role="form"><div class="form-group">' + 
      '<label for="complaint"></label>' + 
      '<textarea class="form-control" id="complaint" ' + 
      'placeholder="Add a comment..."></textarea></div>' + 
      '<div class="form-group">' + 
      '<button class="btn btn-primary submit" type="button">Submit</button> ' + 
      '<button class="btn btn-default cancel" type="button">Cancel</button>' + 
      '</div></form></div></div>';
    return $(element); };
  var constructCommentsElement = function(auth, type, id){
    var element = '<div class="row comments" style="display:none;">' + 
      '<div class="list-group col-md-8 col-md-offset-2">';
    if (auth){
      element += '<li class="list-group-item mycomment">' + 
        '<form role="form"><div class="form-group">' + 
        '<textarea class="form-control" id="commentfield"' + 
        'placeholder="Add your own comment..."></textarea></div>' + 
        '<div class="form-group">' + 
        '<button class="btn btn-primary submit" type="button">Submit</button>' + 
        ' <button class="btn btn-default cancel" type="button">Cancel</button>' + 
        '</div></form></li>';
    } else {
      element += '<a class="list-group-item mycomment text-center" ' + 
        'href="/Pindar/default/user/login?_next=' + 
        '/Pindar/default/' + type + 's/' + id + '?comments=true">' + 
        'Please log in to add your own comment.</a>'; 
    }
    element += '</div></div>';
    return $(element); };


  this.each(function(){
    
    /********************
          INITIALIZE  
    ********************/
    
    var object = $(this);

    var objectActions = object.find('.object-actions');
    var objectResults = object.find('.object-results');


    /********************
          ADD APPROPRIATE ELEMENTS  
    ********************/
    
    
    objectActions.append(constructRateElement(settings.objectType,
      settings.size));
    if (settings.objectType == 'quote'){
      if (settings.size == 'large'){
        objectActions.append(constructBtnCommentsElement(
           settings.size, object.data('comments')));
        objectResults.append(constructCommentsElement(settings.auth,
          settings.objectType, object.data('id')));
      } else {
        objectActions.append(constructBtnCommentsElement(settings.size));  
      }
    }
    if (settings.auth & settings.size == 'large'){
      objectActions.append(constructBtnEditElement());
      objectResults.append(constructEditHistoryElement());
    }
    objectActions.append(constructBtnFlagElement(settings.objectType,
      settings.size));
    if (settings.size == 'large'){
      objectResults.append(constructFlagElement());
    }
    

    /********************
          BASIC FUNCTIONALITY
    ********************/

    var commentAdded = false;
    var numComments = object.data('comments');
    var commentsLoaded = (numComments == 0 ? true : false);
    var flagged = false;

    // clear and hide object results
    var clear = function(){
      object.find('.object-results>div').fadeOut();
      objectResults.slideUp();
      objectActions.find('.btn').removeClass('active').
        removeClass('disabled').blur();
      if (flagged){
        objectActions.find('.btn-flag>.btn').addClass('disabled');
      }
    }

    // show object actions on mouseover (for small objects)
    if (settings.size == 'small' & settings.objectType == 'quote'){
      object.on('mouseover', function(){
        objectActions.children('div').show();
      });
      object.on('mouseleave', function(){
        objectActions.children('div').hide();
      });
      objectActions.children('div').hide();
    }


    // on clicking quote, take user to quote page
    object.on('click', '.text', function(){
      window.location.href = '/Pindar/default/quotes/' + 
        object.data('id');
    });

    // handlers
    object.on('clear.quotify', clear);
    
    // cancel buttons
    objectResults.on('click', '.cancel', function(e){
      e.preventDefault();
      object.trigger('clear.quotify');
    });


    /********************
          EDITING
    ********************/

    var edit = function(){
      var visible = objectResults.find('.edit').is(':visible');
      object.trigger('clear.quotify');
      if (!visible){
        objectResults.find('.edit').fadeIn('fast');
        objectResults.slideDown();
        objectActions.find('.btn-edit').addClass('active');
        objectResults.find('.btn-append-edit-history').show();
      }
    };
    object.on('edit.auth', edit);

    objectActions.on('click', '.btn-edit', function(e){
      e.preventDefault();
      if (settings.auth){
        object.trigger('edit.auth');
      } else if (confirm("You must log in to do that!")){
        var current = window.location;
        window.location.href = "/Pindar/default/user/login?_next=" + current;
      }
    });

    // submit edit
    objectResults.on('click.auth', '#edit-submit', function(e){
      e.preventDefault();
      $(this).addClass('disabled');
      // add verifications here
      var call = '';
      if (settings.objectType == 'quote'){
        call = '/Pindar/api/edit_quote?' + 
          'QuoteID=' + object.data('id') + 
          '&Text=' + $('#QUOTE-Text').val().sanitize() + 
          '&QuoteLanguageID=' + $('#QUOTE-QuoteLanguageID').val() + 
          '&IsOriginalLanguage=' + $('#QUOTE-IsOriginalLanguage').val() + 
          '&Note=' + $('#QUOTE-Note').val().sanitize();
      } else if (settings.objectType == 'author'){
        call = '/Pindar/api/edit_author?' + 
          'AuthorId=' + object.data('author-id') + 
          '&AuthorTrId=' + object.data('author-tr-id') + 
          '&FirstName=' + $('#AUTHOR_TR-FirstName').val() + 
          '&MiddleName=' + $('#AUTHOR_TR-MiddleName').val() + 
          '&LastName=' + $('#AUTHOR_TR-LastName').val() + 
          '&DisplayName=' + $('#AUTHOR_TR-DisplayName').val() + 
          '&Biography=' + $('#AUTHOR_TR-Biography').val()+
          '&WikipediaLink=' + $('#AUTHOR_TR-WikipediaLink').val() + 
          '&YearBorn=' + $('#AUTHOR-YearBorn').val() + 
          '&YearDied=' + $('#AUTHOR-YearDied').val();
      } else if (settings.objectType == 'work'){
        call = '/Pindar/api/edit_work?' + 
          'WorkId=' + object.data('work-id') + 
          '&WorkTrId=' + object.data('work-tr-id') + 
          '&WorkName=' + $('#WORK_TR-WorkName').val() + 
          '&WorkSubtitle=' + $('#WORK_TR-WorkSubtitle').val() + 
          '&WorkDescription=' + 
          $('#WORK_TR-WorkDescription').val() + 
          '&WikipediaLink=' + $('#WORK_TR-WikipediaLink').val() + 
          '&YearPublished=' + $('#WORK-YearPublished').val() + 
          '&YearWritten=' + $('#WORK-YearWritten').val();
      }
      $.getJSON(call, function(response){ 
          location.reload();
      }).error(function(e){
        $('.edit>div').append(e.responseText);
      });
    });



    /********************
          EDIT HISTORY
    ********************/

    objectResults.find('.edit').append(
      '<div class="col-md-6 col-md-offset-3">'+
      '<a class="btn btn-default btn-block ' + 
      'btn-append-edit-history">Show edit history</a></div>');

    var editHistory = function(){
      var editHistoryDiv = objectResults.find('.edit-history');
      var editHistoryDivDiv = objectResults.find('.edit-history>div');
      var visible = editHistoryDiv.is(':visible');
      var editVisible = objectResults.find('.edit').is(':visible');
      if (!editVisible & !visible){  // don't clear if only edit form shows
        object.trigger('clear.quotify');
      }
      objectResults.find('.btn-append-edit-history').hide();
      objectActions.find('.btn-edit-history').
        closest('.btn-group').find('.dropdown-toggle').addClass('disabled');
      editHistoryDiv.fadeIn('fast');
      objectResults.slideDown();
      editHistoryDivDiv.html('<span><i class="fa fa-spinner ' + 
          'fa-spin"></i></span>');
      $.getJSON('/Pindar/api/get_edit_history?' + 
        settings.objectType.capitalize() + 'ID=' + object.data('id'),
        function(response){
          var table = '<table>';
          table += '<thead><tr><th>';
          if (settings.objectType == 'quote'){
            table += 'Text</th><th>Context</th>';
          } else if (settings.objectType == 'author'){
            table += 'Name</th><th>Full Name</th>';
          } else if (settings.objectType == 'work'){
            table += 'Title</th><th>Subtitle</th>';
          } 
          table += '<th>User</th><th>Modified</th></tr></thead>';
          var row = '';
          // the current record
          for (c in response.current){
            h = response.current[c];
            row = '<tr class="current"><td>';
            if (settings.objectType == 'quote'){
              row += h.QUOTE.Text + '</td><td>' + h.QUOTE.Note;
            } else if (settings.objectType == 'author'){
              row += h.AUTHOR_TR.DisplayName + '</td><td>' + 
                h.AUTHOR_TR.FirstName + ' ' + 
                h.AUTHOR_TR.MiddleName + ' ' + 
                h.AUTHOR_TR.LastName;
            } else if (settings.objectType == 'work'){
              row += h.WORK_TR.WorkName + '</td><td>' + 
                h.WORK_TR.WorkSubtitle;
            } 
            row += '</td><td><a href="/Pindar/default/users/' + 
              h.auth_user.username + '">' + h.auth_user.username + '</td><td>';
            if (settings.objectType == 'quote'){
              row += h.QUOTE.modified_on + '</td></tr>';
            } else if (settings.objectType == 'author'){
              row += h.AUTHOR_TR.modified_on + '</td></tr>';
            } else if (settings.objectType == 'work'){
              row += h.WORK_TR.modified_on + '</td></tr>';
            } 
            table += row;
          }
          // all past edits
          for (c in response.past){
            h = response.past[c];
            row = '<tr><td>';
            if (settings.objectType == 'quote'){
              row += h.QUOTE_archive.Text + '</td><td>' + h.QUOTE_archive.Note;
            } else if (settings.objectType == 'author'){
              row += h.AUTHOR_TR_archive.DisplayName + '</td><td>' + 
                h.AUTHOR_TR_archive.FirstName + ' ' + 
                h.AUTHOR_TR_archive.MiddleName + ' ' + 
                h.AUTHOR_TR_archive.LastName;
            } else if (settings.objectType == 'work'){
              row += h.WORK_TR_archive.WorkName + '</td><td>' + 
                h.WORK_TR_archive.WorkSubtitle;
            } 
            row += '</td><td><a href="/Pindar/default/users/' + 
              h.auth_user.username + '">' + h.auth_user.username + '</td><td>';
            if (settings.objectType == 'quote'){
              row += h.QUOTE_archive.modified_on + '</td></tr>';
            } else if (settings.objectType == 'author'){
              row += h.AUTHOR_TR_archive.modified_on + '</td></tr>';
            } else if (settings.objectType == 'work'){
              row += h.WORK_TR_archive.modified_on + '</td></tr>';
            } 
            table += row;
          }
          table += '</tbody></table>';
          table += '<div class="form-group col-md-2">' + 
            '<button class="btn btn-default cancel" type="button">' + 
                'Done</button></div>';
          editHistoryDivDiv.html(table);
          $('.edit-history table').DataTable({
            "dom": '<t>ip',
            "ordering": false,
            "iDisplayLength": 5
          });
          editHistoryDivDiv.find('table').addClass('stripe row-border');
      }).error(function(e){
        editHistoryDivDiv.html(e.responseText);
      });
    };
    object.on('editHistory.auth', editHistory);

    objectActions.on('click.quotify', '.btn-edit-history', function(e){
      e.preventDefault();
      if (!$('.edit-history').is(':visible')){
        object.trigger('editHistory.auth');
      }
    });

    objectResults.on('click', '.btn-append-edit-history', function(e){
      e.preventDefault();
      object.trigger('editHistory.auth');
    })


    /********************
          FLAGGING
    ********************/

    var flag = function(){
      var visible = objectResults.find('.flag-submit').is(':visible');
      object.trigger('clear.quotify');
      if (!visible){
        objectResults.find('.flag-submit').fadeIn('fast');
        objectResults.slideDown();
        objectActions.find('.btn-flag button').addClass('disabled');
      }
    };
    object.on('flag.quotify', flag);

    objectActions.on('click.quotify', '.btn-flag ul a', function(e){
      e.preventDefault();
      var selection = $(this);
      var type = $(this).data('type');
      var label = '';
      if (type == 1){
        label = 'What is offensive about this ' + settings.objectType + '?';
      } else if (type == 2){
        label = 'What is incorrect about this ' + settings.objectType + '?';
      } else if (type == 3){
        label = 'Of what ' + settings.objectType + ' is this a duplicate?';
      } else if (type == 4){
        label = 'What is wrong with this ' + settings.objectType + '?';
      }
      label += ' (Optional)';
      // show space for comment
      objectResults.find('.flag-submit').data('type', type).
        find('label').text(label);
      object.trigger('flag.quotify');
    });
    
    // go to object page with flag open
    objectActions.on('click.quotify', '.btn-goto-flag ul a', function(e){
      e.preventDefault();
      window.location.href = '/Pindar/default/' + settings.objectType + 
        's/' + object.data('id') + '?flagType=' + $(this).data('type');
    })

    // submit a flag
    object.find('.flag-submit').on('click', '.submit', function(e){
      e.preventDefault();
      var form = $(this).closest('.flag-submit');
      var button = object.find('.btn-flag>.btn');
      var call = '/Pindar/api/flag?Type=' + form.data('type') + '&FlagNote=' +
        form.find('textarea').val() + '&' + 
        settings.objectType.capitalize() + 'ID=' + object.data('id');
      $.getJSON('/Pindar/api/flag?Type=' + form.data('type') + '&FlagNote=' +
        form.find('textarea').val() + '&' + 
        settings.objectType.capitalize() + 'ID=' + object.data('id'),
        function(response) {
          button.removeClass('btn-default').addClass('btn-danger').
            html('<i class="fa fa-flag"></i>');
          button.closest('.btn-flag').attr('title', 'You flagged this ' + 
            settings.objectType);
      }).error(function(e){
        console.log(e.responseText);
        button.html('<i class="fa fa-flag"></i> ' + 
          '<i class="fa fa-exclamation-circle"></i>').
          removeClass('btn-default').addClass('btn-warning');
      });
      object.off('flag.quotify');
      flagged = true;
      object.trigger('clear.quotify');
      button.html('<i class="fa fa-circle-o-notch fa-spin"></i> ' + 
        '<i class="fa fa-caret-down"></i>');
    });
    
    
    /********************
          COMMENTING
    ********************/

    // load comments
    object.on('loadComments.quotify', function(){
      var visible = objectResults.find('.comments').is(':visible');
      object.trigger('clear.quotify');
      if (!visible){
        var comments = $('.comments .list-group');
        objectResults.find('.comments').fadeIn('fast');
        objectResults.slideDown();
        objectActions.find('.btn-comments').addClass('active');
        if (!commentsLoaded){
          $('<li class="list-group-item">' + 
            '<p class="text-center"><i class="fa fa-spinner fa-spin"></i>' +
            '</p></li>').appendTo(comments);
          $.getJSON('/Pindar/api/get_comments?QuoteID=' + object.data('id'),
            function(response) {
            for (q in response.comments){
              c = response.comments[q];
              comment = $('<li class="list-group-item"><p>' + c.text + 
                '</p><p class="small"><a href="/Pindar/default/users/' + 
                c.user + '">' + c.user + '</a>, ' + c.timestamp + 
                '</p></li>');
              comments.append(comment);
            }
            comments.find('.list-group-item').eq(1).remove();
            commentsLoaded = true;
          });
        }
      }
    });

    objectActions.on('click.quotify', '.btn-comments', function(e){
      e.preventDefault();
      object.trigger('loadComments.quotify');
    });
    
    // go to object page with comments open
    objectActions.on('click.quotify', '.btn-goto-comments', function(e){
      e.preventDefault();
      window.location.href = '/Pindar/default/' + settings.objectType + 
        's/' + object.data('id') + '?comments=true';
    })

    // submit a comment
    objectResults.on('click', '.mycomment .submit', function(e){
      e.preventDefault();
      if (!settings.auth){
        if (confirm("You must log in to do that!")){
          var current = window.location;
          window.location.href = "/Pindar/default/user/login?_next=" + current;
        }
      } else {
        var text = $(this).closest('.mycomment').find('textarea').val().
          replace('\n', '<br>');
        var button = objectActions.find('.btn-comments');
        var submitButton = $(this);
        submitButton.html('<i class="fa fa-spinner fa-spin"></i> ' + 
          'Working...');
        $.getJSON('/Pindar/api/comment?Text=' + text + '&QuoteID=' + 
          object.data('id'), function(response) {
          var c = response.mycomment;
          comment = '<li class="list-group-item"><p>' + c.text + '</p>';
          comment += '<p class="small"><a href="/Pindar/default/users/' + 
            c.user + '">' + c.user + '</a>, ' + c.timestamp + '</p></li>';
          object.find('.mycomment').hide();
          object.find('.comments .list-group').prepend(comment).show();
          numComments += 1;
          button.find('span').html(numComments).show();
          commentAdded = true;
        });
      }
    })
    
    
    /********************
          RATING
    ********************/

    objectActions.find('.ratings-box').on('mouseenter', function(){
      $(this).find('.star-ratings-user').css('z-index', '2');
    });
    objectActions.find('.ratings-box').on('mouseleave', function(){
      $(this).find('.star-ratings-user').css('z-index', '-1');
    });

    // show current rating
    var updateSumRating = function(newRating, newCount){
      var ratingAsWidth = newRating / 0.05;
      objectActions.find('.star-ratings-top').css('width', ratingAsWidth + '%');  
      if (settings.objectType == 'author' | settings.objectType == 'work'){
        objectActions.find('.sum-ratings').attr('title', 'Average rating: ' + 
          parseFloat(newRating).toFixed(1) + ', based on ' + newCount + ' rating' + plural(newCount));
      }
      if (settings.size == 'large' & settings.objectType == 'quote'){
        objectActions.find('.ratings-count').html(newCount);
      }
      if (settings.objectType == 'quote'){
        if (object.data('rating-user')){
          // pass
        }
      }
    };
    updateSumRating(object.data('rating'), object.data('rating-count'));

    // update user rating
    var updateUserRating = function(rating){
      objectActions.find('.star-ratings-user span.star').
        removeClass('starred');
      for (i = 1; i <= rating; i++){
        objectActions.find('.star-ratings-user span.star[data-star=' + i + 
          ']').addClass('starred');
      }
    };
    updateUserRating(object.data('rating-user'));

    // rate
    var submitRating = function(e){
      e.preventDefault();
      if (!settings.auth){
        if (confirm("You must log in to do that!")){
          var current = window.location;
          window.location.href = "/Pindar/default/user/login?_next=" + current;
        }
      } else {
        var rating = 5 - $(this).index();
        objectActions.find('.star-ratings-user').off('.rating').
          css('cursor', 'default');
        $.getJSON('/Pindar/api/rate?Rating=' + rating + 
          '&QuoteID=' + object.data('id'), function(response) {
          updateUserRating(rating);
          if (response.update){
            var newRating = (object.data('rating-count') * 
              object.data('rating') - response.update + rating) / 
              object.data('rating-count');
            object.data('rating', newRating);
            object.data('rating-user', rating);
          } else {
            object.data('rating-user', rating);
            var newRating = (object.data('rating-count') * 
              object.data('rating') + rating) / (object.data('rating-count')+1);
            var newRatingCount = object.data('rating-count')+1;
            object.data('rating-count', newRatingCount);
            object.data('rating', newRating);
          }
          updateSumRating(object.data('rating'), object.data('rating-count'));
          objectActions.find('.star-ratings-user').on('click.rating', 
            'span.star', submitRating).css('cursor', 'pointer');
        }).error(function(e){
          console.log(e.responseText);
        });
      }
    };

    objectActions.find('.star-ratings-user').on('click.rating', 'span.star',
      submitRating);

    
    /********************
          EXTRA FUNCTIONALITY
    ********************/

    // wikipedia link
    objectResults.on('click', '.wiki-link', function(){
      if ($(this).closest('.input-group').find('input').val().length > 0){
        link = $(this).closest('.input-group').find('input').val();
      } else {
        var query = '';
        if (settings.objectType == 'author'){
          query = $('#AUTHOR_TR-DisplayName').val();
        } else if (settings.objectType == 'work'){
          query = $('#WORK_TR-WorkName').val();
        }
        var link = "https://en.wikipedia.org/w/index.php?search=" + 
          query + "&title=Special%3ASearch";
      }
      link = link.replace(' ', '%20');
      window.open(link);
    });

    
    // permissions
    if (!settings.auth){
      object.off('.auth');
    }

  });

};

