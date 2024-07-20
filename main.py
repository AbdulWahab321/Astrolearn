from flask import Flask, render_template, request, abort, send_from_directory, jsonify
import os
import re
import json
import sys
from lib.mdprocessorlib import CustomSyntaxExtension
app = Flask(__name__)

dirs_to_ignore_in_data = [".obsidian", "cache"]
# Path to the data directory
WEBSITE_NAME = "AstroLearn"
DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
STATIC = "--static-mode" in sys.argv
WRITE_CACHE = "--write-cache" in sys.argv
md = CustomSyntaxExtension(extras=["tables"])
    
def get_subjects():
    """Get a list of subjects from the data directory."""
    return [d for d in os.listdir(DATA_DIR) if os.path.isdir(os.path.join(DATA_DIR, d)) and os.path.exists(os.path.join(DATA_DIR, d,"chapters"))]

def get_chapters(subject, without_ext=False,spaced=False):
    """Get a list of chapter names for a given subject."""
    subject_path = os.path.join(DATA_DIR, subject, 'chapters')
    chapters =  sorted([f for f in os.listdir(subject_path) if f.endswith('.md')],key=lambda x:int(x.split("_",maxsplit=1)[0]))
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
def get_flash_cards(subject,chapter):
    """Get flash card data for a specific chapter."""
    flash_cards_path = os.path.join(DATA_DIR, subject, 'flashcards', f'{chapter}.json')
    if os.path.exists(flash_cards_path):
        with open(flash_cards_path, 'r') as f:
            return f.read()
    return "[]"
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

    return render_template('index.html',website_name = WEBSITE_NAME)

@app.route('/notes',endpoint="notes")
def notes():
    subjects = get_subjects()
    return render_template('notes.html',subjects=subjects,website_name = WEBSITE_NAME)

@app.route('/pyq')
def pyq():
    with open(os.path.join(DATA_DIR,"pyqs.json")) as jsf:
        pyqs = json.load(jsf)    
    return render_template('pyq.html',pyqs=pyqs,website_name = WEBSITE_NAME)

@app.route('/view_pdf')
def view_pdf():  # You can dynamically set this based on your requirements
    pdf_link = request.args.get('pdf_link')
    subject = request.args.get('subject')
    year = request.args.get('year')
    
    if not pdf_link:
        return "PDF link is missing", 400    
    return render_template('pdf_view.html', pdf_link=pdf_link,subject= subject,year=year,website_name = WEBSITE_NAME)

@app.route('/submit_quiz', methods=['POST'])
def submit_quiz():
    data = request.json
    answers = data.get('answers', {})
    # Process the answers, e.g., calculate score
    # For example:
    # score = calculate_score(answers)
    # message = f'Your score is {score}/{total_questions}'
    
    # Replace with actual processing logic
    message = "Quiz submitted successfully!"  # Change this as needed

    return jsonify({'message': message})


@app.route('/quiz_selection',endpoint="quiz_selection")
def quiz_selection():
    quiz_structure = {}
    
    for subject in os.listdir(DATA_DIR):
        subject_path = os.path.join(DATA_DIR, subject, 'quizzes')
        if os.path.isdir(subject_path):
            quiz_structure[subject] = [
                chapter.replace('.json', '') 
                for chapter in os.listdir(subject_path) 
                if chapter.endswith('.json')
            ]
    
    return render_template('quiz_selection.html', quiz_structure=quiz_structure,website_name = WEBSITE_NAME)

@app.route('/quiz/<subject>/<chapter>',endpoint="quiz")
def quiz(subject, chapter):
    quiz_time_limit = 600  # 10 minutes, adjust as needed
    quiz_file = f'data/{subject}/quizzes/{chapter}.json'
    if os.path.exists(quiz_file):
        with open(quiz_file, 'r') as f:
            quiz_data = json.load(f)
        return render_template('quiz.html', subject=subject, chapter=chapter, quiz_data=quiz_data, quiz_time_limit=quiz_time_limit, website_name = WEBSITE_NAME)
    else:
        return render_template('404.html'), 404

@app.route('/<subject>')
def subject(subject):
    """Render the page for a specific subject with a list of chapters."""
    if subject not in get_subjects():
        abort(404)
    navigation = get_navigation()
    chapters = get_chapters(subject, True)
    return render_template('subject.html',website_name = WEBSITE_NAME, subject=subject,chapters=chapters, navigation=navigation)

@app.route('/<subject>/<chapter>')
def chapter(subject, chapter):
    if chapter not in get_chapters(subject, without_ext=True):
        abort(404)
    
    if not STATIC:
        content = get_markdown_content(subject, chapter)
        
        html_content = md.convert(content)
        #html_content = md.finalize(html_content)
        #html_content = finalize_post_processing_md(html_content)
        #print("HTML content:", html_content)  # Debug print
        html_content = html_content.replace('src="', f'src="/data/{subject}/chapters/diagrams/{chapter}/')               
        if WRITE_CACHE:
            if not os.path.exists(os.path.join(DATA_DIR,"cache",subject)):
                os.makedirs(os.path.join(DATA_DIR,"cache",subject))            
            with open(os.path.join(DATA_DIR,"cache",subject,chapter+".html"),"w") as file:
                file.write(html_content)
        return render_template('chapter.html',website_name = WEBSITE_NAME, subject=subject, chapter=chapter, content=html_content, flashcards = get_flash_cards(subject,chapter),is_chapter_page=True)
    else:

        with open(os.path.join(DATA_DIR,"cache",subject,chapter+".html")) as htmlfile:
            return htmlfile.read()
        



@app.route('/data/<subject>/chapters/diagrams/<chapter>/<path:filename>')
def serve_diagram(subject, chapter, filename):
    """Serve diagram files for chapters."""
    chapter = chapter.split("_",maxsplit=1)[1]
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
@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response
if __name__ == '__main__':
    app.run(debug=True)
