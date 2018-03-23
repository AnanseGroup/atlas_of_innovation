var url_string = window.location.href
var url = new URL(url_string);
var country = url.searchParams.get("country");

var type_filter = "country";
var name_filter = country;
var name_f = name_filter.split('+').join(' ');
$.get('/api/space/filter/?country='+country, function(spaces) {
	if(spaces!="")
	{
		console.log(spaces)
	 $('#wiki-list-content').prepend(
 $('<span>').attr('class', 'tab').append("All the spaces of "+type_filter+" "+name_f+" are:" ));
   for (i=0; i<spaces.length; ++i) {	
		var spaceitem = spaces[i];
		$('#wiki-list-content ul').append(
    $('<li>').append(
        $('<a>').attr('href',"/wikipage/"+spaceitem['primary_id']).append(
            $('<span>').attr('class', 'tab').append(spaceitem["name"])
))); 
		}
   	}
	  else {
	 $('#wiki-list-content ul').append(
    $('<li>').append(
            $('<span>').attr('class', 'tab').append("There are no spaces with these details")
));
}
});


