console.log('Adding/removing products from the cart.');

let updateBtns = document.getElementsByClassName('update-cart');

for (let i = 0; i < updateBtns.length; i++){
    updateBtns[i].addEventListener('click', function () {
        let productId = this.dataset.product
        let action = this.dataset.action

        console.log('productId:', productId, 'action: ', action);
        console.log('USER: ', user)                                                                                     // variable defined in base.html

        if (user === 'AnonymousUser'){
            console.log('You are not logged in.');
            alert('You are not logged in.');
        }
        else{
            updateUserOrder(productId, action)
        }
    })
};

function updateUserOrder(productId, action){
    console.log('User is logged in, sending data..');

    var url = '/update_item/'                                                                                           // 'http://127.0.0.1:8000/update_item/'

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({'productId': productId, 'action': action})
    })

     .then((response) => {
        return response.json()
    })

    .then(() => {
        return location.reload()
    });
}
// https://docs.djangoproject.com/en/3.0/ref/csrf/ pasted in request.user location (base.html)

