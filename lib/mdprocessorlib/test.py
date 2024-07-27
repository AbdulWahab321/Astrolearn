import re
import markdown2
from bs4 import BeautifulSoup

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
            "span": [start_line_index]
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

class CustomSyntaxExtension(markdown2.Markdown):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.function_parser = FunctionParser()
        self.canvas_parser = None
        
    def preprocess(self, text):
        lines = text.split("\n")
        new_lines = []
        in_canvas = False
        canvas_content = []

        for idx, line in enumerate(lines):
            if line.strip() == "[canvas::init()]":
                in_canvas = True
                self.function_parser.init("canvas", idx)
            elif line.strip() == "[canvas::end()]":
                in_canvas = False
                self.function_parser.end("canvas", idx)
            elif in_canvas:
                self.function_parser.update(line)
            else:
                new_lines.append(line)

        return "\n".join(new_lines)

    def finalize(self, html_output):
        self.canvas_parser = CanvasParser(self.function_parser)
        self.canvas_parser.parse()
        
        for i, canvas_block in enumerate(self.canvas_parser.data):
            canvas_html = "\n".join(canvas_block["data"])
            canvas_html = f'<div class="canvas-container">{canvas_html}</div>'
            html_output += f'\n{canvas_html}'
        
        return html_output

    def convert(self, text):
        preprocessed_text = self.preprocess(text)
        html_output = super().convert(preprocessed_text)
        html_output = self.finalize(html_output)
        return html_output.strip()

# Usage example
if __name__ == "__main__":
    md = CustomSyntaxExtension(extras=["tables", "fenced-code-blocks", "code-friendly"])

    sample_text = """# Introduction
- Trigonometry is the study of relationship between the angles and the sides of a right triangle

## Angle
- Angle is the measure of rotation of the given ray above its  

[canvas::init()]
circle{width:50}
[canvas::end()]"""

    output = md.convert(sample_text)
    print(output)