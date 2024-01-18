const userContainer = document.getElementById('user_info')

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
                        <p>Total Recents: ${totalRecents}</p>
                        <p>Total Unreturned: ${totalUnreturned}</p>
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
 

function openUser(userContainer) {
    console.log('Opening user');
    if (userContainer) {
        userContainer.classList.add('active');
    }
}

function reloadPage(){
    location.reload()
}

