var itemDisplay
const category = document.getElementsByClassName('category_button')
const selectItem = document.querySelectorAll('.item_button')
const informationId = document.getElementById('item_information')
const backCategory = document.getElementById('back_category')
const itemContainer = document.getElementById('item_list')
const backEditButton = document.getElementById('edit_back_buttons')
const formId = document.getElementById('add_item')
const categoryId = document.getElementById('add_category_form')
const confirmationPopUp = document.getElementById('delete_confirmation')
const addSuccessPopUp = document.getElementById('success_popup')

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

            // items info
            if (selectedItem) {
                const imageUrl = `${selectedItem.item_photo}`
                document.getElementById('item_header').innerHTML = `
                    <img src="${imageUrl}" alt="${selectedItem.item_name}" style="width: 100px; border:1px solid #E67C37; height: 100px;">
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
    
                document.getElementById('item_body').innerHTML = `
                <table>
                
               <tr>
                    <td>Description</td>
                    <td>Quantity</td>
                    <td>Borrowed</td>
                    <td>Available</td>
                </tr>
                <tr>
                    <td>${selectedItem.item_description}</td>
                    <td>${selectedItem.item_total}</td>
                    <td>${selectedItem.item_borrowed}</td>
                    <td>${selectedItem.item_current}</td>
                </tr>
            </table>
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

function openForm(formId) {
    console.log('Opening item form');
    if (formId) {
        formId.classList.add('active');
    }
}

function openCategoryForm(categoryId) {
    console.log('Opening category form');
    if (categoryId) {
        categoryId.classList.add('active');
    }
}

function openConfirmation(confirmationPopUp) {
    console.log('Opening confirmation');
    if (confirmationPopUp) {
        confirmationPopUp.classList.add('active');
    }
}

function closeItem(informationId) {
    console.log('Closing Item');
    informationId.classList.remove('active');
}

function closeForm() {
    console.log('Closing item form');
    formId.classList.remove('active');
    location.reload()
}

function closeCategoryForm() {
    console.log('Closing category form');
    categoryId.classList.remove('active');
}

function closeConfirmation() {
    console.log('Closing confirmation popup');
    confirmationPopUp.classList.remove('active');
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
    
                document.getElementById('edit_back_buttons').innerHTML = `
                <button onclick="addItem()">Add</button>
                <button class="remove_item">Remove</button>
                <button id="back_category" onclick="showAllCategoryButtons()">Back</button>
                `;
                
                document.getElementById('edit_back_buttons').addEventListener('click', function(event){
                    if (event.target.matches('.remove_item')){
                        itemContainer.innerHTML = ''
                        if (Array.isArray(data.items)) {
                            data.items.forEach(selectedItem => {
                                const imageUrl = `${selectedItem.item_photo}`
                                const itemHTML = `
                                    <div>
                                        <img src="${imageUrl}" alt="${selectedItem.item_name}" style="width: 100px; height: 100px;">
                                        <button data-delete-target="${selectedItem.item_id}" onclick="deleteItem(${selectedItem.item_id})"><i class="fa fa-trash"></i></button>
                                        <p>${selectedItem.item_name} </p>
                                    </div>
                                `
                                itemContainer.innerHTML += itemHTML
        
                            })
                        } 
                        else {
                            console.error('Data does not contain an array:', data)
                            
                        }
                    }
                })

                itemContainer.innerHTML += `<p>${data.items.length} items in category: ${data.items[0].item_category.item_category}</p>`;
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
                            <div>
                                <img src="${imageUrl}" alt="${selectedItem.item_name}" style="width: 100px; height: 100px;">
                                <button data-item-target="${selectedItem.item_id}" class="item_button">${selectedItem.item_name}</button>
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
    var buttonContainer = document.getElementById('edit_back_buttons')
    itemContainer.innerHTML = '';
    buttonContainer.innerHTML = ''

}

function addItem() {
    fetch('/get_item_form/')
        .then(response => response.json())
        .then(data => {
            const formContainer = document.getElementById('add_item_form');
            formContainer.innerHTML = data.item_form_html;
            const itemForm = document.getElementById('itemFormId');
            const csrfToken = document.cookie.split(';').find(cookie => cookie.trim().startsWith('csrftoken=')).split('=')[1];
                if (itemForm) {
                    itemForm.addEventListener('submit', function (event) {
                        event.preventDefault();
                    
                        const formData = new FormData(itemForm);

                        formData.append('csrfmiddlewaretoken', csrfToken);
                        console.log(formData)
                        console.log('FormData:', formData);
                        fetch('/save_item_form/', {
                            method: 'POST',
                            body: formData
                        })
                        .then(response => response.json())
                        .then(data => {
                            console.log(data);
                            if (data.message) {
                                formContainer.innerHTML = ''
                                fetch('/get_stock_form/')
                                    .then(response => response.json())
                                    .then(data => {
                                        console.log(data)
                                        const formContainer = document.getElementById('add_stock_form');
                                        formContainer.innerHTML = data.stock_form_html;
                                        const stockForm = document.getElementById('stockFormId');
                                        if(stockForm){
                                            stockForm.addEventListener('submit', function (event) {
                                                event.preventDefault();
                                                const formStockData = new FormData(stockForm);
                                                formStockData.append('csrfmiddlewaretoken', csrfToken);
                                                fetch('/save_stock_form/', {
                                                    method: 'POST',
                                                    body: formStockData
                                                })
                                                .then(response => response.json())
                                                .then(data => {
                                                    console.log(data);
                                                    if (data.message) {
                                                        formContainer.innerHTML = ''
                                                        formContainer.innerHTML = `
                                                        <div class="confirmation-popup-container">
                                                            <div class="confirmation-popup">
                                                                <p>The item has been successfully added with its stock!</p>
                                                                <button onclick="refreshPage()">Ok</button>
                                                            </div>
                                                        </div>
                                                        `
                                                    } else if (data.error) {
                                                        
                                                        console.error(data.error);
                                                    }
                                                    
                                                })
                                                .catch(error => console.error('Error submitting form:', error));
                                            })
                                        }
                                    })
                            } else if (data.error) {
                                
                                console.error(data.error);
                            }
                        })
                        .catch(error => console.error('Error submitting form:', error));

                    });   
                    openForm(formId)                
                }
        })
}

function deleteItem(item_id) {
    confirmationPopUp.innerHTML = `
    <div class="confirmation-popup-container">
        <div class="confirmation-popup">
            <p>Are you sure you want to delete this item?</p>
            <button class="delete_confirm">Yes</button>
            <button class="delete_denied">No</button>
        </div>
    </div>
    
    `
    openConfirmation(confirmationPopUp)

    confirmationPopUp.addEventListener('click', function(event){
        if (event.target.matches('.delete_confirm')) {
            const csrfToken = document.cookie.split(';').find(cookie => cookie.trim().startsWith('csrftoken=')).split('=')[1];
            fetch(`/delete_item/?item_id=${item_id}`, {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                },
            })
            .then(response => response.json())
            .then(data => {
                console.log(data.message);
                
            })
            .catch(error => console.error('Error:', error));
            confirmationPopUp.innerHTML = `
            <div class="confirmation-popup-container">
                <div class="confirmation-popup">
                    <p>The item has been deleted successfully</p>
                    <button onclick="refreshPage()">Back</button>
                <div>
            </div>
            `
        }
        else if (event.target.matches('.delete_denied')) {
            closeConfirmation()
        }
    })
    
}

