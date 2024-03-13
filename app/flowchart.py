class DraggableElement:
    def __init__(self, name, node_html, number_of_inputs, number_of_outputs, function=None):
        self.name = name
        self.node_html = node_html
        self.number_of_inputs = number_of_inputs
        self.number_of_outputs = number_of_outputs
        self.function = function

    def to_js_dict(self):
        return {
            "name": self.name,
            "nodeHTML": self.node_html,
            "inputs": self.number_of_inputs,
            "outputs": self.number_of_outputs
        }

    def to_dict(self):
        return {
            "name": self.name,
            "node_html": self.node_html,
            "number_of_inputs": self.number_of_inputs,
            "number_of_outputs": self.number_of_outputs
        }

to_date_d_m_y = DraggableElement(
    "toDate (d.m.y)",
    "<div><p>toDate (d.m.y)</p></div>",
    1,
    1,
)

constant = DraggableElement(
    "constant",
    "<div><p>Constant</p><input type='text' placeholder='Value'></div>",
    0,
    1,
)

string_concatenation = DraggableElement(
    "string concat",
    "<div><p>String Concat</p></div>",
    2,
    1
)


draggable_elements = [to_date_d_m_y, constant, string_concatenation]





