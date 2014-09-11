
jQuery(document).ready(function(){
  // hide author and work fields
  jQuery('#QUOTE_QuoteLanguageID__row').hide();
  jQuery('#QUOTE_QuoteLanguageID').appendTo(jQuery('#QUOTE_Text__row .w2p_fc'));
  jQuery('#QUOTE_IsOriginalLanguage__row').hide();
  jQuery('#QUOTE_FirstName__row').hide();
  jQuery('#QUOTE_MiddleName__row').hide();
  jQuery('#QUOTE_LastName__row').hide();
  jQuery('#QUOTE_AKA__row').hide();
  jQuery('#QUOTE_DisplayName__row').hide();
  jQuery('#QUOTE_Biography__row').hide();
  jQuery('#QUOTE_AuthorWikipediaLink__row').hide();
  jQuery('#QUOTE_YearBorn__row').hide();
  jQuery('#QUOTE_YearDied__row').hide();
  jQuery('#QUOTE_Author_Submit__row').hide();
  jQuery('#QUOTE_WorkName__row').hide();
  jQuery('#QUOTE_WorkSubtitle__row').hide();
  jQuery('#QUOTE_WorkDescription__row').hide();
  jQuery('#QUOTE_WorkWikipediaLink__row').hide();
  jQuery('#QUOTE_WorkNote__row').hide();
  jQuery('#QUOTE_YearPublished__row').hide();
  jQuery('#QUOTE_YearWritten__row').hide();
  jQuery('#QUOTE_Work_Submit__row').hide();
  jQuery('#QUOTE_Note__row').hide();
  jQuery('#QUOTE_AuthorTrID__row').hide();
  jQuery('#QUOTE_WorkTrID__row').hide();
  jQuery('#QUOTE_Work_Lookup__row').hide();
  jQuery('#submit_record__row').hide();
  jQuery('#QUOTE_Quote_Submit__row').hide();
  jQuery('#author_results').hide();
  jQuery('#work_results').hide();
  
  jQuery('#QUOTE_Text').attr('placeholder', 'Enter the quote...');
  jQuery('#QUOTE_Note').attr('placeholder', 'Context or additional information');

  // disable the following till they can accept urls without http://
  // jQuery('#QUOTE_AuthorWikipediaLink').attr('type', 'url'); 
  // jQuery('#QUOTE_WorkWikipediaLink').attr('type', 'url');
  
  jQuery('#QUOTE_Text__row').hide().fadeIn('slow');
  jQuery('#QUOTE_QuoteLanguageID').hide();
  jQuery('#QUOTE_Author_Lookup__row').hide();
  
  var started = false;
  jQuery('#QUOTE_Text').keyup(function(){
    if (started | jQuery('#QUOTE_Text').val().length > 2){
      started = true;
      jQuery('#QUOTE_Author_Lookup__row').fadeIn('slow');
      jQuery('#QUOTE_QuoteLanguageID').fadeIn('slow');
    }
  });
    
  $.validator.addMethod(
        "regex",
        function(value, element, regexp) {
            var re = new RegExp(regexp);
            return this.optional(element) || re.test(value);
        },
        "Please check your input."
  );

  $(document).on('keypress', 'form', function (e) {
    var code = e.keyCode || e.which;
    if (code == 13) {
      e.preventDefault();
      return false;
    }
  });
  
  jQuery('#QUOTE_Author_Lookup').keyup(function(){
    jQuery('#work_results').html('');
    jQuery('#QUOTE_Work_Lookup__row').fadeOut('fast');
    jQuery('#QUOTE_Work_Lookup').val('');
    jQuery('#QUOTE_Note__row').fadeOut('fast');
    jQuery('#QUOTE_WorkTrID').val('');
    jQuery('#QUOTE_Quote_Submit__row').fadeOut('fast');
    jQuery('#QUOTE_AuthorTrID').val('');
    if (jQuery('#QUOTE_Author_Lookup').val().length < 2){
      if (jQuery('#author_results').is(':visible')){
        jQuery('#author_results').fadeOut('fast').delay(200);
        jQuery('#author_results').html('');
      }
    } else {
      jQuery('#author_results').fadeIn('slow');
      ajax('{{=URL('api', 'author_query')}}', 
          ['author_lookup'], 'author_results');
    }
  });
  
  jQuery('#QUOTE_Work_Lookup').keyup(function(){
    jQuery('#QUOTE_Note__row').fadeOut('fast');
    jQuery('#QUOTE_Quote_Submit__row').fadeOut('fast');
    if (jQuery('#QUOTE_Work_Lookup').val().length < 2){
      if (jQuery('#work_results').is(':visible')){
        jQuery('#work_results').fadeOut('fast').delay(200);
        jQuery('#work_results').html('');
        jQuery('#QUOTE_WorkTrID').val('');
      }
    } else {
      jQuery('#work_results').fadeIn('slow');
      ajax('{{=URL('api', 'work_query')}}', 
          ['work_lookup', 'AuthorTrID'], 'work_results');
    }
  });
  
  
  $(':submit').on('click', function(){
    button = $(this).attr('id');
    if (button != 'QUOTE_Quote_Submit'){
      $('#QUOTE_Text').rules('remove');
    } else {
      $('#QUOTE_Text').rules('add', {
        required: true
      });
    }
  });
  
  $('form').validate({
    rules: {
      FirstName: {
        maxlength: 128
      },
      MiddleName: {
        maxlength: 128
      },
      LastName: {
        maxlength: 128
      },
      DisplayName: {
        required: true,
        maxlength: 512
      },
      Biography: {
        maxlength: 8192
      },
      AuthorWikipediaLink: {
        regex: '^(https://|http://)?[a-z]{2}\.wikipedia\.org/wiki/.{1,}'
      },
      YearBorn: {
        range: [-5000,2050]
      },
      YearDied: {
        range: [-5000, 2050]
      },
      WorkName: {
        required: true,
        maxlength: 1024
      },
      WorkSubtitle: {
        maxlength: 1024
      },
      WorkDescription: {
        maxlength: 4096
      },
      WorkWikipediaLink: {
        regex: '^(https://|http://)?[a-z]{2}\.wikipedia\.org/wiki/.{1,}'
      },
      WorkNote: {
        maxlength: 4096
      },
      YearPublished: {
        range: [-5000, 2050]
      },
      YearWritten: {
        range: [-5000, 2050]
      },
      Text: {
        required: true,
        minlength: 3
      },
      QuoteLanguageID: {
        required: true
      },
      Note: {
        maxlength: 4096
      }
    },
    messages: {
      DisplayName: {
        required: "Please enter a name"
      },
      YearBorn: "Please enter a valid year",
      YearDied: "Please enter a valid year",
      WorkName: {
        required: "Please enter the work name"
      },
      YearPublished: "Please enter a valid year",
      YearWritten: "Please enter a valid year",
      Text: {
        required: "Please enter the quote",
        minlength: "Your quote should be more than two characters"
      },
      QuoteLanguageID: "What language is the quote in?"
    },
    submitHandler: function(form) {
      if (button == 'QUOTE_Author_Submit'){
        ajax('{{=URL('api', 'author_submit')}}',
          ['FirstName', 'MiddleName', 'LastName', 'AKA', 'DisplayName',
           'Biography', 'AuthorWikipediaLink', 'YearBorn', 'YearDied', 
           'LanguageID'],
           ':eval');
        jQuery('#QUOTE_FirstName__row').fadeOut('fast');
        jQuery('#QUOTE_MiddleName__row').fadeOut('fast');
        jQuery('#QUOTE_LastName__row').fadeOut('fast');
        jQuery('#QUOTE_AKA__row').fadeOut('fast');
        jQuery('#QUOTE_DisplayName__row').fadeOut('fast');
        jQuery('#QUOTE_Biography__row').fadeOut('fast');
        jQuery('#QUOTE_AuthorWikipediaLink__row').fadeOut('fast')
        jQuery('#QUOTE_YearBorn__row').fadeOut('fast');
        jQuery('#QUOTE_YearDied__row').fadeOut('fast');
        jQuery('#QUOTE_Author_Submit__row').fadeOut('fast');
        $('#QUOTE_Author_Lookup__row').fadeIn('fast');
        $('#QUOTE_Author_Lookup').val($('#QUOTE_DisplayName').val());
        $('#QUOTE_Work_Lookup__row').fadeIn('fast');
        $('#QUOTE_Work_Lookup').focus();
        clear_author();
      } else if (button == 'QUOTE_Work_Submit'){
        ajax('{{=URL('api', 'work_submit')}}',
          ['WorkName', 'WorkSubtitle', 'WorkDescription', 'WorkWikipediaLink',
           'WorkNote', 'YearPublished', 'YearWritten',  
           'LanguageID', 'AuthorTrID'],
           ':eval');
        jQuery('#QUOTE_WorkName__row').fadeOut('fast');
        jQuery('#QUOTE_WorkSubtitle__row').fadeOut('fast');
        jQuery('#QUOTE_WorkDescription__row').fadeOut('fast');
        jQuery('#QUOTE_WorkWikipediaLink__row').fadeOut('fast');
        jQuery('#QUOTE_WorkNote__row').fadeOut('fast');
        jQuery('#QUOTE_YearPublished__row').fadeOut('fast');
        jQuery('#QUOTE_YearWritten__row').fadeOut('fast');
        jQuery('#QUOTE_Work_Submit__row').fadeOut('fast');
        $('#QUOTE_Work_Lookup__row').fadeIn('fast');
        $('#QUOTE_Work_Lookup').val($('#QUOTE_WorkName').val());
        $('#QUOTE_Note__row').fadeIn('fast');
        $('#QUOTE_Note').focus();
        $('#QUOTE_Quote_Submit__row').fadeIn('fast');
        clear_work();
      } else if (button == 'QUOTE_Quote_Submit'){
        ajax('{{=URL('api', 'quote_submit')}}',
          ['Text', 'QuoteLanguageID', 'IsOriginalLanguage',
           'Note', 'AuthorTrID', 'WorkTrID'],
           ':eval');
        clear_quote();
        clear_author();
        clear_work();
      }
    }
  });
  
  
  jQuery('#authorWikiLink').on('mouseover', function(){
    query = $('#QUOTE_DisplayName').val();
    link = "https://en.wikipedia.org/w/index.php?search=" + query + "&title=Special%3ASearch";
    link = link.replace(' ', '%20');
    $('#authorWikiLink').attr('href', link);
  });
  
  jQuery('#workWikiLink').on('mouseover', function(){
    query = $('#QUOTE_WorkName').val();
    link = "https://en.wikipedia.org/w/index.php?search=" + query + "&title=Special%3ASearch";
    link = link.replace(' ', '%20');
    $('#workWikiLink').attr('href', link);
  });
  
  $('#QUOTE_Author_Cancel').on('click', function(){
    jQuery('#QUOTE_FirstName__row').fadeOut('fast');
    jQuery('#QUOTE_MiddleName__row').fadeOut('fast');
    jQuery('#QUOTE_LastName__row').fadeOut('fast');
    jQuery('#QUOTE_AKA__row').fadeOut('fast');
    jQuery('#QUOTE_DisplayName__row').fadeOut('fast');
    jQuery('#QUOTE_Biography__row').fadeOut('fast');
    jQuery('#QUOTE_AuthorWikipediaLink__row').fadeOut('fast')
    jQuery('#QUOTE_YearBorn__row').fadeOut('fast');
    jQuery('#QUOTE_YearDied__row').fadeOut('fast');
    jQuery('#QUOTE_Author_Submit__row').fadeOut('fast');
    $('#QUOTE_Author_Lookup__row').fadeIn('fast');
    $('#QUOTE_Author_Lookup').val('');
    $('#QUOTE_Author_Lookup').focus();
    clear_author();
  });
  
  $('#QUOTE_Work_Cancel').on('click', function(){
    jQuery('#QUOTE_WorkName__row').fadeOut('fast');
    jQuery('#QUOTE_WorkSubtitle__row').fadeOut('fast');
    jQuery('#QUOTE_WorkDescription__row').fadeOut('fast');
    jQuery('#QUOTE_WorkWikipediaLink__row').fadeOut('fast');
    jQuery('#QUOTE_WorkNote__row').fadeOut('fast');
    jQuery('#QUOTE_YearPublished__row').fadeOut('fast');
    jQuery('#QUOTE_YearWritten__row').fadeOut('fast');
    jQuery('#QUOTE_Work_Submit__row').fadeOut('fast');
    $('#QUOTE_Work_Lookup__row').fadeIn('fast');
    $('#QUOTE_Work_Lookup').val('');
    $('#QUOTE_Work_Lookup').focus();
    clear_work();
  });

});
(function ($) {
  $.selectAuthor = function(tablename){
    var selected;
    $(document).on("click", tablename + " tr", function(e) {
      e.preventDefault();
      selected = $(this);
      selected.css("background-color", "#999");
      if (this.id == 0){
        $('#author_results').fadeOut('fast').delay(500).html('');
        $('#author_results').fadeIn('fast');
        jQuery('#QUOTE_Author_Lookup__row').fadeOut('fast');
        jQuery('#QUOTE_Author_Lookup').val('');
        jQuery('#QUOTE_FirstName__row').fadeIn('fast');
        jQuery('#QUOTE_MiddleName__row').fadeIn('fast');
        jQuery('#QUOTE_LastName__row').fadeIn('fast');
        jQuery('#QUOTE_AKA__row').fadeIn('fast');
        jQuery('#QUOTE_DisplayName__row').fadeIn('fast');
        jQuery('#QUOTE_DisplayName').val($(this).children('td').
          html().capitalize());
        var names = ($(this).children('td').html()).capitalize().split(" ");
        if (names.length == 1){
          jQuery('#QUOTE_FirstName').val(names[0]);
        } else if (names.length == 2){
          jQuery('#QUOTE_FirstName').val(names[0]);
          jQuery('#QUOTE_LastName').val(names[1]);
        } else if (names.length == 3){
          jQuery('#QUOTE_FirstName').val(names[0]);
          jQuery('#QUOTE_MiddleName').val(names[1]);
          jQuery('#QUOTE_LastName').val(names[2]);
        }
        jQuery('#QUOTE_Biography__row').fadeIn('fast');
        jQuery('#QUOTE_AuthorWikipediaLink__row').fadeIn('fast')
        jQuery('#QUOTE_YearBorn__row').fadeIn('fast');
        jQuery('#QUOTE_YearDied__row').fadeIn('fast');
        jQuery('#QUOTE_Author_Submit__row').fadeIn('fast');
      } else {      
        $('#QUOTE_AuthorTrID').val(this.id);
        $('#QUOTE_Author_Lookup').val($(this).children('td').html());
        $('#author_results').fadeOut('fast').delay(500).html('');
        $('#author_results').fadeIn('fast');
        $('#QUOTE_Work_Lookup__row').fadeIn('slow');
      }
      
    });
    $(tablename).on('selectstart', false); //Don't let the user select the table
  }
})(jQuery);
$.selectAuthor("#author_results");

