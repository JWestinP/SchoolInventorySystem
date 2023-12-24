var cleaning = document.getElementById('cleaning');
var gadget = document.getElementById('gadget');
var furniture = document.getElementById('furniture');
var room = document.getElementById('room')
var dean = document.getElementById('dean')
const buttons = document.getElementsByClassName('category_button');


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