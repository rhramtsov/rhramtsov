
  document.addEventListener("DOMContentLoaded", function() {
    const buyNowButtons = document.querySelectorAll('.buy-now-btn');
    buyNowButtons.forEach(button => {
        button.addEventListener('click', function() {
            console.log('Button clicked'); // Log when the button is clicked
            const artId = this.getAttribute('data-art-id');
            const purchaseUrl = `/api/buy-art/${artId}`; // Replace with the actual API endpoint URL
            console.log(`Sending request to ${purchaseUrl}`); // Log the URL of the request
            fetch(purchaseUrl, {
                method: 'POST',
            })
            .then(response => response.json())
            .then(data => {
                console.log(data); // Log the response data
                if (data.success) {
                    alert('Purchase successful!');
                } else {
                    alert('Error occurred while purchasing the art piece.');
                }
            })
            .catch(error => {
                console.error(error); // Log any errors
                alert('Error occurred while purchasing the art piece.');
            });
        });
    });
});
