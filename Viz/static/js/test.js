var numberOfNodes = 1;
var numberOfEdges = 1;
var dataChanged = false;

var nodes = new vis.DataSet([
    {id: numberOfNodes, label: numberOfNodes.toString(), inc: numberOfNodes++, color: "red"}, // Dummy option to increment numberOfNodes
    {id: numberOfNodes, label: numberOfNodes.toString(), inc: numberOfNodes++},
    {id: numberOfNodes, label: numberOfNodes.toString(), inc: numberOfNodes++},
    {id: numberOfNodes, label: numberOfNodes.toString(), inc: numberOfNodes++},
    {id: numberOfNodes, label: numberOfNodes.toString(), inc: numberOfNodes++}
]);

// create an array with edges
var edges = new vis.DataSet([
    {from: 1, to: 3, label: "5"},
    {from: 1, to: 2, label: "12",},
    {from: 2, to: 4, label: "25",},
    {from: 2, to: 5, label: "10",}
]);

// create a network
var container = document.getElementById('dijkstraNodes');

// provide the data in the vis format
var data = {
    nodes: nodes,
    edges: edges
};
// http://visjs.org/docs/network/#options
var options = {
    height: '100%',
    width: '100%',
    nodes: {
        shape: "circle"
    },
    edges: {
        arrows: {
            to: {enabled: true, scaleFactor: 1, type: 'arrow'},
            middle: {enabled: false, scaleFactor: 1, type: 'arrow'},
            from: {enabled: false, scaleFactor: 1, type: 'arrow'}
        },
        color: {
            color: "blue",
            inherit: false,
            opacity: 0.8
        }
    },
    interaction: {hover: true},
    manipulation: {
        enabled: true,
        addNode: function (nodeData, callback) {
            dataChanged = true;
            numberOfNodes++;
            nodeData.label = numberOfNodes.toString();
            nodeData.id = numberOfNodes;
            nodeData.shape = "circle";
            //TODO: error Checking
            callback(nodeData);
        },
        addEdge: function (edgeData, callback) {
            dataChanged = true;
            $('.modal').modal({
                'onCloseEnd': function () {
                    edgeData.label = document.getElementById("dist").value;
                    callback(edgeData)
                }
            });
            $('.modal').modal('open');
        }

    }
};

// initialize your network!
var network = new vis.Network(container, data, options);
var currentLine = -1; // -1 to offset the first increment
var animationSpeed = 1000; //In ms

function updateData(className, data) {
    $("." + className).html(data);
}

function animate(updates, lineNumber) {
    line = updates.updates[lineNumber].mapping;
    if (lineNumber > 0) {
        prevLine = updates.updates[lineNumber - 1].mapping;
        $("#codeline-" + prevLine).css('background-color', 'white');
    }
    if (lineNumber < updates.updates.length - 1) {
        nextLine = updates.updates[lineNumber + 1].mapping;
        $("#codeline-" + nextLine).css('background-color', 'white');
    }

    codeLine = $("#codeline-" + line);
    codeLine.css('background-color', '#FFFF00');
    $("#exp").text(updates.updates[lineNumber].explanation);
    if (updates.updates[lineNumber].data != null) {
        updateDataFromEvent = updates.updates[lineNumber].data;
        spanTag = codeLine.children("span");
        spanTag.addClass(updateDataFromEvent.lineData[0]);
        updateData(updateDataFromEvent.lineData[0], updateDataFromEvent.lineData[1])
    }
}

var animationInterval = null;

function playAnimation() {
    $("#play-btn").hide();
    $("#pause-btn").show();
    animationInterval = setInterval(nextFrame, animationSpeed);
}

function nextFrame() {
    getUpdateFrames(function (updates) {
        if (currentLine > updates.updates.length - 2) {
            pauseAnimation();
        } else {
            currentLine++;
            animate(updates, currentLine);
        }
    });
}

function previousFrame() {
    getUpdateFrames(function (updates) {
        currentLine--;
        if (currentLine < 0) {
            currentLine = 0;
        }
        animate(updates, currentLine)
    });
}

function pauseAnimation() {
    $("#play-btn").show();
    $("#pause-btn").hide();
    clearInterval(animationInterval)
}

function reset() {
    currentLine = 0;
    $(".data").html("");
    $("code").css('background-color', 'white');
}

var responseFrames = null;

function getUpdateFrames(callback) {
    if (responseFrames == null || dataChanged) {
        $.ajax({
            url: "/api/",
            type: "get", //send it through get method
            data: {
                "network": JSON.stringify(data), source: 1
            },
            success: function (response) {
                responseFrames = response.updates;
                callback(response.updates);
                dataChanged = false;
            },
            error: function (xhr) {
                //Do Something to handle error
            }
        });
    } else {
        callback(responseFrames)
    }
}

function updateAnimationTime(val) {
    pauseAnimation();
    animationSpeed = val;
    $("#animationSpeedLabel").text("Animation Speed = "+animationSpeed.toString()+"ms");
    playAnimation()
}

////////////////////////////////////////////////////// Init ////////////////////////////////////////////////////
$(document).ready(function () {
    $("#pause-btn").hide();
    network.setOptions(options);

    for (i = 0; i < algo["lines"].length; i++) {
        $("#generatedCode").append("<code id=codeline-" + i + ">" + i + algo["lines"][i]["line"] + "</code>")
    }
    var i = 0;

});