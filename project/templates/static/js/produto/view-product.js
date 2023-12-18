$(this).ready(() => {     
    const productSelect = document.querySelector('.product-select'); 
    const jsonData = JSON.parse($('#json-data').text());
    
    function loadOptions(data) {
        if (data.options) { 
            data.options.varieties.map((variety, i) => {
                let varietyLabels = $('.label').text();
                
                if (!varietyLabels.includes(variety.name)) {                    
                    const selectBox = setSelectBox(variety, i);
                    
                    variety.variations.map((variation) => {
                        setOptionsInSelect(variation, selectBox);
                    });
                    
                }
            });
        }
    }

    function setSelectBox(variety, i) {
        productSelect.insertAdjacentHTML('beforebegin', `
            <label class="label" for="select-variacoes-${i}">
                <h4>${variety.name}</h4>
            </label>
            <select id="select-variacoes-${i}" class="form-control form-control-lg mb-5 select-variacoes"></select>
        `);  
        return document.querySelector(`#select-variacoes-${i}`);
    }

    function setOptionsInSelect(variation, selectBox) {             
        selectBox.insertAdjacentHTML('beforeend', `
            <option class="ids" value="${variation.id}">
                ${variation.name}
            </option> 
        `);
    }

    function getSelectedOptions() {
        let selectedOptions = [];

        for (selectBox of $('.select-variacoes')) {
            selectedOptions.push(selectBox.options[selectBox.selectedIndex].value);
        }
        return selectedOptions.sort();
    }

    fetch(jsonData.urls.view_product)
    .then(response => response.json())
    .then(data => {
        loadOptions(data);

        const units = [];
        const images = document.querySelector('.carousel-inner');
        data.units.map(unit => {              
            units.push(unit);
            renderImages(images, unit);
        });

        removeImageArrows(units);
        getIndexedUnit(location.href.split('=')[1]); // WARN: spliting single URL param
        $('.select-variacoes').change(() => chooseUnit());
        $('#qty').change(() => changeQuantity());

        function getIndexedUnit(indexedUnit) {
            if (indexedUnit !== undefined) {
                const unit = units.find(unit => unit.id === parseInt(indexedUnit))
                
                removeAddToCartForm();
                renderUnitData(unit);
                changeUnitvariety(unit.variations);
            } else {
                removeAddToCartForm();
                renderUnitData(units[0]);
                changeUnitvariety(units[0].variations);
            }
        }

        function removeAddToCartForm() {
            if (!jsonData.permissions.add_to_cart) {
                $('#add-to-cart-submit').remove();
            }
        }

        function changeUnitName(unit) {
            $('#add-info').text(unit.name);
        }

        function renderUnitData(unit) {
            changeQuantity();
            changeUnitName(unit);

            const name = $('#unit-name');
            const price = $('#unit-price');
            const unitId = $('.unit-id');
            
            name.text(unit.name);
            price.text(priceFormat(unit.price));
            unitId.val(unit.id);
    
            setActiveImage(unit);
            renderPromotional(unit);
            renderAvaliable(unit);
            renderFavoriteForm(unit);
        }

        function setActiveImage(unit) {
            $('.image-item').removeClass('active');
            $(`#image-${unit.id}`).parent().addClass('active');
        }

        function renderPromotional(unit) {
            const promotional = $('#unit-promotional');

            if (unit.promotional === null) {
                $('.text-muted').remove();
            } else {
                promotional.html(`
                    <small class="pl-2 opacity-75 text-danger">
                        <del>
                            ${priceFormat(unit.promotional)}
                        </del>
                    </small>
                `);
            }
        }

        function renderAvaliable(unit) {
            const avaliable = $('#avaliable');
            const booked = $('#booked');
            
            if (unit.stock > 0) {
                avaliable.removeClass("text-danger").addClass("text-success");
                avaliable.text(`${unit.stock - unit.booked} disponíveis`);

                if (unit.booked > 0) {
                    booked.text(` (${unit.booked} reservado(s))`);
                }

                if (unit.stock == unit.booked) {
                    avaliable.removeClass("text-danger text-success");
                    avaliable.text("Indisponível");
                }              
            } else {
                avaliable.removeClass("text-success").addClass("text-danger");
                avaliable.text("Esgotado");
            }
        }

        function renderFavoriteForm(unit) {
            unit.is_favorite ? removeFavoriteForm() : addFavoriteForm();
        }

        function renderImages(carousel, unit) {
            carousel.insertAdjacentHTML('beforeend', `
                <div class="carousel-item image-item">
                    <img src="${unit.image_lg}" class="d-block w-100" id="image-${unit.id}" alt="${unit.name}">
                </div>
            `);
        }

        function removeImageArrows(units) {
            if (units.length < 2) {
                $('.carousel-control-prev').remove();
                $('.carousel-control-next').remove();
            }
        }

        function changeUnitvariety(valuesToSelect) {
            const selectBoxes = document.querySelectorAll('.select-variacoes');
            const ids = document.querySelectorAll('.ids');

            selectBoxes.forEach((selectBox, i) => {
                optionInSelect = Array.from(ids)
                                        .find(option => option.value == valuesToSelect[i]);
                optionInSelect.setAttribute("selected", "");
            }); 
        }

        function chooseUnit() {
            const selectedOptions = getSelectedOptions();

            for (unit of units) {        
                if (unit.variations.sort().toString() === selectedOptions.toString()) {
                    renderUnitData(unit);
                    break;
                }
            }
        }

        function changeQuantity() {
            $('#add-info-qty').text($('#qty').val());
        }       
    }).catch(err => {
            productSelect.innerHTML = '<p class="text-danger">Erro ao carregar o produto!</p>';
            console.error(err);
        }
    );

    const carousel = $("#images-carousel").carousel();
    $(".carousel-control-prev").click(() => carousel.carousel("prev"));
    $(".carousel-control-next").click(() => carousel.carousel("next"));
});