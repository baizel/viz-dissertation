$(document).ready(function () {
    $('.sidenav').sidenav();
    $('.modal').modal();
    $('.pushpin').pushpin();
    $('select').formSelect();
    $('.tabs').tabs();
    destroyTabs();
});

function destroyTabs() {
    if ($(window).width() >= 800) {
        M.Tabs.getInstance($("#algo-tabs")).destroy();
    }
}

function pushPinInit() {
    // $('.pushpin').pushpin({
    //     offset: $(this).height() - $(".pushpin").height()
    // });
    // $("main").css("padding-bottom", $(".pushpin").height());
}

$(window).resize(function () {
    pushPinInit();
    destroyTabs();
});