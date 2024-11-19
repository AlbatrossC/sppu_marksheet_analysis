from flask import Flask, render_template, send_from_directory
from FE.fe_sem1 import upload_file as sem1_upload
from FE.fe_sem1_sem2 import upload_file as sem1_sem2_upload
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)


#Home page
@app.route('/')
def home():
    return render_template('index.html')

#FE:Sem1 page
@app.route('/sem1', methods=['GET', 'POST'])
def run_sem1():
    app.logger.debug('Accessing /sem1 route')
    return sem1_upload()

#FE:sem2 page 
@app.route('/fe_sem1_sem2', methods=['GET', 'POST'])
def run_sem1_sem2():
    app.logger.debug('Accessing /fe_sem1_sem2 route')
    return sem1_sem2_upload()

@app.route('/error')
def error():
    return render_template('error.html')

if __name__ == '__main__':
    app.run(debug=True)