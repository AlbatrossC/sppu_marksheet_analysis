from flask import Flask, request, render_template
import fitz
from werkzeug.utils import secure_filename
import os

# Import rectangles from rects.py
from location.FE.SEM1.sem1_rects import rects1, rects2, rects3, rects4, rects5, rects6, rects7, rects8, rects9, rects10, rects11, rects12, rects13

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
            return 0.0

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
            return 0.0

def extract_text(page, rect):
    try:
        return page.get_text("text", clip=rect).strip()
    except Exception as e:
        print(f"Error extracting text: {e}")
        return ''

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

            return render_template('test.html', info=info, subjects=subjects)

    return render_template('upload.html')

if __name__ == '__main__':
    app.run(debug=True)
