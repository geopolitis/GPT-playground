$(function() {
    $('form').submit(function(event) {
        // Prevent the form from submitting via HTTP
        event.preventDefault();

        // Get the values of the webpage and query input fields
        var webpage = $('#webpage').val();
        var query = $('#query').val();

        // Send an AJAX request to the Flask backend with the input values
        $.ajax({
            url: '/answer',
            method: 'POST',
            data: {
                webpage: webpage,
                query: query
            },
            success: function(response) {
                // Update the result section of the page with the response
                $('#result').html('<h2>Result:</h2><p>' + response + '</p>');
            },
            error: function(xhr, status, error) {
                // Log any errors to the console
                console.error(error);
            }
        });
    });
});
