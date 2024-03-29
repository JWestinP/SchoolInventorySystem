const userContainer = document.getElementById('user_info')
const historyContainer = document.getElementById('user_borrowed_info')


function showUser(user_pk){
    console.log('Sending request for user with id:', user_pk)

    var xhr = new XMLHttpRequest()
    xhr.open('GET', '/get_user/?user_id=' + encodeURIComponent(user_pk), true)
    xhr.send()

    xhr.onload = function(){
        console.log('Response received:', xhr.responseText)
        if (xhr.status != 200) {
            console.error('Error ' + xhr.status + ': ' + xhr.statusText)
        } 
        else {
            try {
                var response = JSON.parse(xhr.responseText);
                if (response && response.user) {
                    var user = response.user;
                
                    // Access the data from the response
                    var userId = user.id;
                    var userName = user.username;
                    var totalRecents = response.total_recents;
                    var totalUnreturned = response.total_unreturned;
                
                    // Update the HTML content
                    document.getElementById('user_info').innerHTML = `
                        <p>User Name: ${userName}</p>
                        <button id="user_recents" onclick="showUserHistory(${userId})">Total Recents: ${totalRecents}</button>
                        <button id="user_unreturned" onclick="showUserUnreturned(${userId})">Total Unreturned: ${totalUnreturned}</button>
                        <button onclick='reloadPage()'> Back</button>
                    `;
                } else {
                    console.error('User data not found in the response');
                }
            }
            catch (error) {
                console.error('Error parsing JSON:', error)
            }
        }
        openUser(userContainer)
    }
}

function showUserHistory(user_pk) {
    console.log('Sending request for user with id:', user_pk);

    var xhr = new XMLHttpRequest();
    xhr.open('GET', '/get_user_history/?user_id=' + encodeURIComponent(user_pk), true);
    xhr.send();

    xhr.onload = function () {
        console.log('Response received:', xhr.responseText);
        if (xhr.status != 200) {
            console.error('Error ' + xhr.status + ': ' + xhr.statusText);
        } else {
            try {
                var response = JSON.parse(xhr.responseText);
                if (response && response.user_history) {
                    var userHistory = response.user_history;
                    var itemCounts = {};

                    // Loop through each Borrowed_Item in userHistory
                    userHistory.forEach(function (borrowedItem) {
                        var itemId = borrowedItem.item_stock.item_information.item_id;
                        var itemStock = borrowedItem.item_stock.item_information.item_category
                        console.log(itemStock)

                        if (itemCounts[itemId]) {
                            itemCounts[itemId]++;
                        } else {
                            itemCounts[itemId] = 1;
                        }
                    });

                    // Generate HTML content
                    var htmlContent = '<h2>User History</h2><ul>';
                    for (var itemId in itemCounts) {
                        console.log(itemId)
                        var itemName = userHistory.find(item => item.item_stock.item_information.item_id == itemId).item_stock.item_information.item_name;
                        htmlContent += '<li>' + itemName + '(' + itemCounts[itemId] + ')' + '</li>';
                    }
                    htmlContent += '</ul>';

                    // Insert HTML content into the userHistoryContainer
                    historyContainer.innerHTML = htmlContent;

                } else {
                    console.error('User history data not found in the response');
                }
            } catch (error) {
                console.error('Error parsing JSON:', error);
            }
        }
        openHistory(historyContainer)
    }
}

function showUserUnreturned(user_pk) {
    console.log('Sending request for user with id:', user_pk);

    var xhr = new XMLHttpRequest();
    xhr.open('GET', '/get_user_unreturned/?user_id=' + encodeURIComponent(user_pk), true);
    xhr.send();

    xhr.onload = function () {
        console.log('Response received:', xhr.responseText);
        if (xhr.status != 200) {
            console.error('Error ' + xhr.status + ': ' + xhr.statusText);
        } else {
            try {
                var response = JSON.parse(xhr.responseText);
                if (response && response.user_unreturned) {
                    var userUnreturned = response.user_unreturned;
                    var itemCounts = {};

                    // Loop through each Borrowed_Item in userHistory
                    userUnreturned.forEach(function (unreturnedItem) {
                        var itemId = unreturnedItem.item_borrowed.item_stock.item_information.item_id;

                        if (itemCounts[itemId]) {
                            itemCounts[itemId]++;
                        } else {
                            itemCounts[itemId] = 1;
                        }
                    });

                    // Generate HTML content
                    var htmlContent = '<h2>User Unreturned</h2><ul>';
                    for (var itemId in itemCounts) {
                        console.log(itemId)
                        var itemName = userUnreturned.find(item => item.item_borrowed.item_stock.item_information.item_id == itemId).item_borrowed.item_stock.item_information.item_name;
                        htmlContent += '<li>' + itemName + '(' + itemCounts[itemId] + ')' + '</li>';
                    }
                    htmlContent += '</ul>';

                    // Insert HTML content into the userHistoryContainer
                    historyContainer.innerHTML = htmlContent;

                } else {
                    console.error('User history data not found in the response');
                }
            } catch (error) {
                console.error('Error parsing JSON:', error);
            }
        }
        openHistory(historyContainer)
    }
}


function openUser(userContainer) {
    console.log('Opening user');
    if (userContainer) {
        userContainer.classList.add('active');
    }
}

function openHistory(historyContainer) {
    console.log('Opening History');
    if (historyContainer) {
        historyContainer.classList.add('active');
    }
}

function reloadPage(){
    location.reload()
}

