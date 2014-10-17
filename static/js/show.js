

var advancedVisible = false;



$(document).ready(function(){
  var quotesFunction = function(){
    return 'lookup=' + $('#textQuery').val() + '&sort=' + $('#sortOrder').val(); 
  };
  var defaultFunction = function(){ return 'sort=' + $('#sortOrder').val(); };
  var advancedQuotesFunction = function(){
    return 'lookup=' + $('#textQuery').val() + 
      '&author=' + $('#advancedAuthor').val() + 
      '&work=' + $('#advancedWork').val() + 
      '&language=' + $('#advancedLanguage').val() + 
      '&minDate=' + $('#advancedMinDate').val() + 
      '&maxDate=' + $('#advancedMaxDate').val() + 
      '&minRating=' + $('#advancedMinRating').val() + 
      '&sort=' + $('#sortOrder').val(); 
  };
  $('.default-content .search-quotes').searchify({searchFunction: quotesFunction });
  $('.default-content .search-authors').searchify({type: 'authors'});
  $('.default-content .search-works').searchify({type: 'works'});
  $('.default-content .show-quotes').searchify({
    searchFunction: defaultFunction,
    isDefault: true 
  });
  $('.default-content .show-authors').searchify({
    type: 'authors', 
    searchFunction: defaultFunction,
    isDefault: true 
  });
  $('.default-content .show-works').searchify({
    type: 'works',
    searchFunction: defaultFunction,
    isDefault: true 
  });
  $('#sortOrder').on('change', function(){
    if ($('.default-content .show-quotes').is(':visible')){
      $('.default-content .show-quotes').trigger('search');
    }
  });

  // initiate advanced
  $('.advanced-content .search').searchify({
    type: 'quotes',
    searchFunction: advancedQuotesFunction,
    isAdvanced: true,
    cols: 3
  });
  $('.advanced-content .search').trigger('sleep');

  // trigger input in case there's text in the box on page load
  $('#textQuery').trigger('input');
  
  // switch between basic and advanced search
  $('.search-bar').on('click', '.show-advanced', function(){
    if ($('.advanced-searchbar').is(':visible')){
      // switch back to basic search
      $(this).html('Advanced <i class="fa fa-chevron-down"></i>');
      $('.advanced-searchbar').find('.select2-search-choice').fadeOut('fast');
      $('.advanced-searchbar').slideUp();
      $('#textQuery').attr('placeholder', 'Search everything');
      advancedVisible = false;
      $('.advanced-content').hide();
      $('.default-content').show();
      $('.advanced-content .search').trigger('sleep');
      $('.default-content .search').trigger('wake');
    } else {
      // switch to advanced search
      $(this).html('Advanced <i class="fa fa-chevron-up"></i>');
      $('.advanced-searchbar').find('.select2-search-choice').fadeIn('slow');
      $('.advanced-searchbar').slideDown();
      $('#textQuery').attr('placeholder', 'Search quotes');
      advancedVisible = true;
      $('.default-content .search').trigger('sleep');
      $('.advanced-content .search').trigger('wake');
      $('.default-content').hide();
      $('.advanced-content').show();
    }
  });

  // fill in select2 elements
  $.getJSON('/Pindar/api/author_query', function(response){
    var authorsArray = [];
    for (c in response.authors){
      authorsArray.push({id: response.authors[c].AUTHOR_TR.id, 
        text: response.authors[c].AUTHOR_TR.DisplayName});
    }
    $("#advancedAuthor").select2({
      data: authorsArray,
      multiple: true,
      placeholder: "Filter authors"
    });
  });

  $.getJSON('/Pindar/api/work_query', function(response){
    var worksArray = [];
    for (c in response.works){
      worksArray.push({id: response.works[c].WORK_TR.id, 
        text: response.works[c].WORK_TR.WorkName});
    }
    $("#advancedWork").select2({
      data: worksArray,
      multiple: true,
      placeholder: "Filter works"
    });
  });

  $.getJSON('/Pindar/api/language_query', function(response){
    var languagesArray = [];
    for (c in response.languages){
      languagesArray.push({id: response.languages[c].LANGUAGE.id, 
        text: response.languages[c].LANGUAGE.NativeName});
    }
    $("#advancedLanguage").select2({
      data: languagesArray,
      multiple: true,
      placeholder: "Filter languages"
    });
  });

});


