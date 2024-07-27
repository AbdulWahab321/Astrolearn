<<<<<<< HEAD
import re

class FunctionParser:
    def __init__(self):
        self.functions = {
            "type": {
                "canvas": []
            }
        }
        self.functions_on_process = []

    def init(self, function, start_line_index):
        self.functions["type"][function].append({
            "data": [],
            "span": [start_line_index + 1]
        })
        self.functions_on_process.append([function, len(self.functions["type"][function]) - 1])

    def update(self, line):
        if self.functions_on_process and not re.match(r"\[(.*)::init\(\)\]", line) and not re.match(r"\[(.*)::end\(\)\]", line):
            function, index = self.functions_on_process[-1]
            self.functions["type"][function][index]["data"].append(line)

    def end(self, function, end_line_index):
        if self.functions_on_process and function == self.functions_on_process[-1][0]:
            function, func_index = self.functions_on_process.pop()
            self.functions["type"][function][func_index]["span"].append(end_line_index)

class CanvasParser:
    def __init__(self, func_parser):
        self.func_parser = func_parser
        self.data = list(reversed(func_parser.functions["type"]["canvas"]))
        self.func_matches = {
            "shape_construct": r"(.*)\{((.*)\:(.*)\,?)*\}"
        }
        self.shapes = {}

    def parse(self):
        for canvas_block in self.data:
            new_data = []
            for line in canvas_block["data"]:
                shape_construct_match = re.match(self.func_matches["shape_construct"], line)
                if shape_construct_match:
                    shape_name = shape_construct_match.group(1)
                    parameters = shape_construct_match.group(2)
                    
                    # Convert shape to HTML tag
                    html_tag = f"<{shape_name}"
                    for param in parameters.split(","):
                        key, value = param.split(":")
                        html_tag += f' {key.strip()}={value.strip()}'
                    html_tag += f"></{shape_name}>"
                    
                    new_data.append(html_tag)
                else:
                    new_data.append(line)
            
            # Update the canvas block data with the new HTML tags
            canvas_block["data"] = new_data
            print(new_data)

    def update_spans(self):
        line_diff = 0
        for canvas_block in self.data:
            start, end = canvas_block["span"]
            canvas_block["span"] = [start + line_diff, end + line_diff]
=======
import re

class FunctionParser:
    def __init__(self):
        self.functions = {
            "type": {
                "canvas": []
            }
        }
        self.functions_on_process = []

    def init(self, function, start_line_index):
        self.functions["type"][function].append({
            "data": [],
            "span": [start_line_index + 1]
        })
        self.functions_on_process.append([function, len(self.functions["type"][function]) - 1])

    def update(self, line):
        if self.functions_on_process and not re.match(r"\[(.*)::init\(\)\]", line) and not re.match(r"\[(.*)::end\(\)\]", line):
            function, index = self.functions_on_process[-1]
            self.functions["type"][function][index]["data"].append(line)

    def end(self, function, end_line_index):
        if self.functions_on_process and function == self.functions_on_process[-1][0]:
            function, func_index = self.functions_on_process.pop()
            self.functions["type"][function][func_index]["span"].append(end_line_index)

class CanvasParser:
    def __init__(self, func_parser):
        self.func_parser = func_parser
        self.data = list(reversed(func_parser.functions["type"]["canvas"]))
        self.func_matches = {
            "shape_construct": r"(.*)\{((.*)\:(.*)\,?)*\}"
        }
        self.shapes = {}

    def parse(self):
        for canvas_block in self.data:
            new_data = []
            for line in canvas_block["data"]:
                shape_construct_match = re.match(self.func_matches["shape_construct"], line)
                if shape_construct_match:
                    shape_name = shape_construct_match.group(1)
                    parameters = shape_construct_match.group(2)
                    
                    # Convert shape to HTML tag
                    html_tag = f"<{shape_name}"
                    for param in parameters.split(","):
                        key, value = param.split(":")
                        html_tag += f' {key.strip()}={value.strip()}'
                    html_tag += f"></{shape_name}>"
                    
                    new_data.append(html_tag)
                else:
                    new_data.append(line)
            
            # Update the canvas block data with the new HTML tags
            canvas_block["data"] = new_data
            print(new_data)

    def update_spans(self):
        line_diff = 0
        for canvas_block in self.data:
            start, end = canvas_block["span"]
            canvas_block["span"] = [start + line_diff, end + line_diff]
>>>>>>> 77990087da15310786318a82e2d150ed2cfa2a62
            line_diff += len(canvas_block["data"]) - (end - start - 1)