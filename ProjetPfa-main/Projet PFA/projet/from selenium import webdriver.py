from flask import Flask, request, jsonify, render_template, redirect, url_for, send_from_directory
import os
import uuid
from profile_manager import load_profiles, match_profiles, add_profile, delete_profile
from utils import extract_text_from_pdf, extract_text_from_docx, generate_swot_analysis, query_llm, summarize_job_description
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'docx'}

# Ensure upload folder
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def home():
    results = []
    if request.method == 'POST' and 'title' in request.form:
        # Job matching
        title = request.form['title']
        description = request.form['description']
        query = f"{title} {description}".strip()
        try:
            profiles = load_profiles('profiles.json')
            results = match_profiles(query, profiles)
        except FileNotFoundError:
            results = []
    return render_template('index.html', results=results)

@app.route('/open_cv/<filename>')
def open_cv(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/analyse', methods=['POST'])
def analyse():
    if 'cv' not in request.files:
        return "No file uploaded", 400
    cv_file = request.files['cv']
    if cv_file and allowed_file(cv_file.filename):
        name = uuid.uuid4().hex + '_' + secure_filename(cv_file.filename)
        path = os.path.join(app.config['UPLOAD_FOLDER'], name)
        cv_file.save(path)
        if name.lower().endswith('.pdf'):
            text = extract_text_from_pdf(path)
        else:
            text = extract_text_from_docx(path)
        swot = generate_swot_analysis(text)
        return jsonify(swot)
    return "Unsupported file format", 400

@app.route('/match', methods=['POST'])
def match():
    if request.content_type != 'application/json':
        return jsonify({"error": "Unsupported Media Type"}), 415
    data = request.get_json()
    query = f"{data.get('title','')} {data.get('description','')}".strip()
    try:
        profiles = load_profiles('profiles.json')
    except FileNotFoundError:
        return jsonify({"error": "profiles.json not found"}), 500
    results = match_profiles(query, profiles)
    return jsonify({"matches": results})

@app.route('/chat', methods=['POST'])
def chat():
    if request.content_type != 'application/json':
        return jsonify({"error": "Unsupported Media Type"}), 415
    data = request.get_json()
    user_message = data.get('message', '')
    if not user_message:
        return jsonify({"error": "No message provided"}), 400
    response = query_llm(user_message)
    return jsonify({"response": response})

@app.route('/profiles', methods=['GET', 'POST', 'DELETE'])
def profiles():
    if request.method == 'GET':
        try:
            profiles = load_profiles('profiles.json')
        except FileNotFoundError:
            return jsonify([])
        return jsonify(profiles)
    elif request.method == 'POST':
        data = request.get_json()
        add_profile(data, 'profiles.json')
        return jsonify({"message": "Profile added successfully"}), 201
    elif request.method == 'DELETE':
        data = request.get_json()
        profile_id = data.get('id')
        if not profile_id:
            return jsonify({"error": "Profile ID is required"}), 400
        delete_profile(profile_id, 'profiles.json')
        return jsonify({"message": "Profile deleted successfully"})

@app.route('/summarize', methods=['POST'])
def summarize():
    if request.content_type != 'application/json':
        return jsonify({"error": "Unsupported Media Type"}), 415
    data = request.get_json()
    description = data.get('description', '')
    if not description:
        return jsonify({"error": "No description provided"}), 400
    summary = summarize_job_description(description)
    return jsonify({"summary": summary})

if __name__ == '__main__':
    app.run(debug=True)