String.prototype.capitalize = function(delim) {
  if(typeof(delim)==='undefined') delim = " ";
  var strings = this.split(delim);
  for (var i = 0; i < strings.length; i++){
    strings[i] = strings[i].charAt(0).toUpperCase() + strings[i].slice(1);
  }
    return strings.join(' ');
}

function clear_quote() {
  jQuery('#QUOTE_Text').val('');
  jQuery('#QUOTE_QuoteLanguageID').val(1);
  jQuery('#QUOTE_IsOriginalLanguage').prop('checked',false)
  jQuery('#QUOTE_Note').val('');
}

function clear_author() {
  jQuery('#QUOTE_FirstName').val('');
  jQuery('#QUOTE_MiddleName').val('');
  jQuery('#QUOTE_LastName').val('');
  jQuery('#QUOTE_AKA').val('');
  jQuery('#QUOTE_DisplayName').val('');
  jQuery('#QUOTE_Biography').val('');
  jQuery('#QUOTE_AuthorWikipediaLink').val('');
  jQuery('#QUOTE_YearBorn').val('');
  jQuery('#QUOTE_YearDied').val('');
}

function clear_work() {
  jQuery('#QUOTE_WorkName').val('');
  jQuery('#QUOTE_WorkSubtitle').val('');
  jQuery('#QUOTE_WorkDescription').val('');
  jQuery('#QUOTE_WorkWikipediaLink').val('');
  jQuery('#QUOTE_Note').val('');
  jQuery('#QUOTE_YearPublished').val('');
  jQuery('#QUOTE_YearWritten').val('');
}

