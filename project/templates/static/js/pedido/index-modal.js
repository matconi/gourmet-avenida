$(this).ready(() => { 
    $('#cancelModal').on('show.bs.modal', event => {
        const button = $(event.relatedTarget); 
        const orderId = button.attr('data-order-id');   
       
        $('#order-id').val(orderId);
    });
});