import cv2
import numpy as np
from typing import List


def justify_text(text, width: int = 100):
    words = text.split()
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
    font: int = cv2.FONT_HERSHEY_SCRIPT_SIMPLEX,
):
    for line in lines:
        cv2.putText(image, line, (lx, ly), font, 0.8, (0, 0, 0), lineType=cv2.LINE_AA)
        ly += height
    return image, ly


def download_pdf(
    records,
    template: str = "/app/app/lib/images/sorci.png",
    bg: str = "/app/app/lib/images/bg.png",
    info: str = "/app/app/lib/images/info.png",
):

    image = cv2.imread(bg)
    template = cv2.imread(template)
    info = cv2.imread(info)

    info, ly = add_text(
        info,
        ["Name: " + records["name"]],
        lx=40,
        ly=40,
        height=10,
        font=cv2.FONT_HERSHEY_COMPLEX,
    )
    info, ly = add_text(
        info,
        ["Email: " + records["email"]],
        lx=40,
        ly=ly + 20,
        height=10,
        font=cv2.FONT_HERSHEY_COMPLEX,
    )
    info, ly = add_text(
        info,
        ["Phone: " + records["phone"]],
        lx=40,
        ly=ly + 20,
        height=10,
        font=cv2.FONT_HERSHEY_COMPLEX,
    )

    # Speculate
    image, ly = add_text(image, ["Speculate: "], lx=50, ly=50)
    image, ly = add_text(image, justify_text(records["speculate"]), lx=50, ly=ly + 20)

    # Explore
    image, ly = add_text(image, ["Explore: "], lx=50, ly=ly + 20)
    image, ly = add_text(image, justify_text(records["explore"]), lx=50, ly=ly + 20)

    # Adapt
    image, ly = add_text(image, ["Adapt: "], lx=50, ly=ly + 20)
    image, ly = add_text(image, justify_text(records["adapt"]), lx=50, ly=ly + 20)

    # Close
    image, ly = add_text(image, ["Close: "], lx=50, ly=ly + 20)
    image, ly = add_text(image, justify_text(records["close"]), lx=50, ly=ly + 20)

    x, y = 80, 500
    template[y : y + image.shape[0], x : x + image.shape[1]] = image

    x, y = 22, 208
    template[y : y + info.shape[0], x : x + info.shape[1]] = info
    return template


if __name__ == "__main__":
    image = download_pdf(
        {
            "name": "Alice Clark",
            "email": "alice@gmail.com",
            "phone": "1234567890",
            "education": ["Indian Institute of Technology - Mumbai"],
            "skills": [
                "Machine Learning",
                "Natural Language Processing",
                "Big Data Handling",
                "Data analysis",
                "Database designing",
                "Microsoft Azure cloud services",
            ],
            "speculate": "Alice Clark has over 20 years of experience in data handling, design, and development. She has worked with Microsoft Azure cloud services and has skills in Machine Learning, Natural Language Processing, and Big Data Handling. However, her resume does not mention any experience in image/video classification and recognition, image segmentation, object detection, OCR, graph neural networks, multimodal, unsupervised and self-supervised learning, etc.",
            "explore": "Alice has worked as a Software Engineer at Microsoft. She has experience in data warehousing and business intelligence. She has also worked on Microsoft Azure cloud services like Document DB, SQL Azure, Stream Analytics, Event hub, Power BI, Web Job, Web App, Power BI, Azure data lake analytics (U-SQL).",
            "adapt": "Alice seems to be adaptable as she has worked on various technologies and platforms. She is also willing to relocate anywhere.",
            "close": "Alice Clark seems to be a strong candidate with extensive experience and a wide range of skills. However, she might need to learn and adapt to some specific technologies and areas mentioned in the job description. Her adaptability and willingness to learn can be a plus point.",
        }
    )
    cv2.imwrite("sample.png", image)
