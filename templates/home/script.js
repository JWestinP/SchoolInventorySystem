// script.js
function showForm(formId) {
  const forms = document.querySelectorAll('.form');
  
  forms.forEach(form => {
    form.style.display = 'none';
  });

  const selectedForm = document.getElementById(formId);
  if (selectedForm) {
    selectedForm.style.display = 'block';
  }
}
function openCategoryModal() {
  document.getElementById('categoryModal').style.display = 'flex';
}

function closeCategoryModal() {
  document.getElementById('categoryModal').style.display = 'none';
}

let modalType;

  function openModal(type) {
    modalType = type;
    document.getElementById('modal').style.display = 'flex';
  }

  function closeModal() {
    document.getElementById('modal').style.display = 'none';
  }

  function addItem() {
    const name = document.getElementById('nameInput').value;
    const image = document.getElementById('myFile').value;

    if (name && image) {
      alert(`Added ${modalType}: ${name}`);
      closeModal();
      // Perform additional actions, such as updating the UI or sending data to a server
    } else {
      alert('Please enter both name and image URL.');
    }
  }

  function showForm(formId) {
    // Hide all forms
    var forms = document.querySelectorAll('.form');
    forms.forEach(function(form) {
      form.style.display = 'none';
    });

    // Show the selected form
    var selectedForm = document.getElementById(formId);
    if (selectedForm) {
      selectedForm.style.display = 'block';
    }
  }
  function cancel ()
{
        let text = "Press a button OK to cancel.";

        if (confirm(text) == true) {
          closeModal();
        } else { false;
        }
        
}
 function toggleForm(formId) {
      var form = document.getElementById(formId);
      form.style.display = form.style.display === 'none' ? 'flex' : 'none';
    }

document.getElementById('addItemForm').addEventListener('submit', function (event) {
    event.preventDefault(); // Prevent the form from submitting and reloading the page

    // Add your logic to check if the item is already added (for demonstration purposes, I'm using a variable 'itemAlreadyAdded')
    var itemAlreadyAdded = true; // Replace this with your actual logic

    if (itemAlreadyAdded) {
        showNotification();
    } else {
        // Continue with the form submission or item addition logic
        console.log('Add the item here...');
    }
});
document.getElementById('addItemForm').addEventListener('submit', function (event) {
    event.preventDefault(); // Prevent the form from submitting and reloading the page

    // Add your logic to check if the item is already added (for demonstration purposes, I'm using a variable 'itemAlreadyAdded')
    var itemAlreadyAdded = true; // Replace this with your actual logic

    if (itemAlreadyAdded) {
        showNotificationModal();
    } else {
        // Continue with the form submission or item addition logic
        console.log('Add the item here...');
    }
});

function showNotificationModal() {
    var modal = document.getElementById('notificationModal');
    modal.style.display = 'flex';
}

function hideNotificationModal() {
    var modal = document.getElementById('notificationModal');
    modal.style.display = 'none';
}
// Add this JavaScript to handle file input and update the preview image
document.getElementById('insertPhoto').addEventListener('change', function (event) {
  var previewImage = document.getElementById('previewImage');
  var fileInput = event.target;
  
  if (fileInput.files && fileInput.files[0]) {
      var reader = new FileReader();

      reader.onload = function (e) {
          previewImage.src = e.target.result;
          previewImage.style.display = 'block'; // Show the image
      };

      reader.readAsDataURL(fileInput.files[0]);
  }
});