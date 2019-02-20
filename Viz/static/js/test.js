var numberOfNodes = 5;
var nodes = new vis.DataSet([
    {id: 1, label: '1', shape: "circle", color: "red"},
    {id: 2, label: '2'},
    {id: 3, label: '3'},
    {id: 4, label: '4'},
    {id: 5, label: '5'}
]);

// create an array with edges
var edges = new vis.DataSet([
    {from: 1, to: 3, label: "5", color: {color: "blue"}},
    {from: 1, to: 2, label: "12", chosen: true},
    {from: 2, to: 4, label: "25", chosen: true},
    {from: 2, to: 5, label: "10", chosen: true}
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
        }
    },
    interaction: {hover: true},
    manipulation: {
        enabled: true,
        addNode: function (nodeData, callback) {
            numberOfNodes++;
            nodeData.label = numberOfNodes.toString();
            nodeData.shape = "circle";
            //TODO: error Checking
            callback(nodeData);
        },
        addEdge: function (edgeData, callback) {
            $('.modal').modal({
                'onCloseEnd': function () {
                    edgeData.label = document.getElementById("dist").value;
                    edgeData.id = document.getElementById("dist").value;
                    callback(edgeData)
                }
            });
            $('.modal').modal('open');
        }

    }
};

// initialize your network!
var network = new vis.Network(container, data, options);


$(document).ready(function () {
    network.setOptions(options);

// algo set in html
    for (i = 0; i < algo["lines"].length; i++) {
        $("#generatedCode").append("<code id=codeline-" + i + ">" + i + algo["lines"][i]["line"] + "</code>")
    }
    var i = 0;

    function codeLoop() {
        setTimeout(function () {
            line = updates.updates[i].mapping;
            if (i > 0) {
                prevLine = updates.updates[i - 1].mapping;
                $("#codeline-" + prevLine).css('background-color', 'white');
            }
            $("#codeline-" + line).css('background-color', '#FFFF00');
            $("#exp").text(updates.updates[i].explanation);
            i++;
            if (i < updates.updates.length) {
                codeLoop();
            }
        }, 2000)
    }

    codeLoop();
});