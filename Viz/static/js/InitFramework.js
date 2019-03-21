$(document).ready(function () {
    $('.sidenav').sidenav();
    $('.modal').modal();
    $('.pushpin').pushpin();

});

function pushPinInit() {
    // $('.pushpin').pushpin({
    //     offset: $(this).height() - $(".pushpin").height()
    // });
    // $("main").css("padding-bottom", $(".pushpin").height());
}

$(window).resize(function () {
    pushPinInit()
})