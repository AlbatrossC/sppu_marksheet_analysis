from flask import request, render_template
import fitz  # PyMuPDF for PDF handling
from werkzeug.utils import secure_filename
import os

# Import rectangles from rects.py for SEM2
from location.FE.SEM2.sem2_rects import rects1, rects2, rects3, rects4, rects5, rects6, rects7, rects8, rects9, rects10, rects11, rects12, rects13, rects14, rects15

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
        self.credits = self.convert_to_float(credits)
        self.earned = self.convert_to_float(earned)
        self.grade = grade
        self.grade_point = self.convert_to_float(grade_point)
        self.points = points

    @staticmethod
    def convert_to_float(value):
        try:
            return float(value)
        except ValueError:
            return ''  # Return blank if conversion fails

# Class for additional information (like SGPA)
class AdditionalInfo:
    def __init__(self, SGPA='', cred_earned='', total_cred='', total_credit_pt=''):
        self.SGPA = self.convert_to_float(SGPA)
        self.cred_earned = self.convert_to_float(cred_earned)
        self.total_cred = self.convert_to_float(total_cred)
        self.total_credit_pt = self.convert_to_float(total_credit_pt)

    @staticmethod
    def convert_to_float(value):
        try:
            return float(value)
        except ValueError:
            return ''  # Return blank if conversion fails

# Function to extract text from a rectangle on the PDF page
def extract_text(page, rect):
    try:
        return page.get_text("text", clip=rect).strip()
    except Exception as e:
        print(f"Error extracting text: {e}")
        return ''

# Function to count backlogs based on grades
def count_backlogs(subjects):
    backlogs = 0
    for subject in subjects:
        if subject.grade == 'F':  # Checking if grade is 'F'
            backlogs += 1
    return backlogs

# Function to check if any subject has grace marks based on '#' symbol in points
def count_grace_marks(subjects):
    grace_count = 0
    for subject in subjects:
        if '#' in subject.points:  # Checking for the '#' symbol in points
            grace_count += 1
    return grace_count

# Main function to handle file uploads for Semester 2
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
            for i in range(1, 16):  # Assuming you have 15 subjects for SEM2
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

            # Render the result template and pass the subjects, additional info, backlog message, and grace message
            return render_template('FE/results.html', info=info, subjects=subjects, backlog_message=backlog_message, grace_message=grace_message)

    return render_template('upload_sem2.html')
