from flask import Flask, render_template
from FE.fe_sem1 import upload_file as sem1_upload
from FE.fe_sem1_sem2 import upload_file as sem1_sem2_upload
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/sem1', methods=['GET', 'POST'])
def run_sem1():
    app.logger.debug('Accessing /sem1 route')
    return sem1_upload()

@app.route('/fe_sem1_sem2', methods=['GET', 'POST'])
def run_sem1_sem2():
    app.logger.debug('Accessing /fe_sem1_sem2 route')
    return sem1_sem2_upload()

if __name__ == '__main__':
    app.run(debug=True)