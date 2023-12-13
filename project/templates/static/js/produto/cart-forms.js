$(this).ready(() => {
    const incrementCartBtn = $('.increment-cart');
    const decrementCartBtn = $('.decrement-cart');
    const removeFromCartBtn = $('.remove-from-cart');
    const cleanCartForm = $('#clean-cart-form');
    const jsonData = JSON.parse($('#json-data').text());
    const csrftoken = Cookies.get('csrftoken');

    // imcrement/decrement cart button
    function incrementCart(target) {
        $.ajax({
            url: jsonData.urls.increment_cart,
            type: 'GET',
            data: {
                "id": target.find('input[name="id"]').val(),
            },
            success: response => {
                loadMessages(response.messages);
                refreshQuantityUnit(response.unit_in_cart, target);
            }, 
            error: err => {
                target.html(
                    '<p class="text-danger">Erro inesperado ao adicionar ao carrinho!</p>');
                console.error(err);
            }
        });
    }

    function decrementCart(target) {
        $.ajax({
            url: jsonData.urls.decrement_cart,
            type: 'GET',
            data: {
                "id": target.find('input[name="id"]').val(),
            },
            success: response => {
                loadMessages(response.messages);
                refreshQuantityUnit(response.unit_in_cart, target);
            }, 
            error: err => {
                target.html(
                    '<p class="text-danger">Erro inesperado ao adicionar ao carrinho!</p>');
                console.error(err);
            }
        });
    }

    function refreshQuantityUnit(unitInCart, target) {
        const quantityContainer = target.parent().find($('.quantity'));
        let original = quantityContainer.text();
    
        if (original == 1 && unitInCart.quantity > 1) {
            target.parent().find('.decrement-cart').removeClass('d-none');
        } else if (unitInCart.quantity == 1) {
            target.parent().find('.decrement-cart').addClass('d-none');
        }
        quantityContainer.text(unitInCart.quantity);

        refreshQuantityPrice(unitInCart, target);
    }

    function refreshQuantityPrice(unitInCart, target) {
        const quantityPriceContainer = target.parent().parent().parent().find($('.unit-quantity-price'));
        quantityPriceContainer.text(`R$ ${unitInCart.quantity_price.toFixed(2).toString().replace('.', ',')}`);
    }

    // remove from cart form
    function removeFromCart(unitId, relatedTarget) {
        $.ajax({
            url: jsonData.urls.remove_from_cart,
            type: 'POST',
            headers: { 'X-CSRFToken': csrftoken },
            data: {
                "id": unitId
            },
            success: response => {
                loadMessages(response.messages);
                $('#removeModal').modal('hide');
                relatedTarget.parent().parent().remove();
            }, 
            error: err => {
                $('#removeModal').modal('hide');
                relatedTarget.html(
                    '<p class="text-danger">Erro inesperado ao remover do carrinho!</p>');
                console.error(err);
            }
        });
    } 

    // clean cart form
    function cleanCart() {
        $.ajax({
            url: jsonData.urls.clean_cart,
            type: 'POST',
            headers: { 'X-CSRFToken': csrftoken },
            success: response => {
                loadMessages(response.messages);

                $('#cleanModal').modal('hide');
                emptyCart();
            }, 
            error: err => {
                $('#cleanModal').modal('hide');
                cleanCartForm.html(
                    '<p class="text-danger">Erro inesperado ao limpar carrinho!</p>');
                console.error(err);
            }
        });
    }

    // utils
    function emptyCart() {
        $('#cart-table').html(`
            <p class="lead">Atualmente o seu Carrinho se encontra vazio.</p>
        `);
        $('#cart-actions').remove();
    }

    // events
    incrementCartBtn.click(event => { 
        incrementCart($(event.currentTarget));
    });
    decrementCartBtn.click(event => {  
        decrementCart($(event.currentTarget));
    });
    $('#removeModal').on('show.bs.modal', event => {
        const button = $(event.relatedTarget); 
        const unitName = button.attr('data-unit-name');   
        const unitId = button.attr('data-unit-id');   
       
        $('.unit-name').text(unitName);
        $('#unit-id').val(unitId);

        removeFromCartBtn.click(() => {  
            removeFromCart(unitId, button);
        });
    });
    cleanCartForm.submit(event => {  
        event.preventDefault();
        cleanCart();
    });
});