from flask import Flask, request, render_template
import fitz
from werkzeug.utils import secure_filename
import os
from location.FE.Both.both_rects import (
    sem1_rects1, sem1_rects2, sem1_rects3, sem1_rects4, sem1_rects5, sem1_rects6, 
    sem1_rects7, sem1_rects8, sem1_rects9, sem1_rects10, sem1_rects11, sem1_rects12, 
    sem1_rects13, sem2_rects1, sem2_rects2, sem2_rects3, sem2_rects4, sem2_rects5, 
    sem2_rects6, sem2_rects7, sem2_rects8, sem2_rects9, sem2_rects10, sem2_rects11, 
    sem2_rects12, sem2_rects13, sem2_rects14, sem2_rects15
)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
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

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            doc = fitz.open(file_path)
            page = doc.load_page(0)

            # For sem1_subjects (Semester 1)
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
                    points=points_text  # Store as text for grace check
                )
                sem1_subjects.append(subject)

            # For sem2_subjects (Semester 2)
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
                    points=points_text  # Store as text for grace check
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

            # Check for grace marks and backlogs
            def check_grace_marks(subjects):
                grace_count = sum(1 for subject in subjects if '#' in subject.points)
                return grace_count

            def check_backlogs(subjects):
                backlog_count = sum(1 for subject in subjects if 'F' in subject.grade)
                return backlog_count

            grace_marks_sem1 = check_grace_marks(sem1_subjects)
            grace_marks_sem2 = check_grace_marks(sem2_subjects)
            backlogs_sem1 = check_backlogs(sem1_subjects)
            backlogs_sem2 = check_backlogs(sem2_subjects)

            # Calculate totals
            total_sem1_credits = sum(subject.credits for subject in sem1_subjects)
            total_sem1_earned = sum(subject.earned for subject in sem1_subjects)
            total_sem1_points = sum(parse_int(subject.points) for subject in sem1_subjects)
            total_sem2_credits = sum(subject.credits for subject in sem2_subjects)
            total_sem2_earned = sum(subject.earned for subject in sem2_subjects)
            total_sem2_points = sum(parse_int(subject.points) for subject in sem2_subjects)

            doc.close()

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
