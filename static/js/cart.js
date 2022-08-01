var updateBtn = document.getElementsByClassName('update-cart')

for(var i = 0; i < updateBtn.length; i++){
    updateBtn[i].addEventListener('click',function(){
    var mealId = this.dataset.product;
    var action = this.dataset.action
    console.log('mealId:',mealId,'action:',action)
    console.log ('User:' , user)
    if (user != 'Anonymous'){
        updateorder(mealId,action)
    }

})
   

    }

    function updateorder(mealId,action){
        console.log ('sending data.....')

        var url = '/updatemenu/'
        fetch(url, {
            method:'POST',
            headers:{
                'Content-Type':'application/json',
                'X-CSRFToken':csrftoken,
            },
            body:JSON.stringify({'mealId':mealId,'action':action})
    })
        .then((response) =>{
            return response.json()
        })
    
        .then((data) =>{
            console.log('data:' ,data)
            location.reload()
        })



    }

