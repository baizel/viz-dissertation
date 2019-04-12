function toggleOverflow() {
    var chk = document.querySelector('.overflowCheck').checked;
    $("pre").css("overflow", chk ? 'auto' : '')
}

$(document).ready(function () {
    $(".perserveHeight").height($('.mobile-controls').height());
    $('.mobile-controls').pushpin({offset: window.innerHeight - $('.mobile-controls').height()});
    toggleOverflow();
});