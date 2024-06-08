$(document).ready(function() {
    $('.delete-transaction-form').on('submit', function(event) {
        event.preventDefault();
        var form = $(this);
        var transactionId = form.data('transaction-id');
        
        $.ajax({
            type: 'POST',
            url: form.attr('action'),
            data: {
                transactionId: transactionId,
                csrfmiddlewaretoken: form.find('input[name=csrfmiddlewaretoken]').val()
            },
            success: function(response) {
                if (response.success) {
                    $('#transaction-' + transactionId).remove();
                    alert(response.message);
                    location.reload();
                } else {
                    alert(response.message);
                }
            },
            error: function() {
                alert('An error occurred. Please try again.');
            }
        });
    });
});