(function ($) {
  $.selectWork = function(tablename){
    var selected;
    $(document).on("click", tablename + " tr", function(e) {
      e.preventDefault();
      selected = $(this);
      selected.css("background-color", "#999");
      if (this.id == 0){
        $('#work_results').fadeOut('fast').delay(500).html('');
        $('#work_results').fadeIn('fast');
        jQuery('#QUOTE_Work_Lookup__row').fadeOut('fast');
        jQuery('#QUOTE_Work_Lookup').val('');
        jQuery('#QUOTE_WorkName__row').fadeIn('fast');
        jQuery('#QUOTE_WorkName').val($(this).children('td').html().capitalize());
        jQuery('#QUOTE_WorkSubtitle__row').fadeIn('fast');
        jQuery('#QUOTE_WorkDescription__row').fadeIn('fast');
        jQuery('#QUOTE_WorkWikipediaLink__row').fadeIn('fast');
        jQuery('#QUOTE_YearPublished__row').fadeIn('fast');
        jQuery('#QUOTE_YearWritten__row').fadeIn('fast');
        jQuery('#QUOTE_Work_Submit__row').fadeIn('fast');
      } else {  
        $('#QUOTE_WorkTrID').val(this.id);
        $('#QUOTE_Work_Lookup').val($(this).children('td').html());
        $('#work_results').fadeOut('fast').delay(500).html('');
        $('#work_results').fadeIn('fast');
        $('#QUOTE_Note__row').fadeIn('slow');
        $('#QUOTE_Quote_Submit__row').fadeIn('slow');
      }
    });
    $(tablename).on('selectstart', false); //Don't let the user select the table
  }
})(jQuery);
$.selectWork("#work_results");