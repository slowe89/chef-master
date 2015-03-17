/**
 *
 * Author: John Turner
 * Version: 1.1
 * Last Updated: 2/28/15
 *
 * Script for the Edit user page. 
 * 
 */

$(function()
{
	// When the form is submitted, grab all of the radio buttons, and 
	// see which is checked. Whichever is checked, add the label to 
	// the hidden field and then submit it. 
	$( 'form' ).submit(function(event)
	{
		// variable for validation:
		var flag = false;
		
		// grab all the buttons
		$( 'paper-radio-button' ).each(function()
		{
			if ($( this ).prop('checked'))
			{
				// set the flag to true
				flag = true;

				// grab the value from the label and set it in the hidden field.
				$( "#group_name" ).val( $( this ).prop('label') )
			}
		});

		// if there was something checked, validate and submit the form
		if (flag) 
		{
			return
		}
		else
		{
			// stop the submission of the form, and show the error 
			event.preventDefault()

			// make the error div visible and add text
			$("#hidden_field_error1").text("Please select a group for the user!").css("display","block");
		}
	});
		
});