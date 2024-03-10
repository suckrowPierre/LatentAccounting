var editor = null;
var output_columns = null;

function getEditorState() {
    return editor.export();
}

function set_output_columns(columns) {
    output_columns = columns;
}

function load_editor_state(state = null) {
    editor = null;
    if (editor == null) {
        start_editor();
    } else {
        import_editor_state(state);
    }
    compareInputCSVToEditorNodesAndCreate();
}

function start_editor() {
    const id = document.getElementById("drawflow");
    editor = new Drawflow(id);


    editor.zoom_max = 1.6;
    editor.zoom_min = 0.5;
    editor.zoom_value = 0.1;
    editor.editor_mode = 'edit';
    editor.start();
    console.log("editor started");
}

function getNodesFromClass(nodeClass) {
    return Object.values(editor.drawflow.drawflow.Home.data).filter(entry => entry.class === nodeClass);
}

function findNodeByName(nodes, name) {
    return nodes.find(entry => entry.name === name);
}

function removeNodeByName(nodes, name) {
    return nodes.filter(entry => entry.name !== name);
}

function createNode(name, x, y, type, inputs, outputs) {
    const htmlNode = `
        <div class="text-sm">
            <p>${name}</p>
        </div>
        `;
    const data = { "name": name };
    editor.addNode(type + name, inputs, outputs, x, y, type, data, htmlNode);
}

function compareInputCSVToEditorNodesAndCreate() {
    const csv_separator = document.getElementById("csv-seperator").value;
    const csv_columns = document.getElementById("csv-columns").value.split(csv_separator);
    console.log(csv_columns);

    const inputNodes = getNodesFromClass('input');
    var copyInputNodes = inputNodes.slice();

    // create boolean array of same length as inputNodes
    let createdNodes = new Array(inputNodes.length).fill(false);
    for (let i = 0; i < csv_columns.length; i++) {
        // ceck if csv column is already in inputNodes
        console.log("checking for " + csv_columns[i]);
        if (inputNodes === [] || !findNodeByName(inputNodes, "input" + csv_columns[i]) ) {
            console.log("creating node");
            createNode(csv_columns[i], 0, i*40+20, 'input', 0, 1);
        } else if (inputNodes !== [] && findNodeByName(inputNodes, "input" + csv_columns[i])) {
            copyInputNodes = removeNodeByName(copyInputNodes, "input" + csv_columns[i]);
        }
    }

    for (let i = 0; i < copyInputNodes.length; i++) {
            editor.removeNodeId("node-" + copyInputNodes[i].id);
    }



}

function import_editor_state(state) {
    editor.import(state);

}

function load_flowchart() {
    const id = document.getElementById("drawflow");
    editor = new Drawflow(id);


    editor.zoom_max = 1.6;
    editor.zoom_min = 0.5;
    editor.zoom_value = 0.1;
    editor.editor_mode = 'edit';
    editor.start();




    //get csv columns and create nodes for each column
    const csv_separator = document.getElementById("csv-seperator").value;
    const csv_columns = document.getElementById("csv-columns").value.split(csv_separator);

    for (let i = 0; i < csv_columns.length; i++) {
        const htmlNode = `
        <div class="text-sm">
            <p>${csv_columns[i]}</p>
        </div>
        `;
        const data = { "name": csv_columns[i] };
        editor.addNode(`input_node_${csv_columns[i]}`, 0, 1, 50, i*40+20, 'input', data, htmlNode);
    }

    //create output nodes
    for ( let i = 0; i < output_columns.length; i++) {
        const htmlNode = `
        <div class="text-sm">
            <p>${output_columns[i]}</p>
        </div>
        `;
        const data = { "name": output_columns[i] };
        editor.addNode(`output_node_${output_columns[i]}`, 1, 0, 650, i*40+20, 'output', data, htmlNode);
    }

    setupDragAndDrop()

}

function setupDragAndDrop() {
    const draggableItems = document.querySelectorAll('li[draggable="true"]');
    const dropZone = document.getElementById('drawflow');

    draggableItems.forEach(item => {
        item.addEventListener('dragstart', handleDragStart);
    });

    dropZone.addEventListener('dragover', event => {
        event.preventDefault(); // Necessary to allow the drop
    });

    dropZone.addEventListener('drop', handleDrop);
}

function handleDragStart(event) {
    draggedElementType = event.target.textContent.trim();
}

function handleDrop(event) {
    event.preventDefault();
    const dropX = event.offsetX;
    const dropY = event.offsetY;

    createNodeAtPosition(draggedElementType, dropX, dropY);
    draggedElementType = null; // Reset after drop
}

function createNodeAtPosition(type, x, y) {
    let nodeHTML = '';
    let inputs = 0;
    let outputs = 0;

    switch(type) {
        case 'toDate (d.m.y)':
            nodeHTML = `<div><p>toDate (d.m.y)</p></div>`;
            inputs = 1;
            outputs = 1;
            break;
        case 'constant':
            nodeHTML = `<div><p>Constant</p><input type="text" placeholder="Value"></div>`;
            outputs = 1;
            break;
        case 'string concat':
            nodeHTML = `<div><p>String Concat</p></div>`;
            inputs = 2;
            outputs = 1;
            break;
    }

    if(nodeHTML) {
        editor.addNode(type.toLowerCase().replace(/\s/g, '_'), inputs, outputs, x, y, type, {}, nodeHTML);
    }
}