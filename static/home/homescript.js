var cleaning = document.getElementById('cleaning')
var gadget = document.getElementById('gadget')
var furniture = document.getElementById('furniture')
var room = document.getElementById('room')
var dean = document.getElementById('dean')
const buttons = document.getElementsByClassName('category_button')
const selectItem = document.querySelectorAll('.item_button')

function hideShowCleaning()
{
    cleaning.style.display = 'block'
    for(var i = 0; i < buttons.length; i++)
    {
        buttons[i].style.display = 'none'
    }
}

function hideShowGadget()
{
    gadget.style.display = 'block'
    for(var i = 0; i < buttons.length; i++)
    {
        buttons[i].style.display = 'none'
    }
}

function hideShowFurniture()
{
    furniture.style.display = 'block'
    for(var i = 0; i < buttons.length; i++)
    {
        buttons[i].style.display = 'none'
    }
}

function hideShowRoom()
{
    room.style.display = 'block'
    for(var i = 0; i < buttons.length; i++)
    {
        buttons[i].style.display = 'none'
    }
}

function hideShowDean()
{
    dean.style.display = 'block'
    for(var i = 0; i < buttons.length; i++)
    {
        buttons[i].style.display = 'none'
    }
}

function backCategories()
{
    cleaning.style.display = 'none'
    gadget.style.display = 'none'
    furniture.style.display = 'none'
    room.style.display = 'none'
    dean.style.display = 'none'
    for(var i = 0; i < buttons.length; i++)
    {
        buttons[i].style.display = 'inline'
    }    
}

function fetchData(itemId, itemType) {
    let apiUrl;
    if (itemType === 'cleaning') {
        apiUrl = '/api/cleaning_inventory/';
        headerId = 'cleaning_header'
        bodyId = 'cleaning_body'
        informationId = document.getElementById('cleaning_information')
    } 
    else if (itemType === 'room') {
        apiUrl = '/api/room_inventory/';
        headerId = 'room_header'
        bodyId = 'room_body'
        informationId = document.getElementById('room_information')
    } 
    else if (itemType === 'furniture') {
        apiUrl = '/api/furniture_inventory/';
        headerId = 'furniture_header'
        bodyId = 'furniture_body'
        informationId = document.getElementById('furniture_information')
    } 
    else if (itemType === 'gadget') {
        apiUrl = '/api/technology_inventory/';
        headerId = 'gadget_header'
        bodyId = 'gadget_body'
        informationId = document.getElementById('gadget_information')
    } 
    else if (itemType === 'dean') {
        apiUrl = '/api/dean_inventory/';
        headerId = 'dean_header'
        bodyId = 'dean_body'
        informationId = document.getElementById('dean_information')
    } 
    else {
        console.error('Invalid item type:', itemType);
        return;
    }

    fetch(apiUrl)
        .then(response => response.json())
        .then(data => {
            const selectedItem = data.find(item => item.item_id === parseInt(itemId));
            const imageUrl = `/media/${selectedItem.item_photo}`
            document.getElementById(headerId).innerHTML = `
                <img src="${imageUrl}" alt="${selectedItem.item_name}" style="width: 100px; height: 100px;">
                <p>Item ID: ${selectedItem.item_id}</p>
                <p>Name: ${selectedItem.item_name}</p>
                <p>Category: ${selectedItem.item_category}</p>
                <button data-close-button class="close_button">&times;</button> 
            `;
            document.body.addEventListener('click', function (event) {
                if (event.target.matches('.close_button')) {
                    console.log('Close Button Clicked');
                    closeItem(informationId);
                }
            });

            document.getElementById(bodyId).innerHTML = `
                <p>Description: ${selectedItem.item_description}</p>
                <p>Total Quantity: ${selectedItem.item_total_quantity}</p>
                <p>Borrowed Quantity: ${selectedItem.item_borrowed_quantity}</p>
                <p>Available Quantity: ${selectedItem.item_current_quantity}</p>
            `;

            const csrfToken = document.cookie.split(';').find(cookie => cookie.trim().startsWith('csrftoken=')).split('=')[1];

            fetch('/get_borrow_form/')
            .then(response => response.json())
            .then(data => {
                
                const formContainer = document.getElementById('item_form');
                formContainer.innerHTML = data.form_html;

                const borrowForm = document.getElementById('borrowFormId');
                console.log('borrowForm:', borrowForm);
                if (borrowForm) {
                    borrowForm.querySelector('[name = "item_id"]').value = selectedItem.item_id
                    borrowForm.querySelector('[name = "item_name"]').value = selectedItem.item_name
                    
                    borrowForm.addEventListener('submit', function (event) {
                        event.preventDefault();
                    
                        const formData = new FormData(borrowForm);

                        formData.append('csrfmiddlewaretoken', csrfToken);
                        formData.append('copy_image', 'true');
                        formData.append('source_item_id', selectedItem.item_id);
                        
                        const fileInput = borrowForm.querySelector('[name = "item_photo"]');
                        if (fileInput && fileInput.files && fileInput.files.length > 0) {
                            formData.append('item_photo', fileInput.files[0]);
                        }

                        console.log(formData.get('item_photo'));
                        console.log('FormData:', formData);
                        fetch('/save_borrow_form/Cleaning_Material/', {
                            method: 'POST',
                            body: formData
                        })
                        .then(response => response.json())
                        .then(data => {
                            console.log(data);
                            if (data.message) {
                                // Success: Do something, e.g., redirect or show success message
                            } else if (data.error) {
                                // Error: Show error message to the user
                                console.error(data.error);
                            }
                        })
                        .catch(error => console.error('Error submitting form:', error));
                    });                   
                }
            })
            .catch(error => console.error('Error fetching form HTML:', error));

            openItem(informationId);
        })
        .catch(error => console.error('Error fetching data:', error));
}

function openItem(informationId) {
    console.log('Opening Item');
    if (informationId) {
        informationId.classList.add('active');
    }
}

function closeItem(informationId) {
    console.log('Closing Item');
    informationId.classList.remove('active');
}

selectItem.forEach(button => {
    button.addEventListener('click', () => {
        const itemId = button.getAttribute('data-item-target');
        const itemType = button.getAttribute('data-item-type');
        console.log('Button Clicked for Item ID:', itemId);
        console.log('Item Type:', itemType);
        
        fetchData(itemId, itemType);
    });
});
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
    function previewImage() {
          var fileInput = document.getElementById('myFile');
          var previewImage = document.getElementById('previewImage');
  
          if (fileInput.files && fileInput.files[0]) {
              var reader = new FileReader();
  
              reader.onload = function (e) {
                  previewImage.src = e.target.result;
              };
  
              reader.readAsDataURL(fileInput.files[0]);
          }
      }
  
      function closeModal() {
           document.getElementById('modal').style.display = 'none';
      }
  
      function cancel() {
          let text = "Press a button OK to cancel.";
  
          if (confirm(text) == true) {
            closeModal();
          } else { false;
          }
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
