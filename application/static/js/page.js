$(document).ready(function() {
	// Button handlers
	$("#contribute-bar-button").click(function(e) {
		e.preventDefault();
		$("#contribute-bar-container").toggleClass('closed');
	});
});