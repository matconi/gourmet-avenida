$(this).ready(() => {
    const favoriteForm = $('#favorite-form');
    const jsonData = JSON.parse($('#json-data').text());
    const csrftoken = Cookies.get('csrftoken');

    function toastAdded(response) {
        $('.favorite-toast-body').html(`
            ${response.name} adicionado aos favoritos.
            <a href="${response.url}">Visualizar</a>
        `);
        const toast = new bootstrap.Toast($('#favorite-toast'));
        toast.show();
    }

    function addFavorite() {     
        console.log($('#unit-id-favorite').val());
        $.ajax({
            url: jsonData.add_favorite_url,
            type: 'POST',
            data: {
                "id": $('#unit-id-favorite').val()
            },
            headers: { 'X-CSRFToken': csrftoken },
            success: response => {
                // favoriteForm.html("");

               toastAdded(response);
            }, 
            error: err => {
                favoriteForm.html(
                    '<p class="text-danger"> Erro ao adicionar favorito!</p>');
                console.error(err);
            }
        });
    }
    favoriteForm.on('submit', event => {
        event.preventDefault();
        addFavorite();
    });
});