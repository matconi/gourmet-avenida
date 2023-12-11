$(this).ready(() => {
    const addToCartForm = $('.add-to-cart-form');
    const jsonData = JSON.parse($('#json-data').text());

    // add to cart form
    function addToCart(target) {
        $.ajax({
            url: jsonData.urls.add_to_cart,
            type: 'GET',
            data: {
                "id": target.find('input[name="id"]').val(),
                "qty": '1'
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

    // events
    addToCartForm.submit(event => {
        event.preventDefault();
        addToCart($(event.currentTarget));
    });
});