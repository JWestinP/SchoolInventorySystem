var cleaning = document.getElementById('cleaning')
var gadget = document.getElementById('gadget')
var furniture = document.getElementById('furniture')
var room = document.getElementById('room')
var dean = document.getElementById('dean')
const buttons = document.getElementsByClassName('category_button')
const selectItem = document.querySelectorAll('.item_button')
const closeItem = document.querySelectorAll('[data-close-button]')
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

function fetchData(itemId) {
    fetch(`/api/cleaning_inventory/`)
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
                    closeModal();
                }
            });

            document.getElementById('item_body').innerHTML = `
                <p>Description: ${selectedItem.item_description}</p>
                <p>Total Quantity: ${selectedItem.item_total_quantity}</p>
                <p>Borrowed Quantity: ${selectedItem.item_borrowed_quantity}</p>
                <p>Available Quantity: ${selectedItem.item_current_quantity}</p>
            `;
            openItem();
        })
        .catch(error => console.error('Error fetching data:', error));
}

// Update your existing click event listener
selectItem.forEach(button => {
    button.addEventListener('click', () => {
        const itemId = button.getAttribute('data-item-target');
        console.log('Button Clicked for Item ID:', itemId);

        // Call the function to fetch data and update the modal
        fetchData(itemId);
    });
});

closeItem.forEach(button => {
    button.addEventListener('click', () => {
        console.log('Close Button Clicked')
        closeModal()
    });
});

function openItem() {
    console.log('Opening Item');
    if (itemInformation) {
        itemInformation.classList.add('active');
        overlay.classList.add('active');
    }
}

function closeModal() {
    console.log('Closing Item');
    itemInformation.classList.remove('active');
    overlay.classList.remove('active');
}

// Close the modal if the user clicks outside of it
overlay.addEventListener('click', () => {
    console.log('Overlay Clicked')
    closeModal()
});
