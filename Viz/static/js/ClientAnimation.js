var NODE_COLOUR = "#64b5f6";
var NODE_SELECTED_COLOUR = "#f44336";
var NODE_SHAPE = "circle";

var EDGE_COLOUR = "#2196f3";
var EDGE_TYPE = "arrow";


var numberOfNodes = 1;
var dataChanged = false;

var nodes = new vis.DataSet([
    {id: numberOfNodes, label: numberOfNodes.toString(), inc: numberOfNodes++}, // Dummy option 'inc' to increment numberOfNodes
    {id: numberOfNodes, label: numberOfNodes.toString(), inc: numberOfNodes++},
    {id: numberOfNodes, label: numberOfNodes.toString(), inc: numberOfNodes++},
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
    {from: 2, to: 5, label: "10", distance: 10,},
    {from: 5, to: 6, label: "11", distance: 11,},
    {from: 6, to: 7, label: "12", distance: 12,}
]);
var network = null;
var isShowingToast = false;

function toast(msg) {
    if (!isShowingToast) {
        isShowingToast = true;
        M.toast({
            html: msg, completeCallback: function () {
                isShowingToast = false;
            }
        });
    }

}

function initGraph(dataset) {
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
            enabled: true,
            addNode: function (nodeData, callback) {
                dataChanged = true;
                resetLines();
                numberOfNodes++;
                nodeData.label = numberOfNodes.toString();
                nodeData.id = numberOfNodes;
                nodeData.shape = NODE_SHAPE;
                //TODO: error Checking
                callback(nodeData);
            },
            addEdge: function (edgeData, callback) {
                dataChanged = true;
                resetLines();
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
                resetLines();
                callback(nodeData)
            },
            editEdge: function (edgeData, callback) {
                dataChanged = true;
                resetLines();
                callback(edgeData);
            },
            deleteNode: function (object, callback) {
                previousNodeId = null;
                selectedNode = null;
                dataChanged = true;
                resetLines();
                callback(object)
            },
            deleteEdge: function (object, callback) {
                dataChanged = true;
                resetLines();
                callback(object)
            },
        }
    };

    network = new vis.Network(container, dataset, options);
    network.on("selectNode", function (data) {
        if (isSourceNeeded) {
            edges.remove(previousAddedEdges);
            previousAddedEdges = [];
            dataChanged = true;
            let previousNode = null;
            let update = [];
            if (previousNodeId != null) {
                previousNode = nodes.get(previousNodeId);
                if (previousNode != null) {
                    previousNode.color = NODE_COLOUR;
                    update.push(previousNode);
                }
            }
            let sNode = nodes.get(data.nodes[0]);
            previousNodeId = sNode.id;
            sNode.color = NODE_SELECTED_COLOUR;
            selectedNode = sNode;
            update.push(sNode);
            nodes.update(update);
            updateAnimationControls();
        }
    });
    network.setOptions(options);

}

var data = null;
var currentLine = -1; // -1 to offset the first increment
var animationSpeed = 1000; //In ms
var listOfDataClasses = [];
var previousNodeId = null;
var selectedNode = null;
var previousAnimatedNodes = [];
var previousAddedEdges = [];
var previousColoredEdges = [];


function updateData(className, data) {
    listOfDataClasses.push(className);
    $("." + className).html(data);
}

function animate(updates, lineNumber) {
    network.unselectAll(); // To show edge colors instead of highlighted colors

    if (selectedNode !== null && nodes.get(selectedNode.id).color === NODE_COLOUR) {
        nodes.update({id: selectedNode.id, color: NODE_SELECTED_COLOUR});
    } else if (selectedNode === null && isSourceNeeded) {
        toast("Select A Node First");
        return
    }
    edges.remove(previousAddedEdges);
    previousAddedEdges = $.extend(true, [], updates[lineNumber].edges);

    edges.update(updates[lineNumber].edges);
    edges.update(previousColoredEdges);
    previousColoredEdges = [];
    for (let i of previousAddedEdges.slice()) {
        if (i.hasOwnProperty("isNew") && !i.isNew) {
            previousAddedEdges.pop(i);
            i.color.color = EDGE_COLOUR;
            previousColoredEdges.push(i);
        }
    }
    if (updates[lineNumber].nodes.length !== 0) {

        for (let n = 0; n < previousAnimatedNodes.length; n++) {
            previousAnimatedNodes[n].color = NODE_COLOUR
        }
        nodes.update(previousAnimatedNodes);
        previousAnimatedNodes = $.extend(true, [], updates[lineNumber].nodes);
        nodes.update(updates[lineNumber].nodes);
    }

    line = updates[lineNumber].mapping;
    if (lineNumber > 0) {
        prevLine = updates[lineNumber - 1].mapping;
        $("#codeline-" + prevLine).css('background-color', '');
    }
    if (lineNumber < updates.length - 1) {
        nextLine = updates[lineNumber + 1].mapping;
        $("#codeline-" + nextLine).css('background-color', '');
    }

    codeLine = $("#codeline-" + line);
    codeLine.css('background-color', '#FFFF00');

    $("#exp").html(updates[lineNumber].explanation);

    //update Data
    if (updates[lineNumber].data != null) {
        updateDataFromEvent = updates[lineNumber].data;
        spanTag = codeLine.children("span");
        if (updateDataFromEvent.updateData.length > 0) {
            for (let d of updateDataFromEvent.updateData) {
                updateData(d.classID, d.rawData);
                updateData(d.classID + "table", d.rawData); //update table data if it exists
                if (d.isShownOnScreen) {
                    spanTag.addClass(d.classID);
                    let inlineExp = d.inlineExp != null ? d.inlineExp + ":" + d.rawData : d.rawData;
                    updateData(d.classID, inlineExp);
                }
            }
        }
        if (updateDataFromEvent.tableData.length > 0) {
            for (let tableData of updateDataFromEvent.tableData) {
                addToTable(tableData.classID + "table", tableData.rawData, tableData.tableExp);
                updateData(tableData.classID + "table", tableData.rawData)
            }
        }
    }
}

