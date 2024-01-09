var itemDisplay
const category = document.getElementsByClassName('category_button')
const selectItem = document.querySelectorAll('.item_button')
const informationId = document.getElementById('item_information')
const backCategory = document.getElementById('back_category')
const itemContainer = document.getElementById('item_list')
const backEditButton = document.getElementById('edit_back_buttons')

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
    
                document.getElementById('item_body').innerHTML = `
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
                                        <button data-delete-target="${selectedItem.item_id}" onclick="deleteItem(${selectedItem.item_id})">-</button>
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
    itemContainer.innerHTML = '';

}

function deleteItem(item_id) {
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
                            
                            } else if (data.error) {
                                
                                console.error(data.error);
                            }
                        })
                        .catch(error => console.error('Error submitting form:', error));
                    });                   
                }
        })
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
