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
    if (itemType === 'cleaning') {
        category = 'cleaning';
        headerId = 'cleaning_header'
        bodyId = 'cleaning_body'
        informationId = document.getElementById('cleaning_information')
    } 
    else if (itemType === 'room') {
        category = 'room';
        headerId = 'room_header'
        bodyId = 'room_body'
        informationId = document.getElementById('room_information')
    } 
    else if (itemType === 'furniture') {
        category = 'furniture';
        headerId = 'furniture_header'
        bodyId = 'furniture_body'
        informationId = document.getElementById('furniture_information')
    } 
    else if (itemType === 'gadget') {
        category = 'gadget';
        headerId = 'gadget_header'
        bodyId = 'gadget_body'
        informationId = document.getElementById('gadget_information')
    } 
    else if (itemType === 'dean') {
        category = 'dean';
        headerId = 'dean_header'
        bodyId = 'dean_body'
        informationId = document.getElementById('dean_information')
    } 
    else {
        console.error('Invalid item type:', itemType);
        return;
    }

    fetch('/api/item_inventory/')
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

