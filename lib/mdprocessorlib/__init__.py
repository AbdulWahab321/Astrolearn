import re
import markdown2
from bs4 import BeautifulSoup

btn_class = "inline-block bg-secondary-light dark:bg-secondary-dark text-white py-2 px-4 rounded hover:bg-opacity-80 transition duration-300 q_and_a_button"

class CustomSyntaxExtension(markdown2.Markdown):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.math_blocks = []
        self.inline_math = []

    def preprocess(self, text):
        # Handle block math
        text = re.sub(r'\$\$(.+?)\$\$', lambda m: self.process_math_block(m.group(1)), text)
        
        # Handle inline math
        text = re.sub(r'(?<!\$)\$(?!\$)(.+?)(?<!\$)\$(?!\$)', lambda m: self.process_inline_math(m.group(1)), text)

        lines = text.split("\n")
        new_lines = []
        in_math_block = False
        math_content = []
        multiline_question = False
        question_text = ""
        answer_lines = []

        for line in lines:
            # Highlighting

            line = re.sub(r'==(.+?)==', r'<span class="highlighted_text">\1</span>', line)
             
            # Math block handling
            if line.strip().startswith('$$') and not in_math_block:
                in_math_block = True
                math_content = [line.strip()[2:]]
            elif line.strip().endswith('$$') and in_math_block:
                math_content.append(line.strip()[:-2])
                new_lines.append(self.process_math_block('\n'.join(math_content)))
                in_math_block = False
                math_content = []
            elif in_math_block:
                math_content.append(line)

            # Multiline question handling
            elif multiline_question:
                if re.search(r"};", line):
                    answer_html = markdown2.markdown("\n".join(answer_lines).strip())
                    new_lines.append(f"""<div class="question"><p>{question_text.strip()}</p><button class="{btn_class}" onclick="">Show Answer</button><div class="q_and_a_answer">{answer_html}</div></div>""")
                    multiline_question = False
                    question_text = ""
                    answer_lines = []
                else:
                    answer_lines.append(line)
                continue

            elif re.search(r"<Q\[(.+?)\]\?{\s*", line):
                multiline_question = True
                question_text = re.search(r"<Q\[(.+?)\]\?{\s*", line).group(1)
                continue

            # In-line question and answer handling
            elif "<Q[" in line and "]>" in line:
                line = re.sub(r'<Q\[(.+?)\]\?\[(.+?)\]>', fr'<div class="question"><p>\1</p><button class="{btn_class}" onclick="">Show Answer</button><p class="q_and_a_answer">\2</p></div>', line)
                new_lines.append(line)

            # Regular line
            else:
                new_lines.append(line)

        return '\n'.join(new_lines)

    def process_math_block(self, content):
        self.math_blocks.append(content)
        return f"<!-- math_block_{len(self.math_blocks) - 1} -->"

    def process_inline_math(self, content):
        self.inline_math.append(content)
        return f"<!-- inline_math_{len(self.inline_math) - 1} -->"

    def process_tables(self, html_output):
        soup = BeautifulSoup(html_output, 'html.parser')
        tables = soup.find_all('table')
        for table in tables:
            table['class'] = table.get('class', []) + ['custom-table']
            
            # Process headers
            if table.thead:
                for th in table.thead.find_all('th'):
                    th['class'] = th.get('class', []) + ['custom-th']
            else:
                first_row = table.find('tr')
                if first_row:
                    for td in first_row.find_all('td'):
                        td.name = 'th'
                        td['class'] = td.get('class', []) + ['custom-th']
                    first_row.wrap(soup.new_tag('thead'))

            # Process body
            if not table.tbody:
                body_rows = table.find_all('tr')[1:] if table.thead else table.find_all('tr')
                tbody = soup.new_tag('tbody')
                for row in body_rows:
                    tbody.append(row)
                table.append(tbody)

            # Add classes to body cells
            for td in table.tbody.find_all('td'):
                td['class'] = td.get('class', []) + ['custom-td']

        return str(soup)

    def finalize(self, html_output):
        for i, math_content in enumerate(self.math_blocks):
            math_html = f'<div class="math-block">$${math_content}$$</div>'
            placeholder = f"<!-- math_block_{i} -->"
            html_output = html_output.replace(placeholder, math_html)
        
        for i, math_content in enumerate(self.inline_math):
            math_html = f'<span class="inline-math">${math_content}$</span>'
            placeholder = f"<!-- inline_math_{i} -->"
            html_output = html_output.replace(placeholder, math_html)
        
        return html_output

    def convert(self, text):
        preprocessed_text = self.preprocess(text)
        html_output = super().convert(preprocessed_text)
        html_output = self.process_tables(html_output)
        html_output = self.finalize(html_output)
        return html_output

if __name__ == "__main__":
    md = CustomSyntaxExtension(extras=["tables", "fenced-code-blocks", "code-friendly"])

    sample_text = """
    This is a paragraph with an inline math block: $$ E = mc^2 $$ and some more text with inline math: $v = \frac{dx}{dt}$.

    | Column 1 | Column 2 | Column 3 |
    |----------|----------|----------|
    | Normal text | $$ e = mc^2 $$ | More text |
    | Another row | With content | $F = ma$ |

    ### Mass of electron
    - The charge to mass ratio of an electron was determined by Thomson as:
      $$ \frac{e}{m_e} = 1.758820 \times 10^{11} \, \text{C kg}^{-1} $$
    - The charge of the electron was determined by **R.A Millikan** by **Oil Drop Experiment** as:
      $e = -1.6 \times 10^{-19} \, \text{C}$
    - The mass of the electron was determined by as follows:
      $$ m_e = \frac{e}{\left(\frac{e}{m_e}\right)} = \frac{1.6 \times 10^{-19}}{1.758820 \times 10^{11}} \approx 9.1094 \times 10^{-31} \, \text{kg} $$

    Here's a ==highlighted== text.

    <Q[What is the speed of light?][The speed of light in vacuum is approximately 299,792,458 meters per second.]>
    """

    print(md.convert(sample_text))