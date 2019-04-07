function getCookie(name) {
    let value = "; " + document.cookie;
    let parts = value.split("; " + name + "=");
    if (parts.length === 2) return parts.pop().split(";").shift();
}

$(function () {
    $('#quizForm').on('submit', function (e) {
        let res = [];
        for (let i = 0; i < quiz.questions.length; i++) {
            let ans = [];
            let groups = quiz.questions[i].id.toString();
            let query = `input[name=${groups}]:checked`;
            $.each($(query), function () {
                let s = $(this).val().toString();
                ans.push(s);
            });
            res.push({"qId": quiz.questions[i].id, "ans": ans})
        }
        $.ajax({
            url: "/api/tutorial/",
            type: "put", //send it through get method
            data: JSON.stringify({"quizId": quiz.id, "result": res}),
            success: function (response) {
                console.log(response)
                //TODO: make and go to summary page
            },
            error: function (xhr) {
                alert("Could not save scores " + xhr.statusText)
            }
        });
        e.preventDefault();
    });
});

function arraysEqual(a, b) {
    if (a === b) return true;
    if (a == null || b == null) return false;
    if (a.length !== b.length) return false;

    a.sort();
    b.sort();

    for (let i = 0; i < a.length; ++i) {
        if (a[i].toString() !== b[i].toString()) return false;
    }
    return true;
}

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
    beforeSend: function (xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
        }
    }
});

$(document).ready(function () {
    let NODE_COLOUR = "#64b5f6";
    let NODE_SHAPE = "circle";

    let EDGE_COLOUR = "#2196f3";
    let EDGE_TYPE = "arrow";

    // create a network
    let container = document.getElementById('network');
    // http://visjs.org/docs/network/#options
    let options = {
        physics: {
            enabled: true
        },
        height: '100%',
        width: '100%',
        nodes: {
            shape: NODE_SHAPE,
            color: NODE_COLOUR

        },
        edges: {
            arrows: {
                to: {enabled: true, scaleFactor: 1, type: EDGE_TYPE},
                middle: {enabled: false, scaleFactor: 1, type: EDGE_TYPE},
                from: {enabled: false, scaleFactor: 1, type: EDGE_TYPE}
            },
            color: {
                color: EDGE_COLOUR,
                inherit: false,
                opacity: 0.8
            }
        },
        interaction: {hover: true, dragView: false, zoomView: false},
        manipulation: {
            enabled: false,
        }
    };

    network = new vis.Network(container, data, options);


    for (let i = 0; i < algo["lines"].length; i++) {
        $("#generatedCode").append("<code id=codeline-" + i + ">" + i + algo["lines"][i]["line"] + "</code>")
    }

    let minHeight = 750;
    let codeGen = $(".codeGen");
    if (codeGen.height() > minHeight) {
        minHeight = codeGen.height()
    }
    $(".minHeight").css("height", minHeight);
    $(".network").css("height", minHeight);
});
