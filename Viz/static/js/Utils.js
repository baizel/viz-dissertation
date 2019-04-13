function toggleOverflow() {
    var chk = document.querySelector('.overflowCheck').checked;
    $("pre").css("overflow", chk ? 'auto' : '')
}

function mobileControls() {
    $(".perserveHeight").height($('.mobile-controls').height());
    $('.mobile-controls').pushpin({offset: window.innerHeight - 63});
}

$(document).ready(function () {
    window.onresize = mobileControls;
    mobileControls();
    toggleOverflow();
});