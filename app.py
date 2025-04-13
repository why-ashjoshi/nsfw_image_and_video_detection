import os
from flask import Flask, render_template, request, redirect, url_for
from image_detection import detect_nudity, is_nsfw
from video_processing import process_video

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload_image', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)
    
    nsfw_score = detect_nudity(file_path)
    is_nsfw_image = is_nsfw(nsfw_score)
    
    return render_template('result.html', is_nsfw=is_nsfw_image, nsfw_score=nsfw_score)

@app.route('/upload_video', methods=['POST'])
def upload_video():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)
    
    results = process_video(file_path)
    
    return render_template('video_result.html', results=results)

if __name__ == '__main__':
    app.run(debug=True)
