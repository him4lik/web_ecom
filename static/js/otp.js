
// Function to send OTP
function sendOTP() {
    let phone = document.getElementById("id_phone").value;

    if (phone.length < 10) {
        alert("Enter a valid phone number");
        return;
    }

    fetch(`http://localhost/proxy-api/send-otp/?username=${encodeURIComponent(phone)}`, {
        method: "GET",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded",
            "X-CSRFToken": getCookie("csrftoken")
        },
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            alert("OTP Sent!");
            document.getElementById("id_otp").style.display = "block";
            document.getElementById("sendOtpBtn").style.display = "none";
            document.getElementById("loginBtn").style.display = "block";
        } else {
            alert("Failed to send OTP. Try again later");
        }
    })
    .catch(error => console.error("Error:", error));
}

// Function to get CSRF token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        let cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            let cookie = cookies[i].trim();
            if (cookie.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
