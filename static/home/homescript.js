var cleaning = document.getElementById('cleaning')
var gadget = document.getElementById('gadget')
var furniture = document.getElementById('furniture')
var room = document.getElementById('room')
var dean = document.getElementById('dean')
const buttons = document.getElementsByClassName('category_button')
const selectItem = document.querySelectorAll('.item_button')
const overlay = document.getElementById('overlay')
const itemInformation = document.getElementById('itemInformation');

console.log('itemInformation:', itemInformation);
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
    } 
    else if (itemType === 'room') {
        apiUrl = '/api/room_inventory/';
    } 
    else if (itemType === 'furniture') {
        apiUrl = '/api/furniture_inventory/';
    } 
    else if (itemType === 'gadget') {
        apiUrl = '/api/technology_inventory/';
    } 
    else if (itemType === 'dean') {
        apiUrl = '/api/dean_inventory/';
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
                    closeItem();
                }
            });

            document.getElementById('item_body').innerHTML = `
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

            openItem();
        })
        .catch(error => console.error('Error fetching data:', error));
}

function openItem() {
    console.log('Opening Item');
    if (itemInformation) {
        itemInformation.classList.add('active');
        overlay.classList.add('active');
    }
}

function closeItem() {
    console.log('Closing Item');
    itemInformation.classList.remove('active');
    overlay.classList.remove('active');
}

overlay.addEventListener('click', () => {
    console.log('Overlay Clicked')
    closeItem()
});

selectItem.forEach(button => {
    button.addEventListener('click', () => {
        const itemId = button.getAttribute('data-item-target');
        const itemType = button.getAttribute('data-item-type');
        console.log('Button Clicked for Item ID:', itemId);
        console.log('Item Type:', itemType);
        
        fetchData(itemId, itemType);
    });
});

