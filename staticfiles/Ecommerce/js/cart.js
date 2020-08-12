console.log('Adding/removing products from the cart.');

let updateBtns = document.getElementsByClassName('update-cart');

for (let i = 0; i < updateBtns.length; i++){
    updateBtns[i].addEventListener('click', function () {
        let productId = this.dataset.product
        let action = this.dataset.action

        console.log('productId:', productId, 'action: ', action);
        console.log('USER: ', user)                                                                                     // zmienna user została zdefiniowana w base.html

        if (user === 'AnonymousUser'){
            console.log('You are not logged in.');
            alert('You are not logged in.');                                                                            // nie działa
        }
        else{
            updateUserOrder(productId, action)
        }
    })
};

function updateUserOrder(productId, action){
    console.log('User is logged in, sending data..');

    var url = '/update_item/'                                                                                           // 'http://127.0.0.1:8000/update_item/'
                                                                                                                        //todo sprawdź fetch() javascript
    fetch(url, {                                                                                                    // drugi argument init nie jest obowiązkowy, używamy go, gdy chcemy użyć metody Http (zamiast np. wyswietlić tylko response)
        method: 'POST',                                                                                                 // metody Http
        headers: {
            'Content-Type': 'application/json',                                                                         // stała wartość
            'X-CSRFToken': csrftoken,                                                                                   // dodajemy po wklejeniu funkcji do base.html?
        },
        body: JSON.stringify({'productId': productId, 'action': action})                                          // co przekazujemy do backendu (update-item: data['productId'], data['action']), musi być przekonwertowane na json (stringify)
    })

     .then((response) => {
        return response.json()
    })

    .then(() => {
        return location.reload()                                                                                        // --> zamieniamy console.log('data', data) na location.reload po wklejeniu funkcji do store.html, zeby strona sie odswieżała i bylo widac aktualna ilosc w koszyku
    });
}

// na tym etapie pojawia się bład --> brak crsf token. Normalnie przesyłamy go w formularzu html, w java script tworzymy nowa funkcję --> https://docs.djangoproject.com/en/3.0/ref/csrf/
// --> wklejamy ją w miejsce, gdzie jest nasz request.user (base.html)
