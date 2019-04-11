$(document).ready(function () {
    $('.sidenav').sidenav();
    $('.modal').modal();
    $('.pushpin').pushpin();
    $('select').formSelect();
    $('.tabs').tabs();
    destroyTabs();
    pushPinInit();
});

function destroyTabs() {
    if ($(window).width() >= 800) {
        M.Tabs.getInstance($("#algo-tabs")).destroy();
    }
}

function pushPinInit() {
    let obj = $('.tabpushpin');
    if (obj.length) {
        obj.pushpin({top: obj.offset().top});
    }
}

$(window).resize(function () {
    pushPinInit();
    destroyTabs();
});