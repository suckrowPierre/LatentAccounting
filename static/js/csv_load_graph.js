var editor = null;
var output_columns = null;
var draggableElements = null;

function getEditorState() {
    return JSON.stringify(editor.export());
}

function set_output_columns(columns) {
    output_columns = columns;
}

function load_editor_state(stateString = null, draggable_elements = null) {
    console.log("loading editor state");
    editor = null;
    console.log(draggable_elements);
    draggableElements = draggable_elements;
    start_editor();
    if (editor && (stateString !== null)){
        import_editor_state(stateString);
    }
    compareInputCSVToEditorNodesAndCreate();
    compareOutputCSVToEditorNodesAndCreate();
    setupDragAndDrop()

    const csvSeparatorInput = document.getElementById('csv-seperator');
    const csvColumnsInput = document.getElementById('csv-columns');
    csvSeparatorInput.addEventListener('change', compareInputCSVToEditorNodesAndCreate);
    csvColumnsInput.addEventListener('change', compareInputCSVToEditorNodesAndCreate);
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

    const inputNodes = getNodesFromClass('input');
    var copyInputNodes = inputNodes.slice();

    console.log(csv_columns.length)
    console.log(csv_columns)
    for (let i = 0; i < csv_columns.length; i++) {
        if (csv_columns[i] !== "") {
            if (inputNodes === [] || !findNodeByName(inputNodes, "input" + csv_columns[i])) {
                createNode(csv_columns[i], 0, i * 40 + 20, 'input', 0, 1);
            } else if (inputNodes !== [] && findNodeByName(inputNodes, "input" + csv_columns[i])) {
                copyInputNodes = removeNodeByName(copyInputNodes, "input" + csv_columns[i]);
            }
        }
    }

    for (let i = 0; i < copyInputNodes.length; i++) {
            editor.removeNodeId("node-" + copyInputNodes[i].id);
    }

}

function compareOutputCSVToEditorNodesAndCreate() {
    const outputNodes = getNodesFromClass('output');
    var copyOutputNodes = outputNodes.slice();

    for (let i = 0; i < output_columns.length; i++) {
        if (outputNodes === [] || !findNodeByName(outputNodes, "output" + output_columns[i]) ) {
            createNode(output_columns[i], 650, i*40+20, 'output', 1, 0);
        } else if (outputNodes !== [] && findNodeByName(outputNodes, "output" + output_columns[i])) {
            copyOutputNodes = removeNodeByName(copyOutputNodes, "output" + output_columns[i]);
        }
    }
    for (let i = 0; i < copyOutputNodes.length; i++) {
            editor.removeNodeId("node-" + copyOutputNodes[i].id);
    }
}

function import_editor_state(stateString) {
    console.log(stateString);
    const state = JSON.parse(stateString);
    console.log("importing state");
    editor.import(state);
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

    draggableElements.forEach(element => {
        if (element.name === type) {
            console.log("match found" + element.name);
            nodeHTML = element.nodeHTML;
            inputs = element.inputs;
            outputs = element.outputs;
        }
    });

    if(nodeHTML) {
        editor.addNode(type.toLowerCase().replace(/\s/g, '_'), inputs, outputs, x, y, type, {}, nodeHTML);
    }
}