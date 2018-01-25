
var currentLocation = window.location.pathname.toString().split("/")[2]
var services = ["Coworking","Making","Hosting Events","Selling","Trading","Incubating Startup","Educating","Vocational training","Investing","Mentoring","Donating","Transferring technology","Coliving","Repairing","Manufacturing","Prototyping","Researching"]
var ownership = ["Civil Society","Private Sector","Hybrid Led","Government","Academic","University"]
$.get('/api/getSpace/'+currentLocation, function(space) {
	document.getElementById('text-name').value = space["name"];
	$("#primary-type").val(space["primary_type"]).trigger('chosen:updated');
	document.getElementById('textarea-address').value = space["street_address"];
	document.getElementById('text-city').value = space["city"];
	document.getElementById('text-country').value = space["country"];
	document.getElementById('text-email').value = space["email"];
	document.getElementById('textarea-description').value = space["description"];
	document.getElementById('number-phone').value = space["phone"];
	document.getElementById('textarea-tools').value = space["tools"];
	$("#members").val(space["number_of_members"]).trigger('chosen:updated');
	 $("#theme").val(space["theme"]).trigger('chosen:updated');
	$("#affiliation").val(space["network_affiliation"]).trigger('chosen:updated');
	$("#select-status").val(space["status"]).trigger('chosen:updated');
	if(space["services"]!=null)
	{
	service_list = space["services"].split(",") ;
   for (var i = 0; i < service_list.length; i++) {
	index =  services.indexOf(service_list[i]);
	if(index!=-1)
	document.getElementById("checkbox-services-"+index).checked = true;   	
   	}
   	}
	
	if(space["ownership"]!=null)
        {
        ownership_list = space["ownership"].split(",") ;
   for (var i = 0; i < ownership_list.length; i++) {
        index =  ownership.indexOf(ownership_list[i]);
        if(index!=-1)
	document.getElementById("checkbox-ownership-"+index).checked = true;
        }
        }
});
