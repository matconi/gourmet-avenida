$(this).ready(() => {
    const favoriteForm = $('#favorite-form');
    const addToCartForm = $('#add-to-cart-form');
    const jsonData = JSON.parse($('#json-data').text());
    const csrftoken = Cookies.get('csrftoken');

    // add favorite form
    function addFavorite() {     
        $.ajax({
            url: jsonData.urls.add_favorite,
            type: 'POST',
            data: {
                "id": $('#unit-id-favorite').val()
            },
            headers: { 'X-CSRFToken': csrftoken },
            success: response => {
               removeFavoriteForm();
               loadMessages(response.messages);
            }, 
            error: err => {
                favoriteForm.html(
                    '<p class="text-danger">Erro ao adicionar favorito!</p>');
                console.error(err);
            }
        });
    }

    function addFavoriteForm() {
        if (jsonData.permissions.add_favorite) {
            $('#favorite-form').attr('action', jsonData.urls.add_favorite).attr('title', 'Adicionar favorito');
            $('#favorite-form button').removeClass('btn-warning text-primary').addClass('btn-outline-warning');
        } else {
            $('#favorite-form').remove();
        }
    }

    // remove favorite form
    function removeFavorite() {     
        $.ajax({
            url: jsonData.urls.remove_favorite,
            type: 'POST',
            data: {
                "id": $('#unit-id-favorite').val()
            },
            headers: { 'X-CSRFToken': csrftoken },
            success: response => {
               addFavoriteForm();
               loadMessages(response.messages);
            }, 
            error: err => {
                favoriteForm.html(
                    '<p class="text-danger">Erro ao remover favorito!</p>');
                console.error(err);
            }
        });
    }

    function removeFavoriteForm() {
        if (jsonData.permissions.remove_favorite) {
            $('#favorite-form').attr('action', jsonData.urls.remove_favorite).attr('title', 'Remover favorito');
            $('#favorite-form button').removeClass('btn-outline-warning').addClass('btn-warning text-primary');
        } else {
            $('#favorite-form').remove();
        }
    }

    // add to cart form
    function loadMessages(messages) {
        $('#toast-container').empty();

        for (let type in messages) {
            const toastConf = getTypeConf(type);
            
            let messageList = messages[type];
            showToast(toastConf, messageList);
        }  
    }

    function addToCart() {    
        $.ajax({
            url: jsonData.urls.add_to_cart,
            type: 'GET',
            data: {
                "id": $('#unit-id-cart').val(),
                "qty": $('#qty').val()
            },
            success: response => {
                loadMessages(response.messages);
            }, 
            error: err => {
                addToCartForm.html(
                    '<p class="text-danger">Erro ao adicionar ao carrinho!</p>');
                console.error(err);
            }
        });
    }

    // utils
    function getTypeConf(type) {
        switch (type) {
            case 'success':
                return {
                    "name": 'success',
                    "headerText": 'Sucesso!',
                    "delay": 3000
                }
            case 'warning':
                return {
                    "name": 'warning',
                    "headerText": 'Aviso!',
                    "delay": 7000
                }   
            case 'danger':
                return {
                    "name": 'danger',
                    "headerText": 'Erro!',
                    "delay": 8000
                }             
            default:
                return {
                    "name": 'info',
                    "headerText": 'Informação',
                    "delay": 5000
                }
        }
    }

    function showToast(typeConf, messageList) {
        for (let message of messageList) {
            $('#toast-container').append(`
                <div class="toast hider" role="alert" aria-live="assertive" aria-atomic="true" data-bs-delay="${typeConf.delay}">
                    <div class="toast-header">
                        <strong class="my-auto alert bg-${typeConf.name} p-1 text-light" id="type-message">${typeConf.headerText}</strong>
                        <button type="button" class="btn-close ms-auto" data-bs-dismiss="toast" aria-label="Close"></button>
                    </div>
                    <p class="container fs-6 toast-body">${message}</p>
                </div>
            `);
            $('.toast').toast('show');
        }
    }

    // events
    favoriteForm.submit(event => {
        event.preventDefault();
        favoriteForm.attr('action') === jsonData.urls.remove_favorite ? removeFavorite() : addFavorite();
    });
    addToCartForm.submit(event => {
        event.preventDefault();
        addToCart();
    });
});