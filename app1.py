#!/usr/bin/env python3
"""
Simple Flask Background Remover - Single File
Save as: app.py
Run with: python app.py

Requirements:
pip install flask rembg pillow
"""

from flask import Flask, request, render_template_string, send_file, jsonify, redirect, url_for
import os
import uuid
import tempfile
from rembg import remove
from PIL import Image
import io

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this'

# Create temp directory for uploads
UPLOAD_DIR = tempfile.mkdtemp()
print(f"📁 Temp directory: {UPLOAD_DIR}")

# HTML Template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Background Remover</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }
        
        .container {
            background: white;
            border-radius: 20px;
            padding: 40px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            max-width: 600px;
            width: 100%;
        }
        
        .header {
            text-align: center;
            margin-bottom: 30px;
        }
        
        .header h1 {
            color: #333;
            font-size: 2.5em;
            margin-bottom: 10px;
        }
        
        .header p {
            color: #666;
            font-size: 1.1em;
        }
        
        .upload-area {
            border: 3px dashed #667eea;
            border-radius: 15px;
            padding: 50px 20px;
            text-align: center;
            margin: 30px 0;
            transition: all 0.3s ease;
            cursor: pointer;
            position: relative;
        }
        
        .upload-area:hover {
            border-color: #764ba2;
            background-color: rgba(102, 126, 234, 0.05);
        }
        
        .upload-area.dragover {
            border-color: #28a745;
            background-color: rgba(40, 167, 69, 0.1);
        }
        
        .upload-icon {
            font-size: 4em;
            color: #667eea;
            margin-bottom: 20px;
        }
        
        .file-input {
            position: absolute;
            opacity: 0;
            width: 100%;
            height: 100%;
            cursor: pointer;
        }
        
        .btn {
            background: linear-gradient(45deg, #667eea, #764ba2);
            color: white;
            border: none;
            padding: 15px 40px;
            border-radius: 50px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            text-decoration: none;
            display: inline-block;
            margin: 10px;
        }
        
        .btn:hover {
            transform: translateY(-3px);
            box-shadow: 0 10px 25px rgba(102, 126, 234, 0.3);
        }
        
        .btn:active {
            transform: translateY(-1px);
        }
        
        .result {
            text-align: center;
            margin-top: 30px;
        }
        
        .result img {
            max-width: 100%;
            border-radius: 15px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.1);
            margin: 20px 0;
        }
        
        .loading {
            display: none;
            text-align: center;
            padding: 40px;
        }
        
        .spinner {
            width: 50px;
            height: 50px;
            border: 5px solid #f3f3f3;
            border-top: 5px solid #667eea;
            border-radius: 50%;
            animation: spin 1s linear infinite;
            margin: 0 auto 20px;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        .message {
            padding: 15px;
            border-radius: 10px;
            margin: 20px 0;
            text-align: center;
        }
        
        .error {
            background: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }
        
        .success {
            background: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }
        
        .file-info {
            background: rgba(102, 126, 234, 0.1);
            padding: 15px;
            border-radius: 10px;
            margin: 15px 0;
            text-align: left;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎨 Background Remover</h1>
            <p>Upload an image and remove its background instantly using AI</p>
        </div>
        
        {% if message %}
        <div class="message {{ message_type }}">
            {{ message }}
        </div>
        {% endif %}
        
        <form id="uploadForm" method="post" enctype="multipart/form-data">
            <div class="upload-area" id="uploadArea">
                <div class="upload-icon">📁</div>
                <h3>Drop your image here or click to browse</h3>
                <p>Supports JPG, PNG, GIF, BMP, WebP (Max: 16MB)</p>
                <input type="file" name="image" id="fileInput" class="file-input" accept="image/*" required>
            </div>
            
            <div id="fileInfo" class="file-info" style="display: none;">
                <strong>Selected file:</strong> <span id="fileName"></span><br>
                <strong>Size:</strong> <span id="fileSize"></span>
            </div>
            
            <div style="text-align: center;">
                <button type="submit" class="btn">✨ Remove Background</button>
            </div>
        </form>
        
        <div id="loading" class="loading">
            <div class="spinner"></div>
            <h3>Processing your image...</h3>
            <p>This usually takes 5-10 seconds</p>
        </div>
        
        {% if result_image %}
        <div class="result">
            <h2>✅ Background Removed Successfully!</h2>
            <img src="/result/{{ result_image }}" alt="Processed Image">
            <br>
            <a href="/download/{{ result_image }}" class="btn">💾 Download Image</a>
            <a href="/" class="btn">➕ Process Another Image</a>
        </div>
        {% endif %}
    </div>

    <script>
        const uploadArea = document.getElementById('uploadArea');
        const fileInput = document.getElementById('fileInput');
        const form = document.getElementById('uploadForm');
        const loading = document.getElementById('loading');
        const fileInfo = document.getElementById('fileInfo');
        
        // Drag and drop functionality
        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
            uploadArea.addEventListener(eventName, preventDefaults, false);
        });
        
        ['dragenter', 'dragover'].forEach(eventName => {
            uploadArea.addEventListener(eventName, highlight, false);
        });
        
        ['dragleave', 'drop'].forEach(eventName => {
            uploadArea.addEventListener(eventName, unhighlight, false);
        });
        
        uploadArea.addEventListener('drop', handleDrop, false);
        
        function preventDefaults(e) {
            e.preventDefault();
            e.stopPropagation();
        }
        
        function highlight(e) {
            uploadArea.classList.add('dragover');
        }
        
        function unhighlight(e) {
            uploadArea.classList.remove('dragover');
        }
        
        function handleDrop(e) {
            const dt = e.dataTransfer;
            const files = dt.files;
            fileInput.files = files;
            showFileInfo(files[0]);
        }
        
        fileInput.addEventListener('change', function() {
            if (this.files[0]) {
                showFileInfo(this.files[0]);
            }
        });
        
        function showFileInfo(file) {
            document.getElementById('fileName').textContent = file.name;
            document.getElementById('fileSize').textContent = (file.size / (1024*1024)).toFixed(2) + ' MB';
            fileInfo.style.display = 'block';
        }
        
        form.addEventListener('submit', function() {
            loading.style.display = 'block';
            form.style.display = 'none';
        });
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/', methods=['POST'])
def upload():
    if 'image' not in request.files:
        return render_template_string(HTML_TEMPLATE, 
                                    message="No file selected", 
                                    message_type="error")
    
    file = request.files['image']
    if file.filename == '':
        return render_template_string(HTML_TEMPLATE, 
                                    message="No file selected", 
                                    message_type="error")
    
    try:
        # Generate unique filename
        file_id = str(uuid.uuid4())
        
        # Read uploaded file
        input_data = file.read()
        
        # Validate file size (16MB limit)
        if len(input_data) > 16 * 1024 * 1024:
            return render_template_string(HTML_TEMPLATE, 
                                        message="File too large. Maximum size is 16MB", 
                                        message_type="error")
        
        # Remove background
        print("🔄 Processing image...")
        output_data = remove(input_data)
        
        # Save processed image
        output_path = os.path.join(UPLOAD_DIR, f"{file_id}.png")
        with open(output_path, 'wb') as f:
            f.write(output_data)
        
        print("✅ Image processed successfully!")
        
        return render_template_string(HTML_TEMPLATE, 
                                    result_image=file_id,
                                    message="Background removed successfully!", 
                                    message_type="success")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return render_template_string(HTML_TEMPLATE, 
                                    message=f"Error processing image: {str(e)}", 
                                    message_type="error")

@app.route('/result/<file_id>')
def show_result(file_id):
    file_path = os.path.join(UPLOAD_DIR, f"{file_id}.png")
    if os.path.exists(file_path):
        return send_file(file_path, mimetype='image/png')
    return "File not found", 404

@app.route('/download/<file_id>')
def download_result(file_id):
    file_path = os.path.join(UPLOAD_DIR, f"{file_id}.png")
    if os.path.exists(file_path):
        return send_file(file_path, 
                        as_attachment=True, 
                        download_name=f"no_background_{file_id}.png",
                        mimetype='image/png')
    return "File not found", 404

if __name__ == '__main__':
    print("🚀 Starting Background Remover...")
    print("📱 Open: http://127.0.0.1:5000")
    print("⏹️  Press Ctrl+C to stop")
    print("-" * 50)
    
    try:
        app.run(debug=True, host='127.0.0.1', port=5000)
    except KeyboardInterrupt:
        print("\n👋 Server stopped!")
    finally:
        # Cleanup temp directory
        import shutil
        try:
            shutil.rmtree(UPLOAD_DIR)
            print("🧹 Cleaned up temporary files")
        except:
            pass