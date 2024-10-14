from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.utils import secure_filename
from azure.storage.blob import BlobServiceClient

import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Needed for sessions


account_url = "https://myflaskwebappstorage.blob.core.windows.net/"
sas_token = "sv=2022-11-02&ss=bfqt&srt=sco&sp=rwdlacupiytfx&se=2024-10-17T07:48:24Z&st=2024-10-13T23:48:24Z&spr=https&sig=5QXXaTrWGsVmwyJ9Y%2B8SkY2jQbymPNt%2FCjWqErTOMdY%3D"
blob_service_client = BlobServiceClient(account_url=account_url, credential=sas_token)

# Set upload folder and allowed file extensions
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif', 'txt', 'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']
    
# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
print("Upload folder created or already exists:", app.config['UPLOAD_FOLDER'])

@app.route('/')
def index():
    print("Accessing index page")
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        print(f"Login attempt by user: {username}")
        # Simple authentication (replace with a real user database check)
        if username == 'admin' and password == 'password':
            session['user'] = username
            print(f"User {username} logged in successfully")
            return redirect(url_for('index'))
            print(f"Invalid login attempt for user: {username}")
        return 'Invalid credentials'
        print("Rendering login page")
    return render_template('login.html')

@app.route('/data', methods=['GET', 'POST'])
def data():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        print(f"Received data - Name: {name}, Email: {email}")
        return f"Name: {name}, Email: {email}"
        print("Rendering data input page")
    return render_template('data.html')



@app.route('/upload', methods=['GET', 'POST'])
def upload():
   if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)  # Secure the file name
            print(f"File {file.filename} received for upload")
            try:
                # Define the container name
                container_name = 'uploads'
                
                # Create a container client for the specified container
                container_client = blob_service_client.get_container_client(container_name)
                
                # Check if the container exists by trying to get its properties
                try:
                    container_client.get_container_properties()  # This will raise an exception if the container does not exist
                    print(f"Container '{container_name}' exists.")
                except Exception as e:  # Catch the exception if the container does not exist
                    # Create the container if it doesn't exist
                    container_client.create_container()
                    print(f"Container '{container_name}' created.")

                # Now that the container exists, upload the blob
                blob_client = blob_service_client.get_blob_client(container=container_name, blob=filename)
                blob_client.upload_blob(file, overwrite=True)  # Use overwrite=True to replace existing blobs
                print(f"File {file.filename} uploaded successfully to Azure Blob Storage")
                return f"File {file.filename} uploaded successfully to Azure Blob Storage"
            except Exception as e:
                print(f"An error occurred while uploading: {str(e)}")  # Log any errors during upload
                return f"An error occurred while uploading: {str(e)}"
        else:
            print(f"File upload failed: {file.filename} not allowed")  # Log if the file is not allowed
            return 'File not allowed'
    
    print("Rendering upload page")  # Log that the upload page is being rendered
    return render_template('upload.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)