var numberOfNodes = 1;
var numberOfEdges = 1;

var nodes = new vis.DataSet([
    {id: numberOfNodes, label: numberOfNodes.toString(), inc: numberOfNodes++, color:"red"}, // Dummy option to increment numberOfNodes
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
        color:{
            color: "blue",
            inherit:false,
            opacity:0.8
        }
    },
    interaction: {hover: true},
    manipulation: {
        enabled: true,
        addNode: function (nodeData, callback) {
            numberOfNodes++;
            nodeData.label = numberOfNodes.toString();
            nodeData.id = numberOfNodes;
            nodeData.shape = "circle";
            //TODO: error Checking
            callback(nodeData);
        },
        addEdge: function (edgeData, callback) {
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

var i = 0;

function updateData(className, data) {
    $("." + className).html(data);
}

function codeLoop(updates) {
    setTimeout(function () {
        console.log(updates.updates[i]);
        line = updates.updates[i].mapping;
        if (i > 0) {
            prevLine = updates.updates[i - 1].mapping;
            $("#codeline-" + prevLine).css('background-color', 'white');
        }
        codeLine = $("#codeline-" + line);
        codeLine.css('background-color', '#FFFF00');
        $("#exp").text(updates.updates[i].explanation);
        if (updates.updates[i].data != null) {
            updateDataFromEvent = updates.updates[i].data;
            spanTag = codeLine.children("span");
            spanTag.addClass(updateDataFromEvent.lineData[0]);
            updateData(updateDataFromEvent.lineData[0], updateDataFromEvent.lineData[1])
        }
        i++;
        if (i < updates.updates.length) {
            codeLoop(updates);
        }
    }, 2000)
}

$(document).ready(function () {
    network.setOptions(options);

// algo set in html
    for (i = 0; i < algo["lines"].length; i++) {
        $("#generatedCode").append("<code id=codeline-" + i + ">" + i + algo["lines"][i]["line"] + "</code>")
    }
    var i = 0;

});

function reset() {
    i = 0;
    $(".data").html("");
    $("code").css('background-color', 'white');
}

function animateAlgo() {
    reset();
    $.ajax({
        url: "/api/",
        type: "get", //send it through get method
        data: {
            "network": JSON.stringify(data), source: 1
        },
        success: function (response) {
            codeLoop(response.updates);
        },
        error: function (xhr) {
            //Do Something to handle error
        }
    });
}