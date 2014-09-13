
$(document).ready(function(){

  // prevent enter from submitting form
  $(document).on('keypress', 'form', function (e) {
    var code = e.keyCode || e.which;
    if (code == 13) {
      e.preventDefault();
      return false;
    }
  });

  // on clicking quote, take user to quote page
  $('.default-content').on('click', '.text', function(){
    window.location.href = '/Pindar/default/quotes/' + 
      $(this).closest('.object').data('id');
  });

  var searching = false;
  var searched = '';

  // if text query changes, reset
  $('.text-search').keyup(function(){
    if ($('.text-search').val().length < 2){
      if ($('.search:first').is(':visible')){
        $('.search').hide().empty();
        $('.default').show();
      }
    } else {
      if ($('.default:first').is(':visible')){
        $('.default').hide();
        $('.search').show().addClass('searchable');
      }
      var query = $(this).val();
      var quotesDiv = $('.search-quotes');
      var authorsDiv = $('.search-authors');
      var worksDiv = $('.search-works');
      $('.search.searchable').prepend('<div class="text-center">' + 
        '<i class="fa fa-spinner fa-spin"></i></div>').
        removeClass('searchable');

      $.getJSON('/Pindar/api/text_query?lookup=' + query,
        function(response) {
        quotesDiv.empty();
        var quotes = '<p>No quotes found.</p>';
        if (response.quotes.length > 0){
          quotesDiv.html(parseQuotes(response.quotes));
        }
        quotesDiv.addClass('searchable');
      });

      $.getJSON('/Pindar/api/author_query?author_lookup=' + query,
        function(response) {
        authorsDiv.empty();
        var authors = '<p>No authors found.</p>';
        if (response.authors.length > 0){
          authors = '<div class="row"><div class="list-group">';
          for (c in response.authors){
            a = response.authors[c];
            object = '<a class="list-group-item" ' + 
              'href="/Pindar/default/authors/' + a.AUTHOR_TR.id + '">';
            object += a.AUTHOR_TR.DisplayName;
            if (a.AUTHOR.YearBorn != null){
              if (a.AUTHOR.YearDied != null){
                object += ' (' + a.AUTHOR.YearBorn + ' - ' + 
                  a.AUTHOR.YearDied + ')';
              } else {
                object += ' (b. ' + a.AUTHOR.YearBorn + ')';
              }
            }
            workcount = a['_extra']['COUNT(WORK_AUTHOR.WorkID)'];
            if (workcount > 0){
              object += '<span class="badge">';
              object += workcount;
              if (workcount == 1){
                object += ' work</span>';
              } else {
                object += ' works</span>';
              }
            }
            object += '</a>'
            authors += object;
          }
          object += '</div></div>';
        }
        authorsDiv.append(authors);
        authorsDiv.addClass('searchable');
      });

      $.getJSON('/Pindar/api/work_query?work_lookup=' + query, 
        function(response) {
        worksDiv.empty();
        var works = '<p>No works found.</p>';
        if (response.works.length > 0){
          works = '<div class="row"><div class="list-group">';
          for (c in response.works){
            w = response.works[c];
            object = '<a class="list-group-item" ' + 
              'href="/Pindar/default/works/' + w.WORK_TR.id + '">';
            object += w.WORK_TR.WorkName;
            if (w.WORK.YearPublished != null){
              object += ' (' + w.WORK.YearPublished + ')';
            } else if (w.WORK.YearWritten != null){
              object += ' (' + w.WORK.YearWritten + ')';
            }
            quotecount = w['_extra']['COUNT(QUOTE_WORK.QuoteID)'];
            if (quotecount > 0){
              object += '<span class="badge">';
              object += quotecount;
              if (quotecount == 1){
                object += ' quote</span>';
              } else {
                object += ' quotes</span>';
              }
            }
            object += '<p class="small">' + w.AUTHOR_TR.DisplayName + '</p>';
            object += '</a>'
            works += object;
          }
          object += '</div></div>';
        }
        worksDiv.append(works);
        worksDiv.addClass('searchable');
      });
    }
  });
  
});
