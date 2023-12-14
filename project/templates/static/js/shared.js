const jsonData = JSON.parse($('#json-data').text());

function loadMessages(messages) {
    $('#toast-container').empty();

    for (let type in messages) {
        const toastConf = getConfType(type);
        
        let messageList = messages[type];
        showToast(toastConf, messageList);
    }  
}

function getConfType(type) {
    switch (type) {
        case 'success':
            return {
                "name": 'success',
                "headerText": 'Sucesso!',
                "delay": 2500
            }
        case 'warning':
            return {
                "name": 'warning',
                "headerText": 'Aviso!',
                "delay": 5000
            }   
        case 'danger':
            return {
                "name": 'danger',
                "headerText": 'Erro!',
                "delay": 7000
            }             
        default:
            return {
                "name": 'info',
                "headerText": 'Informação',
                "delay": 5000
            }
    }
}

function showToast(confType, messageList) {
    for (let message of messageList) {
        $('#toast-container').append(`
            <div class="toast hider" role="alert" aria-live="assertive" aria-atomic="true" data-bs-delay="${confType.delay}">
                <div class="toast-header">
                    <strong class="my-auto alert bg-${confType.name} p-1 text-light" id="type-message">${confType.headerText}</strong>
                    <button type="button" class="btn-close ms-auto" data-bs-dismiss="toast" aria-label="Close"></button>
                </div>
                <p class="container fs-6 toast-body lead fs-5">${message}</p>
            </div>
        `);
        $('.toast').toast('show');
    }
}

function addFavoriteForm() {
    if (jsonData.permissions.add_favorite) {
        $('#favorite-form').attr('action', jsonData.urls.add_favorite).attr('title', 'Adicionar favorito');
        $('#favorite-form button').removeClass('btn-warning text-primary').addClass('btn-outline-warning');
    } else {
        $('#favorite-form').remove();
    }
}

function removeFavoriteForm() {
    if (jsonData.permissions.remove_favorite) {
        $('#favorite-form').attr('action', jsonData.urls.remove_favorite).attr('title', 'Remover favorito');
        $('#favorite-form button').removeClass('btn-outline-warning').addClass('btn-warning text-primary');
    } else {
        $('#favorite-form').remove();
    }
}

function changeTotalQuantity(response) {
    $('.cart-count').text(`${response.refresh_cart.total_in_cart}x`);
}

function changeTotalPrice(response) {
    $('.cart-total').text(priceFormat(response.refresh_cart.total_price_in_cart));
}

function priceFormat(srcValue) {
    return `R$ ${parseFloat(srcValue).toFixed(2).toString().replace('.', ',')}`;
}