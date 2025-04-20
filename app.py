from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import flask
import requests
import xml.etree.ElementTree as ET
import os
import uuid
import mimetypes
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = os.urandom(24)

# S3 Configuration
S3_BUCKET = "file-storage-bucket12"
S3_REGION = "us-east-1"  # Fix typo in variable name (REGION)
S3_URL = f"https://{S3_BUCKET}.s3.{S3_REGION}.amazonaws.com"

# Allowed extensions
ALLOWED_EXTENSIONS = {'pdf', 'jpg', 'jpeg', 'png', 'gif', 'txt', 'doc', 'docx', 'xls', 'xlsx', 'csv'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def list_files_from_s3():
    """List all files from the S3 bucket using the REST API"""
    try:
        # Make request to S3 bucket's REST API
        response = requests.get(f"{S3_URL}/?list-type=2")
        
        if response.status_code == 200:
            # Parse the XML response
            root = ET.fromstring(response.content)
            
            # Define namespace for XML parsing
            ns = {'s3': 'http://s3.amazonaws.com/doc/2006-03-01/'}
            
            files = []
            for content in root.findall('.//s3:Contents', ns):
                key = content.find('s3:Key', ns).text
                size = float(content.find('s3:Size', ns).text) / 1024  # Convert to KB
                last_modified = content.find('s3:LastModified', ns).text
                
                # create the download URL with proper headers
                original_filename = key.split('_', 1)[-1]  # Remove UUID prefix
                download_url = f"{S3_URL}/{key}?response-content-disposition=attachment; filename=\"{original_filename}\""

                files.append({
                    'name': key,
                    'size': round(size, 2),  # Size in KB with 2 decimal places
                    'last_modified': last_modified,
                    'url': f"{S3_URL}/{key}"  # Direct download URL
                })
            return files
        else:
            flash(f"Failed to list files. S3 returned status: {response.status_code}", "error")
            return []
    except Exception as e:
        flash(f"Error listing files from S3: {str(e)}", "error")
        return []

@app.route('/download/<path:key>')
def download_file(key):
    #import requests
    original_name = key.split('_', 1)[-1]
    response = requests.get(f"{S3_URL}/{key}", stream=True)
    
    flask_response = flask.Response(
        response.iter_content(chunk_size=8192),
        content_type=response.headers['Content-Type']
    )
    flask_response.headers['Content-Disposition'] = f'attachment; filename="{original_name}"'
    return flask_response

@app.route('/')
def index():
    files = list_files_from_s3()  # Your existing function
    return render_template('index.html', files=files, s3_url=S3_URL)

@app.route('/generate-upload-url', methods=['POST'])
def generate_upload_url():
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400
    
    data = request.get_json()
    filename = secure_filename(data.get('filename', ''))
    content_type = data.get('content_type', 'application/octet-stream')
    
    if not filename:
        return jsonify({"error": "Filename is required"}), 400
    
    unique_filename = f"{uuid.uuid4().hex}_{filename}"
    
    return jsonify({
        "upload_url": f"{S3_URL}/{unique_filename}",
        "file_url": f"{S3_URL}/{unique_filename}",
        "filename": unique_filename
    })

@app.route('/upload-success')
def upload_success():
    filename = request.args.get('filename', '')
    if filename:
        file_url = f"{S3_URL}/{filename}"
        flash(f'File uploaded successfully! <a href="{file_url}" target="_blank">View file</a>', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)