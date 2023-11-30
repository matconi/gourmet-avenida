$(this).ready(() => {     
    const productSelect = document.querySelector('.product-select'); 
    const jsonData = JSON.parse($('#json-data').text());
    
    function loadOptions(data) {
        if (data.options) { 
            data.options.variants.map((variant, i) => {
                let variantLabels = $('.label').text();
                
                if (!variantLabels.includes(variant.name)) {                    
                    const selectBox = setSelectBox(variant, i);
                    
                    variant.variations.map((variation) => {
                        setOptionsInSelect(variation, selectBox);
                    });
                    
                }
            });
        }
    }

    function setSelectBox(variant, i) {
        productSelect.insertAdjacentHTML('beforebegin', `
            <label class="label" for="select-variacoes-${i}">
                <h4>${variant.name}</h4>
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

    fetch(jsonData.view_product_url)
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
        $('#qty').change(() => chooseUnit());

        function getIndexedUnit(indexedUnit) {
            if (indexedUnit !== undefined) {
                const unit = units.find(unit => unit.id === parseInt(indexedUnit))

                renderUnitData(unit);
                changeUnitVariant(unit.variations);
            } else {
                renderUnitData(units[0]);
                changeUnitVariant(units[0].variations);
            }
        }

        function renderUnitData(unit) {
            const name = $('#unit-name');
            const price = $('#unit-price');
            const unitId = $('#unit-id');

            const addInfo = $('#add-info');
            addInfo.text(`${$('#qty').val()} ${unit.name}`);

            name.text(unit.name);
            price.text(`R$ ${unit.price.replace('.', ',')}`);
            unitId.val(unit.id);
    
            renderPromotional(unit);
            renderAvaliable(unit);
            setActiveImage(unit);
        }

        function renderPromotional(unit) {
            const promotional = $('#unit-promotional');

            if (unit.promotional === null) {
                $('.text-muted').remove();
            } else {
                promotional.html(`
                    <small class="pl-2 opacity-75 text-danger">
                        <del>
                            R$ ${unit.promotional.replace('.', ',')}
                        </del>
                    </small>
                `);
            }
        }

        function renderAvaliable(unit) {
            const avaliable = $('#avaliable');
            const booked = $('#booked');
            
            if (unit.stock > 0) {
                avaliable.removeClass("text-danger");
                avaliable.addClass("text-success");

                avaliable.text(`${unit.stock - unit.booked} disponíveis`);
                if (unit.stock == unit.booked) {
                    avaliable.removeClass("text-danger");
                    avaliable.removeClass("text-success");

                    avaliable.text("Indisponível");
                    booked.text(` (${unit.booked} reservado(s))`);
                }
                if (unit.booked > 0) {
                    booked.text(` (${unit.booked} reservado(s))`);
                }
            } else {
                avaliable.removeClass("text-success");
                avaliable.addClass("text-danger");

                avaliable.text("Esgotado");
            }
        }

        function setActiveImage(unit) {
            $('.image-item').removeClass('active');
            $(`#image-${unit.id}`).parent().addClass('active');
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

        function changeUnitVariant(valuesToSelect) {
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
    });

    const carousel = $("#images-carousel").carousel();
    $(".carousel-control-prev").click(() => carousel.carousel("prev"));
    $(".carousel-control-next").click(() => carousel.carousel("next"));
});