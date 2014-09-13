


function parseQuotes(quotesObject){
  /* returns a 2xN grid of quote tiles */
  var quotes = '';
  for (c in quotesObject){
    object = '';
    q = quotesObject[c];
    if (parseInt(c) % 2 === 0 | parseInt(c) === 0){
      object += '<div class="row">';
    }
    object += '<div class="col-md-6">';
    object += '<div class="object" data-id="' + q.QUOTE.id + '">';
    object += '<div class="object-data panel panel-default">';
    object += '<div class="panel-body"><p class="text">';
    if (q.QUOTE.Text.length > 250){
      object += q.QUOTE.Text.slice(0, q.QUOTE.Text.indexOf(' ', 240)) + ' ...';
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
  return quotes;
}