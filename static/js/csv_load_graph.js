var id = document.getElementById("drawflow");
    const editor = new Drawflow(id);
    editor.start();

    // Add two nodes
    var htmlNode1 = `
      <div style="border: 1px solid #000; padding: 10px;">
        <p>Node 1 Content</p>
      </div>
    `;
    var data1 = { "name": 'Node 1' };
    editor.addNode('node1', 0, 1, 100, 100, 'example', data1, htmlNode1);

    var htmlNode2 = `
      <div style="border: 1px solid #000; padding: 10px;">
        <p>Node 2 Content</p>
      </div>
    `;
    var data2 = { "name": 'Node 2' };
    editor.addNode('node2', 1, 0, 300, 100, 'example', data2, htmlNode2);

    // Allow connection between nodes
    editor.addConnection('node1_output_1', 'node2_input_1', 'output_1', 'input_1');