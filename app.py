from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.utils import secure_filename
from azure.storage.blob import BlobServiceClient

import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Needed for sessions


account_url = "https://myflaskwebappstorage.blob.core.windows.net/"
sas_token = "sv=2022-11-02&ss=bfqt&srt=sco&sp=rwdlacupiytfx&se=2024-10-17T07:48:24Z&st=2024-10-13T23:48:24Z&spr=https&sig=5QXXaTrWGsVmwyJ9Y%2B8SkY2jQbymPNt%2FCjWqErTOMdY%3D"
blob_service_client = BlobServiceClient(account_url=account_url, credential=sas_token)




@app.route('/')
def index():
    return render_template('index.html')

# Set upload folder and allowed file extensions
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif', 'txt', 'pdf'}

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Simple authentication (replace with a real user database check)
        if username == 'admin' and password == 'password':
            session['user'] = username
            return redirect(url_for('index'))
        return 'Invalid credentials'
    return render_template('login.html')

@app.route('/data', methods=['GET', 'POST'])
def data():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        return f"Name: {name}, Email: {email}"
    return render_template('data.html')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return f"File {filename} uploaded successfully"
        return 'File not allowed'
    return render_template('upload.html')


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            # Create a blob client using the container and filename
            blob_client = blob_service_client.get_blob_client(container='uploads', blob=file.filename)
            blob_client.upload_blob(file, overwrite=True)  # Use overwrite=True to replace existing blobs
            return f"File {file.filename} uploaded successfully to Azure Blob Storage"
        return 'File not allowed'
    return render_template('upload.html')
