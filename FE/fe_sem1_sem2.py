from flask import Flask, request, render_template, send_file
import fitz
from werkzeug.utils import secure_filename
import os
import requests
from location.FE.Both.both_rects import (
    sem1_rects1, sem1_rects2, sem1_rects3, sem1_rects4, sem1_rects5, sem1_rects6, 
    sem1_rects7, sem1_rects8, sem1_rects9, sem1_rects10, sem1_rects11, sem1_rects12, 
    sem1_rects13, sem2_rects1, sem2_rects2, sem2_rects3, sem2_rects4, sem2_rects5, 
    sem2_rects6, sem2_rects7, sem2_rects8, sem2_rects9, sem2_rects10, sem2_rects11, 
    sem2_rects12, sem2_rects13, sem2_rects14, sem2_rects15
)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = '/tmp/uploads'  
app.config['ALLOWED_EXTENSIONS'] = {'pdf'}

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

class Subject:
    def __init__(self, code, name, credits='', earned='', grade='', grade_point='', points=''):
        self.code = code
        self.name = name
        self.credits = credits
        self.earned = earned
        self.grade = grade
        self.grade_point = grade_point
        self.points = points

class AdditionalInfo:
    def __init__(self, SGPA='', cred_earned='', total_cred='', total_credit_pt=''):
        self.SGPA = SGPA
        self.cred_earned = cred_earned
        self.total_cred = total_cred
        self.total_credit_pt = total_credit_pt

def extract_text(page, rect):
    try:
        return page.get_text("text", clip=rect).strip()
    except Exception as e:
        print(f"Error extracting text: {e}")
        return ''

def parse_int(value):
    try:
        return int(value)
    except ValueError:
        return 0

def download_pdf(url, payload, student_name):
    retry_count = 3
    for _ in range(retry_count):
        try:
            with requests.Session() as session:
                response = session.post(url, data=payload, verify=False, timeout=10)
                response.raise_for_status()
                pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], f'{student_name}.pdf')
                with open(pdf_path, 'wb') as f:
                    f.write(response.content)
                return pdf_path
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}, retrying...")
            continue
    return None

def process_pdf(file_path):
    doc = fitz.open(file_path)
    page = doc.load_page(0)

    # Process Semester 1
    sem1_subjects = []
    for i in range(1, 13):
        rect = globals().get(f"sem1_rects{i}", {})
        points_text = extract_text(page, rect.get(f"pnt{i}", {}))
        
        subject = Subject(
            code=extract_text(page, rect.get(f"code{i}", {})),
            name=extract_text(page, rect.get(f"name{i}", {})),
            credits=parse_int(extract_text(page, rect.get(f"crd{i}", {}))),
            earned=parse_int(extract_text(page, rect.get(f"earned{i}", {}))),
            grade=extract_text(page, rect.get(f"grd{i}", {})),
            grade_point=parse_int(extract_text(page, rect.get(f"gp{i}", {}))),
            points=points_text
        )
        sem1_subjects.append(subject)

    # Process Semester 2
    sem2_subjects = []
    for i in range(1, 15):
        rect = globals().get(f"sem2_rects{i}", {})
        points_text = extract_text(page, rect.get(f"pnt{i}", {}))
        
        subject = Subject(
            code=extract_text(page, rect.get(f"code{i}", {})),
            name=extract_text(page, rect.get(f"name{i}", {})),
            credits=parse_int(extract_text(page, rect.get(f"crd{i}", {}))),
            earned=parse_int(extract_text(page, rect.get(f"earned{i}", {}))),
            grade=extract_text(page, rect.get(f"grd{i}", {})),
            grade_point=parse_int(extract_text(page, rect.get(f"gp{i}", {}))),
            points=points_text
        )
        sem2_subjects.append(subject)

    # Additional info for Semester 1
    info_sem1 = AdditionalInfo(
        SGPA=extract_text(page, sem1_rects13.get("SGPA", {})),
        cred_earned=parse_int(extract_text(page, sem1_rects13.get("cred_earned", {}))),
        total_cred=parse_int(extract_text(page, sem1_rects13.get("total_cred", {}))),
        total_credit_pt=parse_int(extract_text(page, sem1_rects13.get("total_credit_pt", {})))
    )

    # Additional info for Semester 2
    info_sem2 = AdditionalInfo(
        SGPA=extract_text(page, sem2_rects15.get("SGPA", {})),
        cred_earned=parse_int(extract_text(page, sem2_rects15.get("cred_earned", {}))),
        total_cred=parse_int(extract_text(page, sem2_rects15.get("total_cred", {}))),
        total_credit_pt=parse_int(extract_text(page, sem2_rects15.get("total_credit_pt", {})))
    )

    doc.close()

    return sem1_subjects, sem2_subjects, info_sem1, info_sem2

@app.route('/fe_sem1_sem2', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' in request.files:
            file = request.files['file']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
        else:
            seat_no = request.form['seat_no']
            mother_name = request.form['mother_name']
            student_name = f"result_{seat_no}"

            url = 'https://onlineresults.unipune.ac.in/Result/Dashboard/ViewResult1'
            payload = {
                'PatternID': '6Qw72CLlcXSacHyT9a7RkQ==',  # Example June 2024
                'PatternName': 'RP+zm4rXwFDLUrTpUWU4sEa3GhqzYZU+2WOHorilLYgi2RQ6OKyRcE4pLb5zFaQ9',
                'SeatNo': seat_no,
                'MotherName': mother_name
            }

            file_path = download_pdf(url, payload, student_name)
            if not file_path:
                return "Failed to fetch the marksheet", 400

        sem1_subjects, sem2_subjects, info_sem1, info_sem2 = process_pdf(file_path)

        # Calculate totals and other metrics
        total_sem1_credits = sum(subject.credits for subject in sem1_subjects)
        total_sem1_earned = sum(subject.earned for subject in sem1_subjects)
        total_sem1_points = sum(parse_int(subject.points) for subject in sem1_subjects)
        total_sem2_credits = sum(subject.credits for subject in sem2_subjects)
        total_sem2_earned = sum(subject.earned for subject in sem2_subjects)
        total_sem2_points = sum(parse_int(subject.points) for subject in sem2_subjects)

        grace_marks_sem1 = sum(1 for subject in sem1_subjects if '#' in subject.points)
        grace_marks_sem2 = sum(1 for subject in sem2_subjects if '#' in subject.points)
        backlogs_sem1 = sum(1 for subject in sem1_subjects if 'F' in subject.grade)
        backlogs_sem2 = sum(1 for subject in sem2_subjects if 'F' in subject.grade)

        return render_template(
            'FE/both_results.html', 
            info_sem1=info_sem1, 
            info_sem2=info_sem2, 
            sem1_subjects=sem1_subjects, 
            sem2_subjects=sem2_subjects,
            total_sem1_credits=total_sem1_credits, 
            total_sem1_earned=total_sem1_earned, 
            total_sem1_points=total_sem1_points,
            total_sem2_credits=total_sem2_credits, 
            total_sem2_earned=total_sem2_earned, 
            total_sem2_points=total_sem2_points,
            grace_marks_sem1=grace_marks_sem1, 
            grace_marks_sem2=grace_marks_sem2,
            backlogs_sem1=backlogs_sem1, 
            backlogs_sem2=backlogs_sem2
        )

    return render_template('FE/upload_sem1_sem2.html')

if __name__ == '__main__':
    app.run(debug=True)
