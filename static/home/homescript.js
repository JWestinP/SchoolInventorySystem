var itemDisplay
const category = document.getElementsByClassName('category_button')
const selectItem = document.querySelectorAll('.item_button')
const informationId = document.getElementById('item_information')
const backCategory = document.getElementById('back_category')
const itemContainer = document.getElementById('item_list')

function fetchData(itemId) {
    fetch('/api/item_inventory/')
        .then(response => {
            if (!response.ok) {
                throw new Error(`Error ${response.status}: ${response.statusText}`);
            }
            console.log(itemId)
            return response.json();
        })
        .then(data => {
            console.log('Response data:', data)
            const items = data.items;
            items.forEach(item => {
                console.log(`Item ID: ${item.item_id}`);
            });
            const selectedItem = items.find(item => item.item_id === parseInt(itemId));
            console.log('Selected item ID:', selectedItem.item_id);

            
            if (selectedItem) {
                const imageUrl = `${selectedItem.item_photo}`
                document.getElementById('item_header').innerHTML = `
                    <div class="item-header-pic">
                    <img src="${imageUrl}" alt="${selectedItem.item_name}" style="width: 100px; height: 100px;">
                    </div>
                    <div class="item-header-info">
                    <p class="name">Name: ${selectedItem.item_name}</p>
                    <p>Category: ${selectedItem.item_category}</p>
                    <p >Item ID: ${selectedItem.item_id}</p>
                    </div>
                `;
                document.body.addEventListener('click', function (event) {
                    if (event.target.matches('.close_button')) {
                        console.log('Close Button Clicked');
                        closeItem(informationId);
                    }
                });
    
                document.getElementById('item_body').innerHTML = `
                    <button data-close-button class="close_button">&times;</button> 
                    <p>Description: ${selectedItem.item_description}</p>
                    <p>Total Quantity: ${selectedItem.item_total}</p>
                    <p>Borrowed Quantity: ${selectedItem.item_borrowed}</p>
                    <p>Available Quantity: ${selectedItem.item_current}</p>
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
                        const itemStockInput = borrowForm.querySelector('[name="item_stock"]');
                        if (selectedItem && selectedItem.item_id) {
                            console.log('Selected Item:', selectedItem);
                            console.log('Item Information:', selectedItem.item_id);

                            if (selectedItem.item_id) {
                                itemStockInput.value = selectedItem.stock_id;
                                console.log('item_stockInput value:', itemStockInput.value);

                            } 
                            else {
                                console.error('Missing item_information.item_id:', selectedItem.item_id);
                            }
                        } 
                        else {
                            console.error('Invalid selectedItem or item_information.', 'Selected Item:', selectedItem.item_id);
                        }

                        borrowForm.addEventListener('submit', function (event) {
                            event.preventDefault();
                        
                            const formData = new FormData(borrowForm);
    
                            formData.append('csrfmiddlewaretoken', csrfToken);
                            formData.append('source_item_id', selectedItem.item_id);
                            formData.append('stock_id', selectedItem.stock_id);
                            console.log(formData)
                            console.log('FormData:', formData);
                            fetch('/save_borrow_form/', {
                                method: 'POST',
                                body: formData
                            })
                            .then(response => response.json())
                            .then(data => {
                                console.log(data);
                                if (data.message) {
                                   
                                } else if (data.error) {
                                    
                                    console.error(data.error);
                                }
                            })
                            .catch(error => console.error('Error submitting form:', error));
                        });                   
                    }
                })
    
                openItem(informationId);
            }
            else {
                console.error('Item not found for the given item ID.');
                
            }

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

function showItem(category) {
    console.log('Sending request for category:', category)

    var xhr = new XMLHttpRequest()
    xhr.open('GET', '/get_items/?category=' + encodeURIComponent(category), true)
    xhr.send()

    xhr.onload = function() {
        console.log('Response received:', xhr.responseText)
    
        if (xhr.status != 200) {
            console.error('Error ' + xhr.status + ': ' + xhr.statusText)
        } 
        else {
            try {
                var data = JSON.parse(xhr.responseText)
                console.log('Received data:', data)

                document.getElementById('back-button').innerHTML = `
                <button id="back_category" onclick="showAllCategoryButtons()" class="back-button">Back</button>
                `;
                
                itemContainer.addEventListener('click', function (event) {
                    
                    if (event.target.matches('.item_button')) {
                        const itemId = event.target.getAttribute('data-item-target');
                    
                
                        console.log('Item button clicked. Item ID:', itemId);
                
                        
                        fetchData(itemId);
                    }
                });
                if (Array.isArray(data.items)) {
                    data.items.forEach(selectedItem => {
                        const imageUrl = `${selectedItem.item_photo}`
                        const itemHTML = `
                        <div class="items-grid">
                        
                            <div class="items">

                                <div class="items-pic">
                                    <img src="${imageUrl}" alt="${selectedItem.item_name}" class="item-pic">
                                </div>  

                                <div class= "items-button">
                                    <button data-item-target="${selectedItem.item_id}" class="item_button">${selectedItem.item_name}</button>

                                </div>

                            </div>

                        </div>
                        `
                        itemContainer.innerHTML += itemHTML

                    })
                } 
                else {
                    console.error('Data does not contain an array:', data)
                    
                }
            } 
            catch (error) {
                console.error('Error parsing JSON:', error)
            }
        }
    };
}

function hideAllCategoryButtons() {
    var categoryButtons = document.querySelectorAll('.category_button');
    categoryButtons.forEach(function(button) {
        button.style.display = 'none';
    });
}

function showAllCategoryButtons() {
    
    var categoryButtons = document.querySelectorAll('.category_button');
    categoryButtons.forEach(function(button) {
        button.style.display = 'inline';

    });
    var itemContainer = document.getElementById('item_list');
    itemContainer.innerHTML = '';

    location.reload()

}

selectItem.forEach(button => {
    button.addEventListener('click', () => {
        const itemId = button.getAttribute('data-item-target');
        console.log('Button Clicked for Item ID:', itemId);
        console.log('Item Type:', itemType);
        
        fetchData(itemId);
    });
});

// // code ni nicole start
// function showForm(formId) {
//     const forms = document.querySelectorAll('.form');
    
//     forms.forEach(form => {
//       form.style.display = 'none';
//     });
  
//     const selectedForm = document.getElementById(formId);
//     if (selectedForm) {
//       selectedForm.style.display = 'block';
//     }
//   }
//   function openCategoryModal() {
//     document.getElementById('categoryModal').style.display = 'flex';
//   }
  
//   function closeCategoryModal() {
//     document.getElementById('categoryModal').style.display = 'none';
//   }
  
//   let modalType;
  
//     function openModal(type) {
//       modalType = type;
//       document.getElementById('modal').style.display = 'flex';
//     }
//     function showForm(formId) {
//       // Hide all forms
//       var forms = document.querySelectorAll('.form');
//       forms.forEach(function(form) {
//         form.style.display = 'none';
//       });
  
//       // Show the selected form
//       var selectedForm = document.getElementById(formId);
//       if (selectedForm) {
//         selectedForm.style.display = 'block';
//       }
//     }
//    function toggleForm(formId) {
//         var form = document.getElementById(formId);
//         form.style.display = form.style.display === 'none' ? 'flex' : 'none';
//       }
  
//   document.getElementById('addItemForm').addEventListener('submit', function (event) {
//       event.preventDefault(); // Prevent the form from submitting and reloading the page
  
//       // Add your logic to check if the item is already added (for demonstration purposes, I'm using a variable 'itemAlreadyAdded')
//       var itemAlreadyAdded = true; // Replace this with your actual logic
  
//       if (itemAlreadyAdded) {
//           showNotification();
//       } else {
//           // Continue with the form submission or item addition logic
//           console.log('Add the item here...');
//       }
//   });
//   document.getElementById('addItemForm').addEventListener('submit', function (event) {
//       event.preventDefault(); // Prevent the form from submitting and reloading the page
  
//       // Add your logic to check if the item is already added (for demonstration purposes, I'm using a variable 'itemAlreadyAdded')
//       var itemAlreadyAdded = true; // Replace this with your actual logic
  
//       if (itemAlreadyAdded) {
//           showNotificationModal();
//       } else {
//           // Continue with the form submission or item addition logic
//           console.log('Add the item here...');
//       }
//   });
  
//   function showNotificationModal() {
//       var modal = document.getElementById('notificationModal');
//       modal.style.display = 'flex';
//   }
  
//   function hideNotificationModal() {
//       var modal = document.getElementById('notificationModal');
//       modal.style.display = 'none';
//   }
  
  
//   document.addEventListener('DOMContentLoaded', function () {
//           var addItemForm = document.getElementById('addItemForm');
//           var itemAddedModal = document.getElementById('itemAddedModal');
//           var okayButton = document.getElementById('okayButton');
//           var itemList = document.getElementById('itemlist');
//           var cancelButton = document.getElementById('cancelButton');
  
//           // Handle form submission
//           document.getElementById('addButton').addEventListener('click', function () {
//               // Perform actions to add the item and display the added item
//               // For demonstration purposes, let's just show the confirmation modal
//               itemAddedModal.style.display = 'block';
  
//               // Close the add item form
//               addItemForm.style.display = 'none';
//           });
  
//           // Handle click on the "Cancel" button
//           document.getElementById('cancelButton').addEventListener('click', function () {
//               // Perform actions to go back to the item list
//               // For demonstration purposes, let's just close the modal
//               addItemForm.reset();
//               itemAddedModal.style.display = 'none';
//           });
  
//            cancelButton.addEventListener('click', function () {
//               // Perform actions to close the form
//               addItemForm.reset();
//               addItemForm.style.display = 'none';
//             });
  
//           // Handle click on the "Okay" button in the confirmation modal
//           okayButton.addEventListener('click', function () {
//               // Perform actions, such as navigating to the item list or other actions
//               itemAddedModal.style.display = 'none';
//               addItemForm.style.display = 'none';  // Hide the add item form
//               itemList.scrollIntoView({ behavior: 'smooth' });
//           });
//       })
//   function selectAllItems() {
//           // Replace this with the actual logic for selecting all items
//           var checkboxes = document.querySelectorAll('.form-items input[type="checkbox"]');
//           checkboxes.forEach(function (checkbox) {
//               checkbox.checked = document.getElementById('selectAllCheckbox').checked;
//           });
//       }
//        function confirmRemoveItems() {
//       var checkbox = document.getElementById('selectAllCheckbox');
      
//       if (checkbox.checked) {
//         var confirmDelete = confirm('Do you want to delete the selected items?');
  
//         if (confirmDelete) {
//           // Add your logic to remove items here
//           alert('Items deleted!');
//         } else {
//           // Uncheck the checkbox if the user cancels the deletion
//           checkbox.checked = false;
//         }
//       }
//     }
//     function previewImage() {
//           var fileInput = document.getElementById('myFile');
//           var previewImage = document.getElementById('previewImage');
  
//           if (fileInput.files && fileInput.files[0]) {
//               var reader = new FileReader();
  
//               reader.onload = function (e) {
//                   previewImage.src = e.target.result;
//               };
  
//               reader.readAsDataURL(fileInput.files[0]);
//           }
//       }
  
//       function closeModal() {
//            document.getElementById('modal').style.display = 'none';
//       }
  
//       function cancel() {
//           let text = "Press a button OK to cancel.";
  
//           if (confirm(text) == true) {
//             closeModal();
//           } else { false;
//           }
//       }
  
//       function addItem() {
//             const name = document.getElementById('nameInput').value;
//             const image = document.getElementById('myFile').value;
  
//             if (name && image) {
//               alert(`Added ${modalType}: ${name}`);
//               closeModal();
//               // Perform additional actions, such as updating the UI or sending data to a server
//             } else {
//               alert('Please enter both name and image URL.');
//             }
//           }
//           function openItemForm() {
//             document.getElementById('addItemForm').style.display = 'flex';
//         }
        
//         function closeItemForm() {
//             document.getElementById('addItemForm').style.display = 'none';
//         }
        
//         function previewImage() {
//             var input = document.getElementById("item-myFile");
//             var preview = document.getElementById("item-preview");
//             var previewSection = document.getElementById("previewSection");
        
//             if (input.files && input.files[0]) {
//                 var reader = new FileReader();
        
//                 reader.onload = function (e) {
//                     preview.src = e.target.result;
//                     previewSection.style.display = "block";
//                 };
        
//                 reader.readAsDataURL(input.files[0]);
//             }
//         }
        
//         function cancelItem() {
//             closeItemForm();
//             // Your cancel item logic heredocument.getElementById('addItemForm').style.display = 'none';
//         }
        
//         function addItem() {
//             closeItemForm();
//             var itemName = document.getElementById('item-itemName').value;
//                 var previewImage = document.getElementById('previewSection').style.display;
                
//                 // Perform validation or further processing as needed
        
//                 // Example: Log the values
//                 console.log('Item Name:', itemName);
//                 console.log('Preview Image:', previewImage);
        
//                 // Add your logic to save or process the item here
        
//                 // Hide the form after adding
//                 document.getElementById('addItemForm').style.display = 'none';
//         }
//code ni nicole end dito

document.addEventListener('DOMContentLoaded', function() {
    itemDisplay = document.getElementById('item_information');
    
    var categoryButtons = document.querySelectorAll('.category_button');
    categoryButtons.forEach(function(button) {
        button.addEventListener('click', function() {
            var category = this.getAttribute('data-category');
            hideAllCategoryButtons()
            if (category !== null && category !== 'null') {
                showItem(category);
            }
        });
    });
});


function showBorrowForm(itemId) {
    fetchData(itemId);  // Assuming fetchData function handles displaying the item details
}

function goBack() {
    showAllCategoryButtons();
}


