$(document).ready(() => {
    const tooglePassword = $('.toogle-password');
    const passwordInput = $('.passwordinput');
    const passwordMessage = $('.password-message');

    function toogle() {
        if (passwordInput.attr('type') === 'password') {
            passwordInput.attr('type', 'text');
            passwordMessage.text('Ocultar senha');
        } else {
            passwordInput.attr('type', 'password');
            passwordMessage.text('Mostrar senha');
        }
    }
    tooglePassword.click(toogle);
});