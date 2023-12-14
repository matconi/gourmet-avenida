$(this).ready(() => {
    const addFromListToCartForm = $('.add-to-cart-form');
    const jsonData = JSON.parse($('#json-data').text());

    // add to cart form
    function addFromListToCart(target) {
        $.ajax({
            url: jsonData.urls.add_to_cart,
            type: 'GET',
            data: {
                "id": target.find('input[name="id"]').val(),
            },
            success: response => {
                loadMessages(response.messages);
                changeTotalQuantity(response);
            }, 
            error: err => {
                addFromListToCartForm.html(
                    '<p class="text-danger">Erro ao solicitar adição ao carrinho!</p>');
                console.error(err);
            }
        });
    }

    // events
    addFromListToCartForm.submit(event => {
        event.preventDefault();
        addFromListToCart($(event.currentTarget));
    });
});