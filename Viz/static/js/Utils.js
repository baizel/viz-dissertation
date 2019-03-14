function toggleOverflow() {
    var chk = document.querySelector('.overflowCheck').checked;
    $("pre").css("overflow", chk ? 'auto' : '')
}

$(document).ready(function () {
    toggleOverflow();
});