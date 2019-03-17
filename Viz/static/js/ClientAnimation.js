var NODE_COLOUR = "lightblue";
var NODE_SELECTED_COLOUR = "red";
var NODE_SHAPE = "circle";
var EDGE_COLOUR = "blue";
var EDGE_TYPE = "arrow";


var numberOfNodes = 1;
var numberOfEdges = 1;
var dataChanged = false;

var nodes = new vis.DataSet([
    {id: numberOfNodes, label: numberOfNodes.toString(), inc: numberOfNodes++}, // Dummy option 'inc' to increment numberOfNodes
    {id: numberOfNodes, label: numberOfNodes.toString(), inc: numberOfNodes++},
    {id: numberOfNodes, label: numberOfNodes.toString(), inc: numberOfNodes++},
    {id: numberOfNodes, label: numberOfNodes.toString(), inc: numberOfNodes++},
    {id: numberOfNodes, label: numberOfNodes.toString(), inc: numberOfNodes++}
]);

// create an array with edges
var edges = new vis.DataSet([
    {from: 1, to: 3, label: "5", distance: 5,},
    {from: 1, to: 2, label: "12", distance: 12,},
    {from: 2, to: 4, label: "25", distance: 25,},
    {from: 2, to: 5, label: "10", distance: 10,}
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
    interaction: {hover: true},
    manipulation: {
        enabled: true,
        addNode: function (nodeData, callback) {
            dataChanged = true;
            numberOfNodes++;
            nodeData.label = numberOfNodes.toString();
            nodeData.id = numberOfNodes;
            nodeData.shape = NODE_SHAPE;
            //TODO: error Checking
            callback(nodeData);
        },
        addEdge: function (edgeData, callback) {
            dataChanged = true;
            //TODO: fix modal
            $('.modal').modal({
                'onCloseEnd': function () {
                    edgeData.label = document.getElementById("dist").value;
                    edgeData.distance = parseInt(document.getElementById("dist").value);
                    callback(edgeData)
                }
            });
            $('.modal').modal('open');
        },
        editNode: function (nodeData, callback) {
            dataChanged = true;
            callback(nodeData)
        },
        editEdge: function (edgeData, callback) {
            dataChanged = true;
            callback(edgeData);
        },
        deleteNode: function (object, callback) {
            dataChanged = true;
            callback(object)
        },
        deleteEdge: function (object, callback) {
            dataChanged = true;
            callback(object)
        },

    }
};

// initialize your network!
var network = new vis.Network(container, data, options);
var currentLine = -1; // -1 to offset the first increment
var animationSpeed = 1000; //In ms
var listOfDataClasses = [];
var previousNodeId = null;
var selectedNode = null;

network.on("selectNode", function (data) {
    dataChanged = true;
    var previousNode = null;
    var update = [];
    if (previousNodeId != null) {
        previousNode = nodes.get(previousNodeId);
        previousNode.color = NODE_COLOUR;
        update.push(previousNode);
    }
    var sNode = nodes.get(data.nodes[0]);
    previousNodeId = sNode.id;
    sNode.color = NODE_SELECTED_COLOUR;
    selectedNode = sNode;
    update.push(sNode);
    nodes.update(update);
    updateAnimationControls();
});

function updateData(className, data) {
    listOfDataClasses.push(className);
    $("." + className).html(data);
}

var previousAnimatedNodes = [];
var previousAddedEdges = [];

function animate(updates, lineNumber) {
    edges.remove(previousAddedEdges);
    previousAddedEdges = updates.updates[lineNumber].edges;
    for (var n = 0; n < previousAnimatedNodes.length; n++) {
        previousAnimatedNodes[n].color = NODE_COLOUR
    }
    nodes.update(previousAnimatedNodes);
    previousAnimatedNodes = updates.updates[lineNumber].nodes;
    nodes.update(updates.updates[lineNumber].nodes);
    edges.update(updates.updates[lineNumber].edges);

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

function resetLines() {
    currentLine = 0;
    for (var i = 0; i < listOfDataClasses.length; i++) {
        var element = document.getElementsByClassName(listOfDataClasses[i]);
        for (var ele of element) {
            ele.classList.remove(listOfDataClasses[i]);
        }
    }
    $(".data").html("");
    $("code").css('background-color', 'white');
    listOfDataClasses = [];
}

var responseFrames = null;

function getUpdateFrames(callback) {
    if (responseFrames == null || dataChanged) {
        $.ajax({
            url: "/api/",
            type: "get", //send it through get method
            data: {
                "network": JSON.stringify(data), source: selectedNode.id
            },
            success: function (response) {
                responseFrames = JSON.parse(response.updates);
                callback(responseFrames);
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
    $("#animationSpeedLabel").text("Animation Speed = " + animationSpeed.toString() + "ms");
    playAnimation()
}

function updateAnimationControls() {
    if (selectedNode == null) {
        $("a.animation-controls").attr("disabled", true);
        $("#animation-msg").attr("hidden", false);
    } else {
        $("a.animation-controls").attr("disabled", false);
        $("#animation-msg").attr("hidden", true);

    }
}


////////////////////////////////////////////////////// Init ////////////////////////////////////////////////////
$(document).ready(function () {
    $("#pause-btn").hide();
    network.setOptions(options);

    for (i = 0; i < algo["lines"].length; i++) {
        $("#generatedCode").append("<code id=codeline-" + i + ">" + i + algo["lines"][i]["line"] + "</code>")
    }

    updateAnimationControls();
});