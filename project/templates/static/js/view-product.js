$(this).ready(() => {     
    const productSelect = document.querySelector('.product-select'); 
    const jsonData = JSON.parse($('#json-data').text());
    
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

    function chooseUnit() {
        const selectedOptions = getSelectedOptions();
        
        for (unit of units) {        
            if (unit.variations.sort().toString() === selectedOptions.toString()) {
                renderUnitData(unit);
                break;
            }
        }
    }

    fetch(jsonData.view_product_url)
    .then(response => response.json())
    .then(data => {
        console.log(data);
        data.summary.variants.map((variant, i) => {
            let variantLabels = $('.label').text();
            
            if (!variantLabels.includes(variant.name)) {                    
                const selectBox = setSelectBox(variant, i);
                
                variant.variations.map((variation) => {
                    setOptionsInSelect(variation, selectBox);
                });
                
            }
        });

        const units = [];
        const images = document.querySelector('.carousel-inner');
        data.units.map((unit, i) => {              
            units.push(unit); 
            renderImages(images, unit);
        });
        removeImageArrows(units);
        getIndexedUnit(location.href.split('=')[1]); // WARN: spliting single URL param


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
    
        function changeUnitVariant(valuesToSelect) {
            const selectBoxes = document.querySelectorAll('.select-variacoes');
            const ids = document.querySelectorAll('.ids');

            selectBoxes.forEach((selectBox, i) => {
                optionInSelect = Array.from(ids)
                                        .find(option => option.value == valuesToSelect[i]);

                optionInSelect.setAttribute("selected", "");
            }); 
        }

        function renderUnitData(unit) {
            const name = $('#unit-name');
            const price = $('#unit-price');
            const promotional = $('#unit-promotional');
            const unit_id = $('#unit-id');

            name.html(unit.name);
            price.html(`R$ ${unit.price}`);
            unit_id.val(unit.id);
    
            if (unit.promotional === null) {
                $('.text-muted').remove();
            } else {
                promotional.html(`
                    <small class="pl-2 text-muted">
                        <del>
                            R$ ${unit.promotional}
                        </del>
                    </small>
                `);
            }
        }

        function renderImages(carousel, unit) {
            carousel.insertAdjacentHTML('beforeend', `
                <div class="carousel-item">
                    <img src="${unit.image}" class="d-block w-100" alt="${unit.name}">
                </div>
            `);
        }

        function removeImageArrows(units) {
            if (units.length < 2) {
                $('.carousel-control-prev').remove();
                $('.carousel-control-next').remove();
            }
        }
    });

    const carousel = $("#images-carousel").carousel();
    $(".carousel-control-prev").click(() => carousel.carousel("prev"));
    $(".carousel-control-next").click(() => carousel.carousel("next"));

    $('.select-variacoes').change(() => chooseUnit());
});