var animationInterval = null;

function playAnimation(algo) {
    if (selectedNode !== null || !isSourceNeeded) {
        $(".play-btn").hide();
        $(".pause-btn").show();
        animationInterval = setInterval(function () {
            nextFrame(algo)
        }, animationSpeed);
    } else {
        toast("Select A Node First");
    }
}

function nextFrame(algo) {
    getUpdateFrames(function (updates) {
        if (currentLine > updates.length - 2) {
            pauseAnimation();
        } else {
            currentLine++;
            animate(updates, currentLine);
        }
    }, algo);
}

function previousFrame(algo) {
    getUpdateFrames(function (updates) {
        currentLine--;
        if (currentLine < 0) {
            currentLine = 0;
        }
        animate(updates, currentLine);
    }, algo);
}

function pauseAnimation() {
    $(".play-btn").show();
    $(".pause-btn").hide();
    clearInterval(animationInterval)
}

function resetLines() {
    edges.remove(previousAddedEdges);
    previousAddedEdges = [];
    previousAnimatedNodes = [];
    var n = [];
    Object.keys(nodes._data).forEach(function (key) {
        let v = $.extend(true, {}, nodes._data[key]);
        v.color = NODE_COLOUR;
        n.push(v);
    });
    nodes.update(n);
    currentLine = 0;
    for (let i = 0; i < listOfDataClasses.length; i++) {
        let element = document.getElementsByClassName(listOfDataClasses[i]);
        for (let ele of element) {
            ele.classList.remove(listOfDataClasses[i]);
        }
    }
    $(".data").html("");
    $("code").css('background-color', '');
    listOfDataClasses = [];
    $('table tr.tableValueRow').remove();
}

var responseFrames = null;

function getUpdateFrames(callback, algo) {
    let nodeid = "";
    if (selectedNode !== null) {
        nodeid = selectedNode.id
    } else if (isSourceNeeded) {
        toast("Select A Node First");
        return
    }
    if (responseFrames == null || dataChanged) {
        $.ajax({
            url: "/api/animation/" + algo + "/" + nodeid,
            type: "get", //send it through get method
            data: {
                "network": JSON.stringify(data)
            },
            success: function (response) {
                responseFrames = response.updates;
                callback(responseFrames);
                dataChanged = false;
            },
            error: function (xhr) {
                toast("Could not get animation updates");
            }
        });
    } else {
        callback(responseFrames)
    }
}

function updateAnimationTime(val, algo) {
    pauseAnimation();
    animationSpeed = val;
    $("#animationSpeedLabel").text(animationSpeed.toString() + "ms");
    playAnimation(algo);
}

function updateAnimationControls() {
    // if (selectedNode == null && isSourceNeeded) {
    //     $("a.animation-controls").attr("disabled", true);
    //     document.getElementById("animationSpeed").disabled = true;
    //     $("#animation-msg").attr("hidden", false);
    // } else {
    //     $("a.animation-controls").attr("disabled", false);
    //     document.getElementById("animationSpeed").disabled = false;
    //     $("#animation-msg").attr("hidden", true);
    //
    // }
}

function addToTable(dataClass, value, displayName) {
    if (!$("." + dataClass).length) {
        $('#tableValues').append('<tr class ="tableValueRow"><td>' + displayName + '</td> <td><span class="data ' + dataClass + '" >' + value + '</span></td> </tr>');
    }
}

function graphApiCall(url) {
    $.ajax({
        url: url,
        type: "get", //send it through get method
        data: {
            "isNegativeEdges": isNegativeEdges
        },
        success: function (response) {
            data = {
                nodes: new vis.DataSet(response.nodes),
                edges: new vis.DataSet(response.edges)
            };
            nodes = data.nodes;
            edges = data.edges;
            initGraph(data);
        },
        error: function (xhr) {
            toast("Could not get Graph, please refresh");
            data = {
                nodes: nodes,
                edges: edges
            };
            initGraph(data);
        }
    });
}

////////////////////////////////////////////////////// Init ////////////////////////////////////////////////////
$(document).ready(function () {
    const urlParams = new URLSearchParams(window.location.search);
    const gId = urlParams.get('graphId');
    if (gId === null)
        graphApiCall("/api/graph/random");
    else
        graphApiCall("/api/graph/"+gId);
    $(".pause-btn").hide();

    for (i = 0; i < algo["lines"].length; i++) {
        $("#generatedCode").append("<code id=codeline-" + i + ">" + i + algo["lines"][i]["line"] + "</code>")
    }

    updateAnimationControls();
    let minHeight = 770;
    if ($(".codeGen").height() > minHeight) {
        minHeight = $(".codeGen").height()
    }
    $(".minHeight").css("height", minHeight);
    $(".network").css("height", minHeight);

});
