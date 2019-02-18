var nodes = new vis.DataSet([
    {id: 1, label: '1', shape: "circle", color: "red"},
    {id: 2, label: '2'},
    {id: 3, label: '3'},
    {id: 4, label: '4'},
    {id: 5, label: '5'}
]);

// create an array with edges
var edges = new vis.DataSet([
    {from: 1, to: 3, id: 1, label: "5", color: {color: "blue"}},
    {from: 1, to: 2, id: 2, label: "12", chosen: true},
    {from: 2, to: 4, id: 3, label: "25", chosen: true},
    {from: 2, to: 5, id: 4, label: "10", chosen: true}
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
    }
};

// initialize your network!
var network = new vis.Network(container, data, options);


$(document).ready(function () {
    network.setOptions(options);

// algo set in html
    for (i = 0; i < algo["lines"].length; i++) {
        $("#generatedCode").append("<code id=codeline-"+i+">"+ i + algo["lines"][i]["line"]+"</code>")
    }
});