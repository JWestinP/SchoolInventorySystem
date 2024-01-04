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


document.addEventListener('DOMContentLoaded', function () {
        var addItemForm = document.getElementById('addItemForm');
        var itemAddedModal = document.getElementById('itemAddedModal');
        var okayButton = document.getElementById('okayButton');
        var itemList = document.getElementById('itemlist');
        var cancelButton = document.getElementById('cancelButton');

        // Handle form submission
        document.getElementById('addButton').addEventListener('click', function () {
            // Perform actions to add the item and display the added item
            // For demonstration purposes, let's just show the confirmation modal
            itemAddedModal.style.display = 'block';

            // Close the add item form
            addItemForm.style.display = 'none';
        });

        // Handle click on the "Cancel" button
        document.getElementById('cancelButton').addEventListener('click', function () {
            // Perform actions to go back to the item list
            // For demonstration purposes, let's just close the modal
            addItemForm.reset();
            itemAddedModal.style.display = 'none';
        });

         cancelButton.addEventListener('click', function () {
            // Perform actions to close the form
            addItemForm.reset();
            addItemForm.style.display = 'none';
          });

        // Handle click on the "Okay" button in the confirmation modal
        okayButton.addEventListener('click', function () {
            // Perform actions, such as navigating to the item list or other actions
            itemAddedModal.style.display = 'none';
            addItemForm.style.display = 'none';  // Hide the add item form
            itemList.scrollIntoView({ behavior: 'smooth' });
        });
    })
function selectAllItems() {
        // Replace this with the actual logic for selecting all items
        var checkboxes = document.querySelectorAll('.form-items input[type="checkbox"]');
        checkboxes.forEach(function (checkbox) {
            checkbox.checked = document.getElementById('selectAllCheckbox').checked;
        });
    }
     function confirmRemoveItems() {
    var checkbox = document.getElementById('selectAllCheckbox');
    
    if (checkbox.checked) {
      var confirmDelete = confirm('Do you want to delete the selected items?');

      if (confirmDelete) {
        // Add your logic to remove items here
        alert('Items deleted!');
      } else {
        // Uncheck the checkbox if the user cancels the deletion
        checkbox.checked = false;
      }
    }
  }
  