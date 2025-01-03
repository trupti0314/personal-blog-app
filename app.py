import boto3
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os
 
# AWS S3 Configuration
s3 = boto3.client('s3')
bucket_name = "blog-image-buckets "  # Replace with your S3 bucket name
 
app = Flask(__name__)
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}  # Allowed file extensions
 
# Check if file extension is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']
 
@app.route('/')
def home():
    return render_template('index.html')
 
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
 
        # Upload to S3
        try:
            s3.upload_file(
                os.path.join(app.config['UPLOAD_FOLDER'], filename),
                bucket_name,
                f"images/{filename}"
            )
image_url = f"https://{bucket_name}.s3.amazonaws.com/images/{filename}"
            return f"File uploaded successfully! <a href='{image_url}'>View Image</a>"
        except Exception as e:
            return f"Error uploading file: {str(e)}"
    return "Invalid file format or no file selected."
 
if __name__ == "__main__":
app.run(debug=True, host="0.0.0.0", port=5000)
