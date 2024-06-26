const category = document.getElementsByClassName('category_button')
const selectItem = document.querySelectorAll('.item_button')
const informationId = document.getElementById('item_information')
const backCategory = document.getElementById('back_category')
const itemContainer = document.getElementById('item_list')

var itemDisplay

//In charge of hiding the category buttons when clicking a category
function hideAllCategoryButtons() {
    var categoryButtons = document.querySelectorAll('.category_button');
    categoryButtons.forEach(function(button) {
        button.style.display = 'none';
    });
}

//In charge of showing the category buttons when closing a category
function showAllCategoryButtons() {
    
    var categoryButtons = document.querySelectorAll('.category_button');
    categoryButtons.forEach(function(button) {
        button.style.display = 'inline';

    });
    var itemContainer = document.getElementById('item_list');
    itemContainer.innerHTML = '';

    location.reload()

}

//In charge of showing the item list in a specific category
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
                        <div class="row-container">
                                 <div class="square-container">
                                    <div class="item-photo">
                                        <img src="${imageUrl}" alt="${selectedItem.item_name}" style="width: 100px; height: 100px;">
                                    </div> 
                                    <div class="item-button">  
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

//In charge of showing item information and item borrow form
function fetchData(itemId) {
    fetch('/item_inventory/')
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
                    <button data-close-button class="close_button">&times;</button>  
                        <img src="${imageUrl}" alt="${selectedItem.item_name}" style="width: 150px; border:1px solid black; height: 150px;">
                    </div>
                    <div class="header-info">    
                        <p>Item ID: ${selectedItem.item_id}</p>
                        <p>Name: ${selectedItem.item_name}</p>
                        <p>Category: ${selectedItem.item_category}</p>
                        <p>One per user: ${selectedItem.item_one_time_borrow}</p>
                    </div>
                `;
                document.body.addEventListener('click', function (event) {
                    if (event.target.matches('.close_button')) {
                        console.log('Close Button Clicked');
                        closeItem(informationId);
                    }
                });
    
                document.getElementById('item_body').innerHTML = `
                <table class="table-row">
                
               <tr>
                    <td>Description</td>
                    <td>Total Quantity</td>
                    <td>Total Pristine</td>
                    <td>Borrowed</td>
                    <td>Available</td>
                    <td>Total Damaged</td>
                </tr>
                <tr>
                    <td>${selectedItem.item_description}</td>
                    <td>${selectedItem.item_total}</td>
                    <td>${selectedItem.item_pristine}</td>
                    <td>${selectedItem.item_borrowed}</td>
                    <td>${selectedItem.item_current}</td>
                    <td>${selectedItem.item_damaged}</td>
                </tr>
            </table>
                `;
    
                const csrfToken = document.cookie.split(';').find(cookie => cookie.trim().startsWith('csrftoken=')).split('=')[1];
                if (selectedItem.item_current > 0){
                    fetch('/get_borrow_form/')
                    .then(response => response.json())
                    .then(data => {
                        
                        const formContainer = document.getElementById('item_form');
                        formContainer.innerHTML = data.form_html;
        
                        const borrowForm = document.getElementById('borrowFormId');
                        console.log('borrowForm:', borrowForm);
                        if (borrowForm) {
                            const itemStockInput = borrowForm.querySelector('[name="item_stock"]');
                            console.log(itemStockInput);
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
                                        showPopup(data.message || data.error);
                                    } else if (data.error) {
                                        showPopup(data.message || data.error);
                                        console.error(data.error);
                                    }
                                })
                                .catch(error => console.error('Error submitting form:', error));
                            });
                                            
                        }
                    })
                }

                else {
                    const formContainer = document.getElementById('item_form');
                    formContainer.innerHTML = ''
                }

                openItem(informationId);
            }
            else {
                console.error('Item not found for the given item ID.');
                
            }

        })
        .catch(error => console.error('Error fetching data:', error));
}

//In charge of opening the pop up item window
function openItem(informationId) {
    console.log('Opening Item');
    if (informationId) {
        informationId.classList.add('active');
    }
}

//In charge of closing the pop up item window
function closeItem(informationId) {
    console.log('Closing Item');
    informationId.classList.remove('active');
}

//In charge of showing the item list when a category is clicked
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

//In charge of initializing all the item information in the item list
selectItem.forEach(button => {
    button.addEventListener('click', () => {
        const itemId = button.getAttribute('data-item-target');
        console.log('Button Clicked for Item ID:', itemId);
        console.log('Item Type:', itemType);
        
        fetchData(itemId);
    });
});

//In charge of the pop up window for successful/error action in faculty home
function showPopup(message) {
    const popup = document.getElementById('popup');
    const popupMessage = document.getElementById('popup-message');
    popupMessage.textContent = message;
    popup.classList.add('active');

    document.querySelector('.popup .close-btn').addEventListener('click', function() {
        popup.classList.remove('active');
    });
}