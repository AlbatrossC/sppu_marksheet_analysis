from flask import Flask, request, render_template
import fitz
from werkzeug.utils import secure_filename
import os
import requests
from location.FE.SEM1.sem1_rects import rects1, rects2, rects3, rects4, rects5, rects6, rects7, rects8, rects9, rects10, rects11, rects12, rects13

app = Flask(__name__)

UPLOAD_FOLDER = '/tmp/uploads'
ALLOWED_EXTENSIONS = {'pdf'}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

class Subject:
    def __init__(self, code, name, credits='', earned='', grade='', grade_point='', points=''):
        self.code = code
        self.name = name
        self.credits = self.convert_to_int(credits)
        self.earned = self.convert_to_int(earned)
        self.grade = grade
        self.grade_point = self.convert_to_int(grade_point)
        self.points = points

    @staticmethod
    def convert_to_int(value):
        try:
            return int(value)
        except ValueError:
            return 0

class AdditionalInfo:
    def __init__(self, SGPA='', cred_earned='', total_cred='', total_credit_pt=''):
        self.SGPA = SGPA
        self.cred_earned = self.convert_to_int(cred_earned)
        self.total_cred = self.convert_to_int(total_cred)
        self.total_credit_pt = self.convert_to_int(total_credit_pt)

    @staticmethod
    def convert_to_int(value):
        try:
            return int(value)
        except ValueError:
            return 0

def extract_text(page, rect):
    try:
        return page.get_text("text", clip=rect).strip()
    except Exception as e:
        print(f"Error extracting text: {e}")
        return ''

def count_backlogs(subjects):
    return sum(1 for subject in subjects if subject.grade == 'F')

def count_grace_marks(subjects):
    return sum(1 for subject in subjects if '#' in str(subject.points))

def calculate_total_earned_credits(subjects):
    return sum(subject.earned for subject in subjects)

def download_pdf(url, payload, student_name):
    retry_count = 3
    for _ in range(retry_count):
        try:
            with requests.Session() as session:
                response = session.post(url, data=payload, verify=False, timeout=10)
                response.raise_for_status()
                pdf_path = os.path.join(UPLOAD_FOLDER, f'{student_name}.pdf')
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

    subjects = []
    for i in range(1, 13):
        rect = globals().get(f"rects{i}", {})
        subject = Subject(
            code=extract_text(page, rect.get(f"code{i}", {})),
            name=extract_text(page, rect.get(f"name{i}", {})),
            credits=extract_text(page, rect.get(f"crd{i}", {})),
            earned=extract_text(page, rect.get(f"earned{i}", {})),
            grade=extract_text(page, rect.get(f"grd{i}", {})),
            grade_point=extract_text(page, rect.get(f"gp{i}", {})),
            points=extract_text(page, rect.get(f"pnt{i}", {}))
        )
        subjects.append(subject)

    info_rect = rects13
    info = AdditionalInfo(
        SGPA=extract_text(page, info_rect.get("SGPA", {})),
        cred_earned=extract_text(page, info_rect.get("cred_earned", {})),
        total_cred=extract_text(page, info_rect.get("total_cred", {})),
        total_credit_pt=extract_text(page, info_rect.get("total_credit_pt", {}))
    )

    doc.close()

    return subjects, info

def upload_file():
    if request.method == 'POST':
        try:
            if 'file' in request.files:
                file = request.files['file']
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file_path = os.path.join(UPLOAD_FOLDER, filename)
                    file.save(file_path)
            else:
                seat_no = request.form['seat_no']
                mother_name = request.form['mother_name']
                student_name = f"result_{seat_no}"

                url = 'https://onlineresults.unipune.ac.in/Result/Dashboard/ViewResult1'
                payload = {
                    'PatternID': '6Qw72CLlcXSacHyT9a7RkQ==',
                    'PatternName': 'RP+zm4rXwFDLUrTpUWU4sEa3GhqzYZU+2WOHorilLYgi2RQ6OKyRcE4pLb5zFaQ9',
                    'SeatNo': seat_no,
                    'MotherName': mother_name
                }

                file_path = download_pdf(url, payload, student_name)
                if not file_path:
                    return render_template('error.html'), 500

            subjects, info = process_pdf(file_path)

            backlogs = count_backlogs(subjects)
            backlog_message = f"You have {backlogs} backlogs" if backlogs > 0 else "You have 0 backlogs"

            grace_count = count_grace_marks(subjects)
            grace_message = f"You have given grace marks in {grace_count} subjects. Grace marks are awarded to help you pass subjects with marginally lower scores."

            total_earned_credits = calculate_total_earned_credits(subjects)

            return render_template('FE/results.html', info=info, subjects=subjects, backlog_message=backlog_message, grace_message=grace_message, total_earned_credits=total_earned_credits)
        except Exception as e:
            print(f"Error: {e}")
            return render_template('error.html'), 500

    return render_template('FE/upload_sem1.html')