$(this).ready(() => {
    const favoriteForm = $('#favorite-form');
    const jsonData = JSON.parse($('#json-data').text());
    const csrftoken = Cookies.get('csrftoken');

    function toastAdded(response) {
        $('.toast-body').html(`
            <strong>${response.name}</strong> adicionado aos favoritos.
            <a href="${response.url}">Visualizar</a>
        `);
        const toast = new bootstrap.Toast($('.toast'));
        toast.show();
    }

    function toastRemoved(response) {
        $('.toast-body').html(`
            <strong>${response.name}</strong> removido dos favoritos.
            <a href="${response.url}">Visualizar</a>
        `);
        const toast = new bootstrap.Toast($('.toast'));
        toast.show();
    }

    function addFavorite() {     
        $.ajax({
            url: jsonData.add_favorite_url,
            type: 'POST',
            data: {
                "id": $('#unit-id-favorite').val()
            },
            headers: { 'X-CSRFToken': csrftoken },
            success: response => {
               removeFavoriteForm();
               toastAdded(response);
            }, 
            error: err => {
                favoriteForm.html(
                    '<p class="text-danger">Erro ao adicionar favorito!</p>');
                console.error(err);
            }
        });
    }

    function removeFavorite() {     
        $.ajax({
            url: jsonData.remove_favorite_url,
            type: 'POST',
            data: {
                "id": $('#unit-id-favorite').val()
            },
            headers: { 'X-CSRFToken': csrftoken },
            success: response => {
               addFavoriteForm();
               toastRemoved(response);
            }, 
            error: err => {
                favoriteForm.html(
                    '<p class="text-danger">Erro ao remover favorito!</p>');
                console.error(err);
            }
        });
    }

    function addFavoriteForm() {
        if (jsonData.add_favorite_permission) {
            $('#favorite-form').attr('action', jsonData.add_favorite_url).attr('title', 'Adicionar favorito');
            $('#favorite-form button').removeClass('btn-warning text-primary').addClass('btn-outline-warning');
        } else {
            $('#favorite-form').remove();
        }
    }

    function removeFavoriteForm() {
        if (jsonData.remove_favorite_permission) {
            $('#favorite-form').attr('action', jsonData.remove_favorite_url).attr('title', 'Remover favorito');
            $('#favorite-form button').removeClass('btn-outline-warning').addClass('btn-warning text-primary');
        } else {
            $('#favorite-form').remove();
        }
    }

    favoriteForm.on('submit', event => {
        event.preventDefault();
        favoriteForm.attr('action') === jsonData.remove_favorite_url ? removeFavorite() : addFavorite();
    });
});