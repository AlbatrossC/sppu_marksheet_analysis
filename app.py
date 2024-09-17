from flask import Flask, request, render_template
import os
from FE.fe_sem1 import upload_file as sem1_upload
from FE.fe_sem2 import upload_file as sem2_upload
from FE.fe_sem1_sem2 import upload_file as sem1_sem2_upload  # Import for SEM1 & SEM2 combined

app = Flask(__name__)

# Use /tmp directory on Vercel for uploads
app.config['UPLOAD_FOLDER'] = '/tmp/uploads'
app.config['ALLOWED_EXTENSIONS'] = {'pdf'}

# Create upload folder in /tmp if it doesn't exist
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Route for selecting semester
@app.route('/')
def home():
    return render_template('index.html')  # Create a simple home page to select SEM1, SEM2, or SEM1 & SEM2

# Route to handle SEM1 PDF processing
@app.route('/sem1', methods=['GET', 'POST'])
def run_sem1():
    if request.method == 'POST':
        return sem1_upload()  # Call the function from fe_sem1.py
    return render_template('FE/upload_sem1.html')

# Route to handle SEM2 PDF processing
@app.route('/sem2', methods=['GET', 'POST'])
def run_sem2():
    if request.method == 'POST':
        return sem2_upload()  # Call the function from fe_sem2.py
    return render_template('FE/upload_sem2.html')

# Route to handle SEM1 & SEM2 combined PDF processing
@app.route('/fe_sem1_sem2', methods=['GET', 'POST'])
def run_sem1_sem2():
    if request.method == 'POST':
        return sem1_sem2_upload()  # Call the function from fe_sem1_sem2.py
    return render_template('FE/upload_sem1_sem2.html')  # The HTML form for SEM1 & SEM2 combined upload

if __name__ == '__main__':
    app.run(debug=True)
