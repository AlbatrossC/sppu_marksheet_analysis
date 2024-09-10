import fitz
from rects import rects1, rects2, rects3, rects4, rects5, rects6, rects7, rects8, rects9, rects10, rects11, rects12, rects13

class Subject:
    def __init__(self, code, name, credits='', earned='', grade='', grade_point='', points=''):
        self.code = code
        self.name = name
        self.credits = credits
        self.earned = earned
        self.grade = grade
        self.grade_point = grade_point
        self.points = points

    def __repr__(self):
        return (
            f"Subject(\n"
            f"code={self.code}, \n"
            f"name={self.name}, \n"
            f"credits={self.credits if self.credits else 'N/A'}, \n"
            f"earned={self.earned if self.earned else 'N/A'}, \n"
            f"grade={self.grade if self.grade else 'N/A'}, \n"
            f"grade_point={self.grade_point if self.grade_point else 'N/A'}, \n"
            f"points={self.points if self.points else 'N/A'}\n"
            f")"
        )

# Open the PDF file
pdf_path="F.E Sem1 Marksheet.pdf"
doc = fitz.open(pdf_path)
page = doc.load_page(0)  # Load the first page


# Function to extract text from a rectangle
def extract_text(rect):
    try:
        return page.get_text("text", clip=rect).strip()
    except Exception as e:
        print(f"Error extracting text: {e}")
        return ''

# List to hold all subjects
subjects = []

# Extract data for each subject using a loop
for i in range(1, 13):
    rect = globals().get(f"rects{i}", {})
    subject = Subject(
        code=extract_text(rect.get(f"code{i}", '')),
        name=extract_text(rect.get(f"name{i}", '')),
        credits=extract_text(rect.get(f"crd{i}", '')),
        earned=extract_text(rect.get(f"earned{i}", '')),
        grade=extract_text(rect.get(f"grd{i}", '')),
        grade_point=extract_text(rect.get(f"gp{i}", '')),
        points=extract_text(rect.get(f"pnt{i}", ''))
    )
    subjects.append(subject)

class AdditionalInfo:
    def __init__(self, SGPA, cred_earned, total_cred, total_credit_pt):
        self.SGPA = SGPA
        self.cred_earned = cred_earned
        self.total_cred = total_cred
        self.total_credit_pt = total_credit_pt

# Extracting data from rects13
info = AdditionalInfo(
    SGPA=extract_text(rects13.get("SGPA", '')),
    cred_earned=extract_text(rects13.get("cred_earned", '')),
    total_cred=extract_text(rects13.get("total_cred", '')),
    total_credit_pt=extract_text(rects13.get("total_credit_pt", ''))
)

# Print AdditionalInfo instance and subject grades
print(info.__dict__)

for subject in subjects:
    print(subject)
