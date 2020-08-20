let updateCart = document.getElementsByClassName('update-cart');

for (let i=0 ; i< updateCart.length; i++){
    updateCart[i].addEventListener('click', function(e){
        let productId = this.dataset.product
        let action = this.dataset.action

        if (user=='AnonymousUser'){
            addCookieItem(productId, action)

        }else{
            updateUserOrder(productId, action)
        }

    })
}

function addCookieItem (productId, action){
    console.log('USER:', user)

    if (action=='add'){
        if (cart[productId]== undefined){
            cart[productId] = {'quantity' : 1}
        }else{
            cart[productId]['quantity'] += 1 
        }

    }
    if (action=='remove'){
        cart[productId]['quantity'] -= 1
        if (cart[productId]['quantity']<=0){
            console.log('removed')
            delete cart[productId]
        }
    }
    console.log('Cart:', cart)
    document.cookie = 'cart=' + JSON.stringify(cart) + ';domain=;path=/'
    location.reload()
}


function updateUserOrder(productId, action){
    console.log('sent data')
    let url  = '/update/'
    fetch(url,{
        method:'POST',
        headers :{
            'Content-Type' : 'application/json',
            'X-CSRFToken' : csrftoken,
        },
        body:JSON.stringify({'productId' : productId,'action' : action})
    })

    .then((response) =>{
        return response.json()
    })

    .then((data)=>{
        console.log(data)
        location.reload()
    })
}