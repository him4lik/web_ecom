document.addEventListener("DOMContentLoaded", function() {
    const button = document.getElementById('rzp-button1');

    if (!button) return;

    const options = {
        key: button.dataset.key,
        currency: button.dataset.currency,
        name: button.dataset.name,
        description: button.dataset.description,
        order_id: button.dataset.orderId,
        handler: function (response) {
            document.getElementById('razorpay_payment_id').value = response.razorpay_payment_id;
            document.getElementById('razorpay_order_id').value = response.razorpay_order_id;
            document.getElementById('razorpay_signature').value = response.razorpay_signature;
            document.getElementById('payment-form').submit();
        },
        modal: {
            ondismiss: function() {
                window.location.href = button.dataset.dismissUrl;
            }
        },
        prefill: {
            name: button.dataset.prefillName,
            email: button.dataset.prefillEmail,
            contact: button.dataset.prefillContact
        },
        theme: { color: "#3399cc" }
    };

    var rzp1 = new Razorpay(options);

    rzp1.on('payment.failed', function(response) {
        alert(
            "Payment failed!\n" +
            "Error Code: " + response.error.code + "\n" +
            "Description: " + response.error.description + "\n\n" +
            "Please try again later."
        );
        window.location.href = button.dataset.dismissUrl;
    });

    button.onclick = function(e) {
        rzp1.open();
        e.preventDefault();
    };

    if (button.dataset.autoOpen === "true") {
        button.click();
    }
});
