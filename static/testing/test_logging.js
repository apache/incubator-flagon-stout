ac.registerActivityLogger( 
	"http://52.20.48.202",
	"STOUT", 
	"v0.1"
	);

$('#test-button').click(function() {
  ac.logUserActivity('Test button', // description
  'test_button', // activity code
  ac.WF_OTHER
  );
})