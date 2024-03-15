import json
import app.csv_loader.converters as converters


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
    "todate_(d.m.y)",
    "<div><p>toDate (d.m.y)</p></div>",
    1,
    1,
    converters.string_date_to_date_d_m_y
)

constant = DraggableElement(
    "constant",
    "<div><p>Constant</p><input type='text' placeholder='Value'></div>",
    0,
    1,
)

string_concatenation = DraggableElement(
    "string_concat",
    "<div><p>String Concat</p></div>",
    2,
    1,
    converters.concatenate_strings
)

def filter_nodes_by_class(nodes, class_name):
    result = []
    for node in nodes:
        if node["class"] == class_name:
            result.append(node)
    return result


draggable_elements = [to_date_d_m_y, constant, string_concatenation]


def build_conversion_functions(flowchart_diagram):
    diagram = list(json.loads(flowchart_diagram)["drawflow"]["Home"]["data"].values())
    node_map = {str(node["id"]): node for node in diagram}
    outputs = [node for node in diagram if node["class"] == "output"]
    conversion_functions = {}

    for output in outputs:
        # The output node itself does not need a function; we start from its input
        input_chain_function = build_function_chain(str(output["id"]), diagram, node_map)
        conversion_functions[output["name"]] = input_chain_function

    return conversion_functions



def get_function_by_name(name):
    for element in draggable_elements:
        if element.name == name:
            return element.function
    return None

def build_function_chain(node_id, diagram, node_map):
    node = node_map[node_id]
    # If the node is an input, return a lambda function to fetch the input value
    if node["class"] == "input":
        return lambda row, name=node["name"]: row[name]

    # For function nodes, build the chain
    elif node["class"] == "function":
        node_function = get_function_by_name(node["name"])
        if not node_function:
            raise ValueError(f"No function found for node: {node['name']}")

        # Handle multiple inputs
        input_connections = [conn for inp in node["inputs"].values() for conn in inp["connections"]]
        if not input_connections:
            raise ValueError(f"No input connections found for node: {node['name']}")

        input_chain_functions = [build_function_chain(str(conn["node"]), diagram, node_map) for conn in input_connections]

        # If the function expects multiple arguments, adjust accordingly
        if len(input_chain_functions) > 1:
            return lambda row, f=node_function, icfs=input_chain_functions: f(*[icf(row) for icf in icfs])
        else:
            # Single input, maintain previous behavior for simplicity
            return lambda row, f=node_function, icf=input_chain_functions[0]: f(icf(row))

    # Output nodes do not represent a transformation and should not be reached directly in this context
    elif node["class"] == "output":
        input_connections = next(iter(node["inputs"].values()))["connections"]
        if not input_connections:
            raise ValueError(f"Output node '{node['name']}' does not have inputs.")
        # Directly proceed to the connected node
        connected_node_id = str(input_connections[0]["node"])
        return build_function_chain(connected_node_id, diagram, node_map)

    else:
        raise ValueError(f"Unhandled node class: {node['class']}")



