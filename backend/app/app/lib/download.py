import cv2
import pandas as pd
import numpy as np
from typing import List


def justify_text(text, width: int = 90):
    words = ". ".join(text.split(".")[:2])
    words = words.split()
    lines, current_line = [], ""
    for word in words:
        if len(current_line + word) + 1 <= width:
            current_line += word + " "
        else:
            lines.append(current_line.rstrip())
            current_line = word + " "
    if current_line:
        lines.append(current_line.rstrip())
    return lines


def add_text(
    image: np.ndarray,
    lines: List[str],
    lx: int = 50,
    ly: int = 50,
    height: int = 40,
    font: int = cv2.FONT_HERSHEY_SIMPLEX,
    f_size: float = 0.8,
):
    for line in lines:
        cv2.putText(image, line, (lx, ly), font, f_size, (0, 0, 0), lineType=cv2.LINE_AA)
        ly += height
    return image, ly

def download_exceled(
    applications,
    path: str,
):
    cols = ["Name", "Email", "Phone", "Education", "Skills", "Certification", "Candidate Review", "Note for Consideration", "Recommendation", "Decision"]
    data = []
    for app in applications:
        print("APP", app.records.keys())
        data.append(
            [
                app.records["name"],
                app.records.get("email", "Not provided"),
                app.records.get("phone", "Not provided"),
                ", ".join(app.records["education"]) if isinstance(app.records["education"], list) else app.records["education"],
                ", ".join(app.records["skills"]) if isinstance(app.records["skills"], list) else app.records["skills"],
                ", ".join(app.records["certification"]) if isinstance(app.records["certification"], list) else app.records["certification"],
                app.records["candidate_review"],
                app.records["note_for_consideration"],
                app.records["recommendation"],
                app.records["decision"],
            ]
        ) 
    df = pd.DataFrame(data, columns=cols)
    excel_path = f"{path}/records.xlsx"
    df.to_excel(excel_path, index=False)
    return excel_path
    # data = [
    #     records["name"],
    #     records["email"],
    #     records["phone"],
    #     ", ".join(records["education"]) if isinstance(records["education"], list) else records["education"],
    #     ", ".join(records["skills"]) if isinstance(records["skills"], list) else records["skills"],
    #     ", ".join(records["certification"]) if isinstance(records["certification"], list) else records["certification"],
    #     records["candidate_review"],
    #     records["note_for_consideration"],
    #     records["recommendation"],
    #     records["decision"],
    # ]
    # excel_path = f"{path}/records.xlsx"
    # df = pd.DataFrame([data], columns=cols)
    # df.to_excel(excel_path, index=False)
    # return excel_path


