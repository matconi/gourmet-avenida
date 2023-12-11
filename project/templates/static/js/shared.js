function loadMessages(messages) {
    $('#toast-container').empty();

    for (let type in messages) {
        const toastConf = getConfType(type);
        
        let messageList = messages[type];
        showToast(toastConf, messageList);
    }  
}

function getConfType(type) {
    switch (type) {
        case 'success':
            return {
                "name": 'success',
                "headerText": 'Sucesso!',
                "delay": 2500
            }
        case 'warning':
            return {
                "name": 'warning',
                "headerText": 'Aviso!',
                "delay": 5000
            }   
        case 'danger':
            return {
                "name": 'danger',
                "headerText": 'Erro!',
                "delay": 7000
            }             
        default:
            return {
                "name": 'info',
                "headerText": 'Informação',
                "delay": 5000
            }
    }
}

function showToast(confType, messageList) {
    for (let message of messageList) {
        $('#toast-container').append(`
            <div class="toast hider" role="alert" aria-live="assertive" aria-atomic="true" data-bs-delay="${confType.delay}">
                <div class="toast-header">
                    <strong class="my-auto alert bg-${confType.name} p-1 text-light" id="type-message">${confType.headerText}</strong>
                    <button type="button" class="btn-close ms-auto" data-bs-dismiss="toast" aria-label="Close"></button>
                </div>
                <p class="container fs-6 toast-body lead fs-5">${message}</p>
            </div>
        `);
        $('.toast').toast('show');
    }
}