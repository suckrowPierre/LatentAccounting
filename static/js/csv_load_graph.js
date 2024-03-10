var editor = null;

function load_flowchart(output_columns) {
    console.log(output_columns)
    const id = document.getElementById("drawflow");
    editor = new Drawflow(id);
    editor.start();

    editor.zoom_max = 1.6;
    editor.zoom_min = 0.5;
    editor.zoom_value = 0.1;
    editor.editor_mode = 'edit';




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
        editor.addNode(`node_${csv_columns[i]}`, 0, 1, 100, i*40+50, 'example', data, htmlNode);
    }

    //create output nodes
    for ( let i = 0; i < output_columns.length; i++) {
        const htmlNode = `
        <div class="text-sm">
            <p>${output_columns[i]}</p>
        </div>
        `;
        const data = { "name": output_columns[i] };
        editor.addNode(`output_node_${output_columns[i]}`, 1, 0, 500, i*40+50, 'output', data, htmlNode);
    }

}
