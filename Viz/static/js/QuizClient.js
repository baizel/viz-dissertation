$(document).ready(function () {
    var NODE_COLOUR = "#64b5f6";
    var NODE_SHAPE = "circle";

    var EDGE_COLOUR = "#2196f3";
    var EDGE_TYPE = "arrow";

    // create a network
    var container = document.getElementById('network');
    // http://visjs.org/docs/network/#options
    var options = {
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


    for (i = 0; i < algo["lines"].length; i++) {
        $("#generatedCode").append("<code id=codeline-" + i + ">" + i + algo["lines"][i]["line"] + "</code>")
    }

    let minHeight = 750;
    if ($(".codeGen").height() > minHeight) {
        minHeight = $(".codeGen").height()
    }
    $(".minHeight").css("height", minHeight);
    $(".network").css("height", minHeight);
});

function onSubmit() {
    let score = 0;
    let maxScore = questions.length;
    for (let i = 0; i < questions.length; i++) {
        let ans = [];
        let groups = "group" + (i + 1).toString();
        let query = `input[name=${groups}]:checked`;
        $.each($(query), function () {
            let s = $(this).val().toString();
            ans.push(s);
        });
        if (arraysEqual(ans, questions[i].ans)) {
            score++;
        }
    }
    console.log((score / maxScore) * 100 + "%");
    alert("You got " + (score / maxScore) * 100 + "%");
    return false; //To stop page refresh
}

function arraysEqual(a, b) {
    if (a === b) return true;
    if (a == null || b == null) return false;
    if (a.length !== b.length) return false;

    a.sort();
    b.sort();

    for (var i = 0; i < a.length; ++i) {
        if (a[i].toString() !== b[i].toString()) return false;
    }
    return true;
}