def download_pdf(
    records,
    template: str = "/app/app/lib/images/sorci.png",
    bg: str = "/app/app/lib/images/bg.png",
    info: str = "/app/app/lib/images/info.png",
):

    image = cv2.imread(template)
    image, ly = add_text(image, ["NAME: " + records['name']], lx=40, ly=60, height=25, font=cv2.FONT_HERSHEY_TRIPLEX)
    image, ly = add_text(image, ["EMAIL: " + records['email']], lx=40, ly=ly + 10, height=25, font=cv2.FONT_HERSHEY_TRIPLEX)
    image, ly = add_text(image, ["PHONE: " + records['phone']], lx=40, ly=ly + 10, height=25, font=cv2.FONT_HERSHEY_TRIPLEX)

    image, ly = add_text(image, ["CANDIDATE REVIEW"], lx=40, ly=ly + 30, height=10, font=cv2.FONT_HERSHEY_TRIPLEX, f_size=1)
    image, ly = add_text(image, justify_text(records['candidate_review'], 87), lx=40, ly=ly + 20, height=20, font=cv2.FONT_HERSHEY_SIMPLEX, f_size=0.5)

    image, ly = add_text(image, ["NOTES FOR CONSIDERATION"], lx=40, ly=ly + 30, height=10, font=cv2.FONT_HERSHEY_TRIPLEX, f_size=1)
    image, ly = add_text(image, justify_text(records['note_for_consideration'], 87), lx=40, ly=ly + 20, height=20, font=cv2.FONT_HERSHEY_SIMPLEX, f_size=0.5)

    lyt = ly
    image, ly = add_text(image, ["SKILL MATCHING"], lx=40, ly=ly + 30, height=10, font=cv2.FONT_HERSHEY_TRIPLEX, f_size=0.75)
    image, ly = add_text(image, ["JOB DESCRIPTION"], lx=40, ly=ly + 20, height=10, font=cv2.FONT_HERSHEY_TRIPLEX, f_size=0.75)

    skills = records['skills']
    skills = skills[:len(skills) if len(skills) < 5 else 5]
    for skill in skills:
        image, ly = add_text(image, justify_text("- " + skill, 30), lx=40, ly=ly + 20, height=20, font=cv2.FONT_HERSHEY_SIMPLEX, f_size=0.5)

    image, ly = add_text(image, ["RELEVANT CERTIFICATIONS"], lx=40, ly=ly + 30, height=10, font=cv2.FONT_HERSHEY_TRIPLEX, f_size=0.75)
    certs = records['certification']
    certs = certs[:len(certs) if len(certs) < 5 else 5]
    for cert in certs:
        image, ly = add_text(image, justify_text("- " + cert, 300), lx=40, ly=ly + 20, height=20, font=cv2.FONT_HERSHEY_SIMPLEX, f_size=0.5)

    image, ly = add_text(image, ["EDUCATION"], lx=400, ly=lyt + 30, height=10, font=cv2.FONT_HERSHEY_TRIPLEX, f_size=0.75)
    for edu in records['education']:
        image, ly = add_text(image, justify_text(edu, 50), lx=400, ly=ly + 20, height=10, font=cv2.FONT_HERSHEY_SIMPLEX, f_size=0.5)

    image, ly = add_text(image, ["RECOMMENDATION"], lx=400, ly=ly + 40, height=10, font=cv2.FONT_HERSHEY_TRIPLEX, f_size=0.75)
    image, ly = add_text(image, justify_text(records['recommendation'], 50), lx=400, ly=ly + 20, height=20, font=cv2.FONT_HERSHEY_SIMPLEX, f_size=0.5)

    image, ly = add_text(image, ["Next steps:"], lx=400, ly=ly + 40, height=10, font=cv2.FONT_HERSHEY_TRIPLEX, f_size=0.75)
    image, ly = add_text(image, justify_text(records['decision'], 50), lx=400, ly=ly + 20, height=20, font=cv2.FONT_HERSHEY_SIMPLEX, f_size=0.5)
    return image

if __name__ == "__main__":
    image = download_pdf(
        {
            "name": "Alice Clark",
            "email": "alice@gmail.com",
            "phone": "1234567890",
            "education": ["Indian Institute of Technology - Mumbai"],
            "skills": [
                "Machine Learning",
                "Natural Language Processing (NLP) and Text Mining",
                "Big Data Handling",
                "Data analysis",
                "Database designing",
                "Microsoft Azure cloud services",
            ],
            "certification": [
                "Machine Learning",
                "Natural Language Processing",
                "Big Data Handling",
                "Data analysis",
                "Database designing",
                "Microsoft Azure cloud services",
            ],
            "candidate_review": "Alice Clark has over 20 years of experience in data handling, design, and development. She has worked with Microsoft Azure cloud services and has skills in Machine Learning, Natural Language Processing, and Big Data Handling. However, her resume does not mention any experience in image/video classification and recognition, image segmentation, object detection, OCR, graph neural networks, multimodal, unsupervised and self-supervised learning, etc.",
            "note_for_consideration": "Alice has worked as a Software Engineer at Microsoft. She has experience in data warehousing and business intelligence. She has also worked on Microsoft Azure cloud services like Document DB, SQL Azure, Stream Analytics, Event hub, Power BI, Web Job, Web App, Power BI, Azure data lake analytics (U-SQL).",
            "recommendation": "Alice seems to be adaptable as she has worked on various technologies and platforms. She is also willing to relocate anywhere.",
            "decision": "Alice Clark seems to be a strong candidate with extensive experience and a wide range of skills. However, she might need to learn and adapt to some specific technologies and areas mentioned in the job description. Her adaptability and willingness to learn can be a plus point.",
        }
    )
    cv2.imwrite("sample.png", image)
