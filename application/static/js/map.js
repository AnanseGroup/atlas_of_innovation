
var map = L.map('map', {
	minZoom: 2,
	worldCopyJump: true
}).setView([20,0], 2);
L.tileLayer('https://api.mapbox.com/styles/v1/albiebrown/civehqtub00022ikc7sgmp1n2/tiles/256/{z}/{x}/{y}?access_token=pk.eyJ1IjoiYWxiaWVicm93biIsImEiOiJjaXZlaDh1a2MwMWl6MnlwZDJldzFvYjNxIn0.d04rCBRG42H2JkkiID2qpA', {
    attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://mapbox.com">Mapbox</a>',
    maxZoom: 18,
}).addTo(map);

var markerClusters = L.markerClusterGroup({
		spiderfyOnMaxZoom: true,
    showCoverageOnHover: false,
    zoomToBoundsOnClick: true,
    maxClusterRadius: 40
});

var allTypes = {
	"hub": "Hub",
	"workshop": "Workshop",
	"event": "Event",
	"art gallery": "Art Gallery",
	"gallery": "Art Gallery",
	"factory": "Factory",
	"retail": "Retail",
	"virtual": "Virtual",
	"ecovillage": "Ecovillage",
	"cluster": "Cluster",
	"library": "Library",
	"lab": "Lab",
	"": "Hub"
};

var myIcon = L.icon({
    iconUrl: '/static/images/pin1.png',
    iconSize: [23, 30],
    iconAnchor: [11, 29],
    popupAnchor: [0, -30]
});

var allMarkers = [];
var noLocation = [];

$.get('/api/getAllSpaces',{cache: true}, function(spaces) {
	buildMarkers(spaces);
});

function buildMarkers(allSpaces) {
	$(".loader-text").text("Building Map . . .");
	for (i=0; i<allSpaces.length; ++i) {	
		var space = allSpaces[i];
		if (space.latitude && space.longitude) {
			try {
				var marker = L.marker([space.latitude, space.longitude], {icon: myIcon});

				marker.placeData = space;
				var popup = createPopup(space);
				marker.bindPopup(popup, {minWidth: "250"});
				markerClusters.addLayer(marker);
				allMarkers.push(marker);
			} catch (e) {
				// console.log("TypeError: " + space.name);
				// console.log(e.message);
			}
		} else {
			noLocation.push(space);
		}
	}
	map.addLayer(markerClusters, {"chunkedLoading": true});
	$("#loading").fadeOut();
}

function createPopup(space) {
	
	var popupText = "<div class='popup-header'>";
	popupText += "<h3>"+space.name+"</h3>";
	popupText += "</div>";
	popupText += "<p><img src='/static/images/pin2.png' \
						  height='14' \
						  class='popup-location-text'>\
				   <span style='margin-bottom:3px;position:fixed;'>";

	if (space.city) {
		popupText += space.city+", "+space.country;
 	} else {
		popupText += space.country;
 	}
 	popupText += "</span></p>"
 	if (space.website){
		popupText += "<a class='popup-website-link' \
						target='_blank' \
						href='http://"+space.website+"'>"
						+ space.website + "</a>"; 
	} 

	if (space.short_description){
		popupText += "<p>"+space.short_description+"</p>";
	}			
	popupText += "<a href='/space/"+space.id+"'><img src='/static/images/space_page.png' class='space-page-button'></a>";

	return popupText;
 }
 
var appliedFilters = [];

function runFilter() {	
	markerClusters.clearLayers();
	for(var i = 0; i < allMarkers.length; i++) {
		if(matchesFilter(allMarkers[i])) {
			markerClusters.addLayer(allMarkers[i]);
		}
	}
	map.addLayer(markerClusters, {"chunkedLoading": true});
}

function matchesFilter(marker) {
	for(var i = 0; i < appliedFilters.length; i++) {
		if(appliedFilters[i][1] == 'all') {
			return true;
		}

		if(!marker.placeData[appliedFilters[i][0]] || marker.placeData[appliedFilters[i][0]].toLowerCase() !== appliedFilters[i][1].toLowerCase()) {
			return false;
		}
	}
	return true;
}

$(document).ready(function() {

	// Button handlers
	$("#filter-bar .filter-bar-button").click(function(e) {		
		e.preventDefault();	
		$("#filter-bar a.active").not(this).removeClass('active');
		$(this).toggleClass('active');
		var filterType = $(this).data('filter');
		$("#filters .active").not($("#"+filterType+"-filter")).removeClass('active');
		$("#"+filterType+"-filter").toggleClass('active');
	});

	$(".filter-item").click(function(e) {		
		e.preventDefault();
		appliedFilters = [];
		var filterType = $(this).data('filterGroup');
		var filter = $(this).data('filterItem');
		appliedFilters.push([filterType, filter]);
		runFilter();
	});
});
