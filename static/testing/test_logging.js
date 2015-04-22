ac.registerActivityLogger( 
	"http://10.1.93.208", 
	"STOUT", 
	"v0.1"
	);

$('#test-button').click(function() {
  ac.logUserActivity('Test button', // description
  'test_button', // activity code
  ac.WF_OTHER
  );
})