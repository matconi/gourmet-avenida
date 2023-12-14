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
                    '<p class="text-danger">Erro inesperado ao adicionar favorito!</p>');
                console.error(err);
            }
        });
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
                    '<p class="text-danger">Erro inesperado ao remover favorito!</p>');
                console.error(err);
            }
        });
    }

    // add to cart form
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
                changeTotalQuantity(response);
            }, 
            error: err => {
                addToCartForm.html(
                    '<p class="text-danger">Erro inesperado ao adicionar ao carrinho!</p>');
                console.error(err);
            }
        });
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