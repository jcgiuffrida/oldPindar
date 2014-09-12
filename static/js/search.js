
$(document).ready(function(){

  // prevent enter from submitting form
  $(document).on('keypress', 'form', function (e) {
    var code = e.keyCode || e.which;
    if (code == 13) {
      e.preventDefault();
      return false;
    }
  });

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

      $.ajax({
        url: '/Pindar/api/text_query?lookup=' + query,
        type: 'GET',
        contentType: 'application/json',
        dataType: 'json',
        success: function(response) {
          quotesDiv.empty();
          var quotes = '<p>No quotes found</p>';
          if (response.quotes.length > 0){
            quotes = '';
            for (c in response.quotes){
              object = '';
              q = response.quotes[c];
              if (parseInt(c) % 2 === 0 | parseInt(c) === 0){
                object += '<div class="row">';
              }
              object += '<div class="col-md-6">';
              object += '<div class="object" data-id="' + q.QUOTE.id + '">';
              object += '<div class="object-data panel panel-default">';
              object += '<div class="panel-body"><p class="text">';
              if (q.QUOTE.Text.length > 250){
                object += q.QUOTE.Text.slice(0, q.QUOTE.Text.indexOf(' ', 240));
              } else {
                object += q.QUOTE.Text;
              }
              object += '</p><p><a class="btn btn-primary btn-sm" ';
              object += 'href="/Pindar/default/authors/' + q.AUTHOR_TR.id + '">';
              object += q.AUTHOR_TR.DisplayName + '</a> ';
              object += '<a class="btn btn-primary btn-sm" ';
              object += 'href="/Pindar/default/works/' + q.WORK_TR.id + '">';
              object += q.WORK_TR.WorkName + '</a>';
              object += '</p></div></div></div></div>';
              if ((parseInt(c) + 1) % 2 === 0){
                object += '</div>';
              }
              quotes += object;
            }
            quotesDiv.append(quotes);
          }
          quotesDiv.addClass('searchable');
        },
        error: function(request, errorType, errorMessage) {
          
        },
        timeout: 3000,
        beforeSend: function(){
        },
      });

      $.ajax({
        url: '/Pindar/api/author_query?author_lookup=' + query,
        type: 'GET',
        contentType: 'application/json',
        dataType: 'json',
        success: function(response) {
          authorsDiv.empty();
          if (response.authors.length > 0){
            var authors = '<p>' + response.authors.length + 
              ' authors found</p>';
            authorsDiv.append(authors);
          }
          authorsDiv.addClass('searchable');
        },
        error: function(request, errorType, errorMessage) {
          
        },
        timeout: 3000,
        beforeSend: function(){
        },
      });

      $.getJSON('/Pindar/api/work_query?work_lookup=' + query, 
        function(response) {
        worksDiv.empty();
        if (response.works.length > 0){
          var works = '<p>' + response.works.length + 
            ' works found</p>';
          worksDiv.append(works);
        }
        worksDiv.addClass('searchable');
      });
    }
  });
  
});
