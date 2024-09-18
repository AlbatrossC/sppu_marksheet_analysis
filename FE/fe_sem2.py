from flask import Flask, request, render_template, send_file
import fitz  # PyMuPDF for PDF handling
from werkzeug.utils import secure_filename
import os
import requests

# Import rectangles from rects.py for SEM2
from location.FE.SEM2.sem2_rects import rects1, rects2, rects3, rects4, rects5, rects6, rects7, rects8, rects9, rects10, rects11, rects12, rects13, rects14, rects15

app = Flask(__name__)

# Use /tmp directory on Vercel for uploads
UPLOAD_FOLDER = '/tmp/uploads'
ALLOWED_EXTENSIONS = {'pdf'}

# Ensure the upload folder exists in /tmp
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Function to check if the file is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Class for holding subject data
class Subject:
    def __init__(self, code, name, credits='', earned='', grade='', grade_point='', points=''):
        self.code = code
        self.name = name
        self.credits = self.convert_to_int(credits)
        self.earned = self.convert_to_int(earned)
        self.grade = grade
        self.grade_point = self.convert_to_int(grade_point)
        self.points = points  # Keep points as is

    @staticmethod
    def convert_to_int(value):
        try:
            return int(value)
        except ValueError:
            return 0  # Return 0 if conversion fails

# Class for additional information (like SGPA)
class AdditionalInfo:
    def __init__(self, SGPA='', cred_earned='', total_cred='', total_credit_pt=''):
        self.SGPA = SGPA  # Keep SGPA as it is (string or float)
        self.cred_earned = self.convert_to_int(cred_earned)
        self.total_cred = self.convert_to_int(total_cred)
        self.total_credit_pt = self.convert_to_int(total_credit_pt)

    @staticmethod
    def convert_to_int(value):
        try:
            return int(value)
        except ValueError:
            return 0 # Return 0 if conversion fails

# Function to extract text from a rectangle on the PDF page
def extract_text(page, rect):
    try:
        return page.get_text("text", clip=rect).strip()
    except Exception as e:
        print(f"Error extracting text: {e}")
        return ''

# Function to count backlogs based on grades
def count_backlogs(subjects):
    return sum(1 for subject in subjects if subject.grade == 'F')

# Function to check if any subject has grace marks based on '#' symbol in points
def count_grace_marks(subjects):
    return sum(1 for subject in subjects if '#' in str(subject.points))

# Function to calculate the total earned credits
def calculate_total_earned_credits(subjects):
    return sum(subject.earned for subject in subjects)

# Function to download PDF
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

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        seat_no = request.form['seat_no']
        mother_name = request.form['mother_name']
        student_name = f"result_{seat_no}"  # You can modify how you want to name the PDF

        url = 'https://onlineresults.unipune.ac.in/Result/Dashboard/ViewResult1'
        payload = {
            'PatternID': '6Qw72CLlcXSacHyT9a7RkQ==',  # Example June 2024
            'PatternName': 'RP+zm4rXwFDLUrTpUWU4sEa3GhqzYZU+2WOHorilLYgi2RQ6OKyRcE4pLb5zFaQ9',
            'SeatNo': seat_no,
            'MotherName': mother_name
        }

        pdf_path = download_pdf(url, payload, student_name)

        if pdf_path:
            return send_file(pdf_path, as_attachment=True)
        else:
            return "Failed to download PDF", 400

    return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(file_path)

            # Open and process the PDF
            doc = fitz.open(file_path)
            page = doc.load_page(0)

            subjects = []
            for i in range(1, 15):  # Assuming you have 15 subjects for SEM2
                rect = globals().get(f"rects{i}", {})
                subject = Subject(
                    code=extract_text(page, rect.get(f"code{i}", {})),
                    name=extract_text(page, rect.get(f"name{i}", {})),
                    credits=extract_text(page, rect.get(f"crd{i}", {})),
                    earned=extract_text(page, rect.get(f"earned{i}", {})),
                    grade=extract_text(page, rect.get(f"grd{i}", {})),
                    grade_point=extract_text(page, rect.get(f"gp{i}", {})),
                    points=extract_text(page, rect.get(f"pnt{i}", {}))  # Keep points as is
                )
                subjects.append(subject)

            # Extract additional information like SGPA
            info_rect = rects15  # Assuming rects15 contains additional info
            info = AdditionalInfo(
                SGPA=extract_text(page, info_rect.get("SGPA", {})),
                cred_earned=extract_text(page, info_rect.get("cred_earned", {})),
                total_cred=extract_text(page, info_rect.get("total_cred", {})),
                total_credit_pt=extract_text(page, info_rect.get("total_credit_pt", {}))
            )

            doc.close()

            # Calculate the number of backlogs
            backlogs = count_backlogs(subjects)
            backlog_message = f"You have {backlogs} backlogs" if backlogs > 0 else "You have 0 backlogs"

            # Calculate the number of subjects with grace marks
            grace_count = count_grace_marks(subjects)
            grace_message = f"You have given grace marks in {grace_count} subjects. Grace marks are awarded to help you pass subjects with marginally lower scores."

            # Calculate the total earned credits
            total_earned_credits = calculate_total_earned_credits(subjects)

            # Render the result template and pass the subjects, additional info, backlog message, and grace message
            return render_template('FE/results.html', info=info, subjects=subjects, backlog_message=backlog_message, grace_message=grace_message, total_earned_credits=total_earned_credits)

    return render_template('upload_sem2.html')

@app.route('/sem2_fetch_and_process', methods=['POST'])
def fetch_and_process():
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

    pdf_path = download_pdf(url, payload, student_name)

    if pdf_path:
        # Process the downloaded PDF
        doc = fitz.open(pdf_path)
        page = doc.load_page(0)

        subjects = []
        for i in range(1, 15):  # Assuming you have 15 subjects for SEM2
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

        info_rect = rects15
        info = AdditionalInfo(
            SGPA=extract_text(page, info_rect.get("SGPA", {})),
            cred_earned=extract_text(page, info_rect.get("cred_earned", {})),
            total_cred=extract_text(page, info_rect.get("total_cred", {})),
            total_credit_pt=extract_text(page, info_rect.get("total_credit_pt", {}))
        )

        doc.close()

        backlogs = count_backlogs(subjects)
        backlog_message = f"You have {backlogs} backlogs" if backlogs > 0 else "You have 0 backlogs"

        grace_count = count_grace_marks(subjects)
        grace_message = f"You have given grace marks in {grace_count} subjects. Grace marks are awarded to help you pass subjects with marginally lower scores."

        total_earned_credits = calculate_total_earned_credits(subjects)

        return render_template('FE/results.html', info=info, subjects=subjects, backlog_message=backlog_message, grace_message=grace_message, total_earned_credits=total_earned_credits)
    else:
        return "Failed to fetch and process the marksheet", 400

if __name__ == '__main__':
    app.run(debug=True)