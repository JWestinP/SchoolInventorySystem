const returnContainer = document.getElementById('return_container')

function showReturnForm(borrow_id){
    console.log('Sending request for borrowed form with id:', borrow_id);

    var xhr = new XMLHttpRequest();
    xhr.open('GET', '/get_borrow_info/?borrow_id=' + encodeURIComponent(borrow_id), true);
    xhr.send();

    xhr.onload = function(){
        console.log('Response received:', xhr.responseText)
        if (xhr.status != 200) {
            console.error('Error ' + xhr.status + ': ' + xhr.statusText)
        } 
        else {
            try {
                var response = JSON.parse(xhr.responseText);
                if (response && response.borrowed_info && response.unreturned_info) {
                    fetch('/get_return_form/')
                    .then(response => response.json())
                    .then(data => {
                        var borrowed = response.borrowed_info;
                        var unreturned = response.unreturned_info;
                        const formContainer = document.getElementById('return_container');
                        formContainer.innerHTML = data.form_html;

                        const returnForm = document.getElementById('ReturnFormId');

                        if (returnForm) {
                            const returnForm = document.getElementById('ReturnFormId');
                        
                            

                            const csrfToken = document.cookie.split(';').find(cookie => cookie.trim().startsWith('csrftoken=')).split('=')[1];
                            returnForm.addEventListener('submit', function (event) {
                                event.preventDefault();
                            
                                const formData = new FormData(returnForm);
                                formData.append('stock_id', borrowed.item_stock.id)
                                formData.append('unreturned_id', unreturned.id)
                                formData.append('borrowed_id', borrowed.borrow_form_id)
                                formData.append('csrfmiddlewaretoken', csrfToken);
                                console.log(formData)
                                console.log('FormData:', formData);
                                fetch('/save_return_form/', {
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
                        else {
                            console.error('Missing form');
                        }
                    })
                
                   
                } else {
                    console.error('Borrowed data not found in the response');
                }
            }
            catch (error) {
                console.error('Error parsing JSON:', error)
            }
        }
        openReturnForm(returnContainer)
    }    
}

function openReturnForm(returnContainer) {
    console.log('Opening return form');
    if (returnContainer) {
        returnContainer.classList.add('active');
    }
}