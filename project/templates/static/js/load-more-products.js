$(this).ready(() => {
    const loadMoreBtn = $('#load-more-btn');
    const spinner = $('#spinner');
    const jsonData = JSON.parse($('#json-data').text());
    const alert = $('#no-more-alert');
    
    function loadMore() {
        const currentItensCount = $('.single-content').length;
        const contentContainer = $("#content");

        $.ajax({
            url: jsonData.load_more_url,
            type: 'GET',
            data: {
                'offset': currentItensCount
            },
            beforeSend: () => {
                loadMoreBtn.addClass('d-none');
                spinner.removeClass('d-none');
            },
            success: response => {
                spinner.addClass('d-none');
                
                response.map(unit => {
                    renderCard(contentContainer, unit);
                    renderPromotional(unit);
                    renderCardFooter(unit, jsonData);
                });

                renderNoMoreAlert(currentItensCount, jsonData, loadMoreBtn);
            }
        });
    }

    function renderCard(contentContainer, unit) {
        const card = `
            <div class="single-content col-6 col-sm-4 col-lg-3 mb-4">
                <div class="card shadow-sm">
                    <a href="${unit.category_slug}/${unit.product_slug}?uid=${unit.uid}">        
                        <img class="card-img-top d-block w-100" src="${unit.image}" alt="${unit.name}">  
                    </a>           
                    <div class="card-body d-flex flex-column">
                        <strong>
                            <h5 class="card-title fs-6">${unit.name}</h5>
                        </strong>
                        
                        <div class="product-price-block text-center">
                            <span class="product-price text-success">
                                R$ ${unit.price.replace('.', ',')}
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
                        R$ ${unit.promotional.replace('.', ',')}
                    </del>
                </small>
            `);
        }
    }
    
    function renderCardFooter(unit, jsonData) {
        const footer = $(`#card-footer-${unit.uid}`);

        if (!jsonData.add_to_cart_permission) {
            footer.remove();
        } else {
            footer.html(`
                <div class="card-footer bg-transparent border-top-light-custom text-center">
                    <form action="${jsonData.add_to_cart_url}" method="GET"> 
                        <input type="hidden" name="id" value="${unit.uid}">
                        <button type="submit" class="btn btn-primary btn-sm m-1 mt-3 w-75">
                            <i class="fa fa-cart-plus" aria-hidden="true"></i>
                            <span class="d-none d-sm-inline">Adicionar</span>
                        </button>
                    </form>
                </div>
            `);
        }
    }

    function renderNoMoreAlert(currentItensCount, jsonData, loadMoreBtn) {
        if (currentItensCount == jsonData.total_units) {
            alert.removeClass('d-none');
        } else {
            loadMoreBtn.removeClass('d-none');
        }
    }

    loadMoreBtn.click(loadMore);
});