function addCategory() {
    fetch('/get_category_form/')
        .then(response => response.json())
        .then(data => {
            const formContainer = document.getElementById('add_category_form');
            formContainer.innerHTML = data.category_form_html;
            const categoryForm = document.getElementById('categoryFormId');
            const csrfToken = document.cookie.split(';').find(cookie => cookie.trim().startsWith('csrftoken=')).split('=')[1];
                if (categoryForm) {
                    categoryForm.addEventListener('submit', function (event) {
                        event.preventDefault();
                    
                        const formData = new FormData(categoryForm);

                        formData.append('csrfmiddlewaretoken', csrfToken);
                        console.log(formData)
                        console.log('FormData:', formData);
                        fetch('/save_category_form/', {
                            method: 'POST',
                            body: formData
                        })
                        .then(response => response.json())
                        .then(data => {
                            console.log(data);
                            if (data.message) {
                                formContainer.innerHTML = `
                                <div class="confirmation-popup-container">
                                    <div class="success-popup">
                                        <p>The item has been successfully added with its stock!</p>
                                        <button onclick="refreshPage()">Ok</button>
                                    </div>
                                </div>   
                                `
                            } else if (data.error) {
                                
                                console.error(data.error);
                            }
                        })
                        .catch(error => console.error('Error submitting form:', error));

                    });
                    openCategoryForm(categoryId)                   
                }
        })
}

function deleteCategory(category_id) {
    confirmationPopUp.innerHTML = `
    <div class="confirmation-popup-container">
        <div class="confirmation-popup">
                <p>Are you sure you want to delete this category?</p>
                <button class="delete_confirm">Yes</button>
                <button class="delete_denied">No</button>
        </div>
    </div>
    `
    openConfirmation(confirmationPopUp)
    
    confirmationPopUp.addEventListener('click', function(event){
        if (event.target.matches('.delete_confirm')) {
            const csrfToken = document.cookie.split(';').find(cookie => cookie.trim().startsWith('csrftoken=')).split('=')[1];
            fetch(`/delete_category/?category_id=${category_id}`, {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                },
            })
            .then(response => response.json())
            .then(data => {
                console.log(data.message);
                
            })
            .catch(error => console.error('Error:', error));

            confirmationPopUp.innerHTML = `
            <div class="confirmation-popup-container">
                <div class="confirmation-popup">
                    <p>The category has been deleted successfully</p>
                    <button onclick="refreshPage()">Back</button>
                </div>
            </div>
            `
        }

        else if (event.target.matches('.delete_denied')) {
            closeConfirmation()
        }
    })
    
}

function editCategory() {
    var xhr = new XMLHttpRequest();
    xhr.open('GET', '/get_category/', true);
    xhr.onload = function () {
        if (xhr.status != 200) {
            console.error('Request failed with status ' + xhr.status);
            
        } else {
            var responseData = JSON.parse(xhr.responseText);
            var categories = responseData.categories;
            var categoryContainer = document.getElementById('category_container');
            
            document.getElementById('edit_category_buttons').innerHTML = `
                <button onclick="addCategory()"><i class="fa fa-plus"></i> Add</button>
                <button class="remove_category"><i class="fa fa-trash"></i>Remove</button>
                <button onclick="refreshPage()">Back</button>
            `

            document.getElementById('edit_category_buttons').addEventListener('click', function(event){
                if (event.target.matches('.remove_category')){
                    categoryContainer.innerHTML = ''
                    if (Array.isArray(categories)) {
                        categories.forEach(category => {
                            const categoryName = category.category_name;
                            console.log(categoryName);
                            document.getElementById
                            const categoryHTML = `
                            <div>
                            <button class="category_button">${category.item_category}</button><br>
                            <button><p onclick="deleteCategory(${category.id})"><i class="fa fa-trash" ></i>Remove</p></button>
                        </div>
                        
                            `;

                            categoryContainer.innerHTML += categoryHTML;
                            
                        });
                    }
                }
            })
            
        }
    };
    xhr.send();
}

function refreshPage() {
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
