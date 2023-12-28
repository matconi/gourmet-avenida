$(document).ready(() => {
    // masks needs <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery.mask/1.14.16/jquery.mask.min.js" integrity="sha512-pHVGpX7F/27yZ0ISY+VVjyULApbDlD0/X0rgGbTqCE7WFW5MezNTWG/dnhtbBuICzsd0WQPgpE4REBLv+UqChw==" crossorigin="anonymous" referrerpolicy="no-referrer"></script>
    $('.cel-input').mask('(00) 00000-0000');
    $('.date-input').mask('00/00/0000');
    $('.datetime > input').on('focus', (event) => {
        if ( $(event.currentTarget)[0].classList[0] === "vDateField") {
            $(event.currentTarget).mask('00/00/0000');
        } else {
            $(event.currentTarget).mask('00:00:00');
        }
    });
});