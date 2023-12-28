$(document).ready(() => {
    const loadMoreBtn = $('#load-more-btn');
    const spinner = $('#spinner');
    const jsonData = JSON.parse($('#json-data').text());
    const alert = $('#no-more-alert');
    
    function loadMore(is_reload) {     
        reloadCardsOnFilter(is_reload);
        const currentItensCount = $('.single-content').length;
        const contentContainer = $("#content");

        $.ajax({
            url: jsonData.urls.load_more,
            type: 'GET',
            data: {
                'offset': currentItensCount,
                'q': $('[name="q"]').val(),
                'cat': $('[name="cat"]').val()
            },
            beforeSend: () => {
                loadMoreBtn.addClass('d-none');
                spinner.removeClass('d-none');
            },
            success: response => {
                spinner.addClass('d-none');
                response.units.map(unit => {
                    renderCard(contentContainer, unit);
                    renderPromotional(unit);
                    renderCardFooter(unit, jsonData);
                });
                const totalUnits = getTotalUnits(is_reload, currentItensCount, response);
                renderNoMoreAlert(currentItensCount, totalUnits, loadMoreBtn);
            },
            error: err => {
                spinner.addClass('d-none');
                contentContainer.html('<p class="text-danger">Erro ao carregar a lista de produtos!</p>');
                console.error(err);
            }
        });
    }

    function reloadCardsOnFilter(is_reload) {
        if (is_reload) {
            $('.single-content').remove();
        }
        alert.addClass('d-none');
    }

    function renderCard(contentContainer, unit) {
        const card = `
            <div class="single-content col-6 col-sm-4 col-lg-3 mb-4">
                <div class="card shadow-sm">
                    <a href="/produtos/${unit.category_slug}/${unit.product_slug}?uid=${unit.uid}">        
                        <img class="card-img-top d-block w-100" src="${unit.image_sm}" alt="${unit.name}">  
                    </a>           
                    <div class="card-body d-flex flex-column">
                        <strong>
                            <h5 class="card-title fs-6">${unit.name}</h5>
                        </strong>
                        
                        <div class="product-price-block text-center">
                            <span class="product-price text-success">
                                ${currencyFormat(unit.price)}
                            </span>
                            <span id="unit-promotional-${unit.uid}"></span>         
                        </div>
                    </div>
                    <span id="card-footer-${unit.uid}"></span>
                </div>
            </div>`;
        contentContainer.append(card);
    }

    function renderPromotional(unit) {
        const promotional = $(`#unit-promotional-${unit.uid}`);

        if (unit.promotional === null) {
            promotional.remove();
        } else {
            promotional.html(`
                <small class="pl-2 text-muted">
                    <del>
                        ${currencyFormat(unit.promotional)}
                    </del>
                </small>
            `);
        }
    }
    
    function renderCardFooter(unit, jsonData) {
        const footer = $(`#card-footer-${unit.uid}`);
        footer.html(`
            <div class="card-footer bg-transparent border-top-light-custom text-center">
                ${getAvaliable(unit)}    
            </div>
        `);
        if (jsonData.permissions.add_to_cart) {
            footer.find('.card-footer').append(`
                <form action="${jsonData.urls.add_to_cart}" method="GET"> 
                    <input type="hidden" name="id" value="${unit.uid}">
                    <button type="submit" class="btn btn-primary btn-sm m-1 mt-3 w-75">
                        <i class="fa fa-cart-plus" aria-hidden="true"></i>
                        <span class="d-none d-sm-inline">Adicionar</span>
                    </button>
                </form>
            `);
        }
    }

    function getAvaliable(unit) {  
        if (unit.avaliable == 0 && unit.stock > 0) {
            return '<p class="opacity-75 m-0">Indisponível</p>';
        } else if (unit.stock > 0) {
            return `<p class="opacity-75 m-0">${unit.avaliable} disponíveis</p>`;
        }
        return '<p class="opacity-75 m-0 text-danger">Esgotado</p>';
    }

    function getTotalUnits(is_reload, currentItensCount, response) {
        if (is_reload) {
            return response.added_units
        }
        return currentItensCount + response.added_units
    }

    function renderNoMoreAlert(currentItensCount, totalUnits, loadMoreBtn) {
        if (currentItensCount == totalUnits) {
            alert.removeClass('d-none');
        } else {
            loadMoreBtn.removeClass('d-none');
        }
    }

    loadMoreBtn.click(() => loadMore(false));
    $('#filter-form').click(() => loadMore(true));
    $('#select-category').change(() => loadMore(true));

    
    const backToTopBtn = $('#back-to-top');
    $(window).scroll(() => {
        if ($(this).scrollTop() > 100) {
            backToTopBtn.removeClass('d-none');
            backToTopBtn.fadeIn();
        } else {
            backToTopBtn.fadeOut();
        }
    });

    backToTopBtn.click(() => {
        $('html, body').animate({scrollTop : 0}, 100);
        return false;
    });
});