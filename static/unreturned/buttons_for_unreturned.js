//In charge of showing the return item form
function show_hide_pop_up(){
    var popup_form = document.getElementById("popup_form");

    if (popup_form.style.display == "none"){
        popup_form.style.display = "block";
    }
    else {
        popup_form.style.display = "none";
    }
}

//In charge of the submission prompt 
document.getElementById('return_form').addEventListener('submit', function(event) {
    event.preventDefault(); 

    var form = event.target;
    var formData = new FormData(form);
    var actionUrl = form.action;

    fetch(actionUrl, {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': formData.get('csrfmiddlewaretoken')
        }
    })
    .then(response => {
        if (response.ok) {
            return response.json();
        } else {
            throw new Error('Network response was not ok');
        }
    })
    .then(data => {
        if (data.success) {
            showPopup('Form submitted successfully!');
        } else {
            showPopup('Error: ' + data.error);
        }
    })
    .catch(error => {
        showPopup('Error: ' + error.message);
    });
});

function showPopup(message) {
    var popup = document.getElementById('statusPopup');
    var statusMessage = document.getElementById('statusMessage');
    statusMessage.textContent = message;
    popup.style.display = 'block';
}

function closePopup() {
    var popup = document.getElementById('statusPopup');
    popup.style.display = 'none';
    location.reload()
}