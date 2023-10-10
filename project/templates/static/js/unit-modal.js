$(this).ready(() => {
    $('#removeModal').on('show.bs.modal', (e) => {
        const button = $(e.relatedTarget); 
        const unitName = button.attr('data-unit-name');   
        const unitId = button.attr('data-unit-id');   
       
        $('.unit-name').text(unitName);
        $('#unit-id').val(unitId);
    });
});