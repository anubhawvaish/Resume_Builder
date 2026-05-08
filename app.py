from flask import Flask, render_template, request, redirect
import pdfplumber
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


skills_database = [
    'python',
    'java',
    'flask',
    'django',
    'html',
    'css',
    'javascript',
    'mysql',
    'machine learning',
    'data structures',
    'react',
    'git',
    'github'
]


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/builder')
def builder():
    return render_template('builder.html')


@app.route('/analyzer')
def analyzer():
    return render_template('analyzer.html')


@app.route('/analyze', methods=['POST'])
def analyze_resume():

    file = request.files['resume']

    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)

    text = ''

    with pdfplumber.open(filepath) as pdf:
        for page in pdf.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted.lower()

    found_skills = []
    missing_skills = []

    for skill in skills_database:
        if skill in text:
            found_skills.append(skill)
        else:
            missing_skills.append(skill)

    score = int((len(found_skills) / len(skills_database)) * 100)

    suggestions = []

    if score < 40:
        suggestions.append('Add more technical skills')
        suggestions.append('Add strong projects section')
        suggestions.append('Improve formatting')

    elif score < 70:
        suggestions.append('Add internships and certifications')
        suggestions.append('Improve keyword optimization')

    else:
        suggestions.append('Resume looks strong')
        suggestions.append('Add measurable achievements')

    return render_template(
        'result.html',
        score=score,
        found_skills=found_skills,
        missing_skills=missing_skills,
        suggestions=suggestions
    )


if __name__== '__main__':
    app.run(debug=True)