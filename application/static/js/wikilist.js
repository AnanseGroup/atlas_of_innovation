var url_string = window.location.href;
var url = new URL(url_string);
var country = url.searchParams.get("country");
if(country){
var type_filter = "country";
var name_filter = country;
var name_f = name_filter.split('+').join(' ');
$.get('/api/space/filter/?country='+country+'&fields=id,name&not_extend', function(spaces) {
	if(spaces!="") {
		$('#wiki-list-content').prepend(
			$('<span>')
			.attr('class', 'tab')
			.append("All the spaces of "+type_filter+" "+name_f+" are:")
		);
		for (i=0; i<spaces.length; ++i) {
			var spaceitem = spaces[i];
			var li = $('<li>').append(
				$('<a>').attr('href',"/space/"+spaceitem['id']).append(
					$('<span>')
					.attr('class', 'tab')
					.append(spaceitem["name"])
				)
			)
			if(spaceitem.recently_updated) {
				li.append(
					$('<span>')
					.attr('class','badge new red')
					.append('recently updated')
				)
			}
			if(spaceitem.validated) {
				li.append(
					$('<span>')
					.attr('class','badge new')
					.append('verified')
				)
			}
			$('#wiki-list-content ul').append(li);
		}
	} else {
		$('#wiki-list-content ul').append(
			$('<li>').append(
				$('<span>')
				.attr('class', 'tab')
				.append("There are no spaces with these details")
			)
		);
	}
});
}
