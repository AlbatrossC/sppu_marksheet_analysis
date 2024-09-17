from flask import request, render_template, redirect, url_for
import fitz  # PyMuPDF for PDF handling
from werkzeug.utils import secure_filename
import os

# Import rectangles from rects.py (these need to exist in your project)
from location.FE.SEM1.sem1_rects import rects1, rects2, rects3, rects4, rects5, rects6, rects7, rects8, rects9, rects10, rects11, rects12, rects13

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
        self.points = points

    @staticmethod
    def convert_to_int(value):
        try:
            return int(value)
        except ValueError:
            return 0

    def grade_to_points(self):
        return self.GRADE_POINTS.get(self.grade, 0)  # Default to 0 if grade is not found

    def grade_credits_product(self):
        return self.grade_to_points() * self.credits

# Class for additional information (like SGPA)
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
        if '#' in str(subject.points):  # Checking for the '#' symbol in points
            grace_count += 1
    return grace_count

# Function to calculate the total earned credits
def calculate_total_earned_credits(subjects):
    total_earned_credits = sum(subject.earned for subject in subjects)
    return total_earned_credits

# Function to calculate the total Grade × Credits Earned


# Main function to handle file uploads for Semester 1
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(file_path)

            doc = fitz.open(file_path)
            page = doc.load_page(0)

            subjects = []
            for i in range(1, 13):  # Assuming you have 12 subjects
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

            backlogs = count_backlogs(subjects)
            backlog_message = f"You have {backlogs} backlogs" if backlogs > 0 else "You have 0 backlogs"

            grace_count = count_grace_marks(subjects)
            grace_message = f"You have given grace marks in {grace_count} subjects."

            total_earned_credits = calculate_total_earned_credits(subjects)

            return render_template('FE/results.html', info=info, subjects=subjects, backlog_message=backlog_message, grace_message=grace_message, total_earned_credits=total_earned_credits)

    return render_template('upload_sem1.html')
