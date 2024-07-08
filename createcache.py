import markdown
from markdown.extensions import Extension
from markdown.preprocessors import Preprocessor
import os
import re
import jinja2

# Define directories
DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')

class HighlightExtension(Extension):
    def extendMarkdown(self, md):
        md.preprocessors.register(HighlightPreprocessor(md), 'highlight', 30)

class HighlightPreprocessor(Preprocessor):
    def run(self, lines):
        new_lines = []
        multiline_question = False
        question_text = ""
        answer_lines = []
        for line in lines:
            line = re.sub(r'==(.+?)==', r'<strong><span class="highlighted_text">\1</span></strong>', line)
            if multiline_question:
                if re.search(r"}::>", line):
                    answer_html = markdown.markdown("\n".join(answer_lines).strip())
                    new_lines.append(f"""<div class="question"><p>{question_text.strip()}</p><button class="q_and_a_button" onclick="">Show Answer</button><div class="q_and_a_answer">{answer_html}</div></div>""")
                    multiline_question = False
                    question_text = ""
                    answer_lines = []
                else:
                    answer_lines.append(line)
                continue
            match = re.match(r".+<Q::(.+?)::{\s*", line)
            if match:
                multiline_question = True
                question_text = match.group(1)
                continue
            line = re.sub(r'<Q::(.+?)::(.+?)>', r"""<div class="question"><p>\1</p><button class="q_and_a_button" onclick="">Show Answer</button><p class="q_and_a_answer">\2</p></div>""", line)
            new_lines.append(line)
        return new_lines

def get_subjects():
    return [d for d in os.listdir(DATA_DIR) if os.path.isdir(os.path.join(DATA_DIR, d)) and os.path.exists(os.path.join(DATA_DIR, d,"chapters"))]

def get_chapters(subject, without_ext=False, spaced=False):
    subject_path = os.path.join(DATA_DIR, subject, 'chapters')
    chapters = sorted([f for f in os.listdir(subject_path) if f.endswith('.md')])
    if without_ext:
        chapters = [os.path.splitext(f)[0].replace("_" if spaced else ""," " if spaced else "") for f in chapters]
    else:
        chapters = [f.replace("_" if spaced else ""," " if spaced else "") for f in chapters]
    return chapters

def get_markdown_content(subject, chapter):
    chapter_path = os.path.join(DATA_DIR, subject, 'chapters', chapter + '.md')
    with open(chapter_path, 'r', encoding='utf-8') as f:
        content = f.read()
    return content

def create_cache():
    template_env = jinja2.Environment(loader=jinja2.FileSystemLoader(searchpath="./templates"))
    template = template_env.get_template('cache_base.html')
    
    for subject in get_subjects():
        for chapter in get_chapters(subject, True):
            content = get_markdown_content(subject, chapter)
            html_content = markdown.markdown(content, extensions=['tables', HighlightExtension()])
            html_content = html_content.replace('src="', f'src="/data/{subject}/chapters/diagrams/{chapter}/')
            
            if not os.path.exists(os.path.join(DATA_DIR, "cache", subject)):
                os.makedirs(os.path.join(DATA_DIR, "cache", subject))
            
            rendered_html = template.render(subject=subject, chapter=chapter+"", content=html_content)
            
            with open(os.path.join(DATA_DIR, "cache", subject, chapter + ".html"), "w", encoding="utf-8") as f:
                f.write(rendered_html)

if __name__ == "__main__":
    create_cache()
