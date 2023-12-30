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
      