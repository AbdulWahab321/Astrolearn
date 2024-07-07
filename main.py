from flask import Flask, render_template, request, abort, send_from_directory, jsonify
import markdown
from markdown.extensions import Extension
from markdown.preprocessors import Preprocessor
import os
import re
import json
import sys

app = Flask(__name__)
if __file__.endswith(".py"):
    argv = sys.argv[1:]
host, port = argv[0].split(":")
port = int(port)
dirs_to_ignore_in_data = [".obsidian", "cache"]
# Path to the data directory
DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')

class HighlightExtension(Extension):
    def extendMarkdown(self, md):
        md.preprocessors.register(HighlightPreprocessor(md), 'highlight', 30)

class HighlightPreprocessor(Preprocessor):
    def run(self, lines):
        new_lines = []
        for line in lines:
            line = re.sub(r'==(.+?)==', r'<strong><span style="color: #ED1C24;">\1</span></strong>', line)
            new_lines.append(line)
        return new_lines

def get_subjects():
    """Get a list of subjects from the data directory."""
    return [d for d in os.listdir(DATA_DIR) if os.path.isdir(os.path.join(DATA_DIR, d)) and os.path.exists(os.path.join(DATA_DIR, d,"chapters"))]

def get_chapters(subject, without_ext=False,spaced=False):
    """Get a list of chapter names for a given subject."""
    subject_path = os.path.join(DATA_DIR, subject, 'chapters')
    chapters = [f for f in os.listdir(subject_path) if f.endswith('.md')]
    if without_ext:
        chapters = [os.path.splitext(f)[0].replace("_" if spaced else ""," " if spaced else "") for f in chapters]
    else:
        chapters = [f.replace("_" if spaced else ""," " if spaced else "") for f in chapters]
    return chapters

def get_markdown_content(subject, chapter):
    """Read the content of a Markdown file for a given chapter."""
    chapter_path = os.path.join(DATA_DIR, subject, 'chapters', chapter + '.md')
    with open(chapter_path, 'r', encoding='utf-8') as f:
        content = f.read()
    return content

def get_navigation():
    """Create a dictionary with subjects and their chapters."""
    subjects = get_subjects()
    return {subject: get_chapters(subject, without_ext=True) for subject in subjects}

@app.context_processor
def inject_functions():
    """Inject functions and navigation data into the templates."""
    navigation = get_navigation()
    return dict(get_subjects=get_subjects, navigation=navigation)

@app.route('/')
def index():
    """Render the home page with the list of subjects."""
    subjects = get_subjects()
    return render_template('index.html', subjects=subjects)

@app.route('/<subject>')
def subject(subject):
    """Render the page for a specific subject with a list of chapters."""
    if subject not in get_subjects():
        abort(404)
    navigation = get_navigation()
    chapters = get_chapters(subject, True)
    chapters_names = get_chapters(subject, True,True)
    return render_template('subject.html', subject=subject, chapters_names=chapters_names,chapters=chapters, navigation=navigation)

@app.route('/<subject>/<chapter>')
def chapter(subject, chapter):
    """Render the page for a specific chapter with Markdown content converted to HTML."""
    if chapter not in get_chapters(subject, without_ext=True):
        abort(404)
    content = get_markdown_content(subject, chapter)
    html_content = markdown.markdown(content, extensions=['tables', HighlightExtension()])
    html_content = html_content.replace('src="', f'src="/data/{subject}/chapters/diagrams/{chapter}/')
    if not os.path.exists(os.path.join(DATA_DIR,"cache",subject)):
        os.makedirs(os.path.join(DATA_DIR,"cache",subject))
    with open(os.path.join(DATA_DIR,"cache",subject,chapter+".html"),"w") as f:
        f.write(html_content)
    return render_template('chapter.html', subject=subject, chapter=chapter, content=html_content)

def get_quiz(subject, chapter):
    """Get quiz data for a specific chapter."""
    quiz_path = os.path.join(DATA_DIR, subject, 'quizzes', f'{chapter}.json')
    if os.path.exists(quiz_path):
        with open(quiz_path, 'r') as f:
            return json.load(f)
    return None
@app.route('/<subject>/<chapter>/quiz', methods=['GET', 'POST'])
def quiz(subject, chapter):
    """Render the quiz page for a specific chapter and handle quiz submissions."""
    if chapter not in get_chapters(subject, without_ext=True):
        abort(404)
    
    quiz_data = get_quiz(subject, chapter)
    if not quiz_data:
        abort(404)

    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            score = 0
            correct_answers = {f'q{i}': q['correct_answer'] for i, q in enumerate(quiz_data['questions'])}

            for key, value in data.items():
                if key in correct_answers and value == correct_answers[key]:
                    score += 1

            return jsonify({'score': score, 'total': len(correct_answers)})
        else:
            return jsonify({'error': 'Unsupported Media Type'}), 415

    # For GET request, render the quiz page
    return render_template('quiz.html', subject=subject, chapter=chapter, quiz=quiz_data)

@app.route('/data/<subject>/chapters/diagrams/<chapter>/<path:filename>')
def serve_diagram(subject, chapter, filename):
    """Serve diagram files for chapters."""
    directory = os.path.join(DATA_DIR, subject, 'chapters', 'diagrams', chapter)
    if not os.path.exists(os.path.join(directory, filename)):
        for root, dirs, files in os.walk(directory):
            if filename in files:
                return send_from_directory(root, filename)
    return send_from_directory(directory, filename)

@app.errorhandler(404)
def page_not_found(e):
    """Render the 404 error page."""
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(host, port, debug=True)
