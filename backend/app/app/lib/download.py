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


def add_text(image: np.ndarray, lines: List[str], lx: int = 50, ly: int = 50):
    font = cv2.FONT_HERSHEY_SCRIPT_SIMPLEX
    for line in lines:
        cv2.putText(image, line, (lx, ly), font, 0.8, (0, 0, 0), lineType=cv2.LINE_AA)
        ly += 40
    return image, ly


def download_pdf(records, template: str = "sorci.png", bg: str = "bg.png"):

    image = cv2.imread(bg)
    template = cv2.imread(template)

    # Speculate
    image, ly = add_text(image, ["Speculate: "], lx=50, ly=50)
    image, ly = add_text(image, [records["speculate"]], lx=50, ly=ly + 70)

    # Explore
    image, ly = add_text(image, ["Explore: "], lx=50, ly=ly + 70)
    image, ly = add_text(image, [records["explore"]], lx=50, ly=ly + 70)

    # Adapt
    image, ly = add_text(image, ["Adapt: "], lx=50, ly=ly + 70)
    image, ly = add_text(image, [records["adapt"]], lx=50, ly=ly + 70)

    # Close
    image, ly = add_text(image, ["Close: "], lx=50, ly=ly + 70)
    image, ly = add_text(image, [records["close"]], lx=50, ly=ly + 70)

    x, y = 80, 500
    template[y : y + image.shape[0], x : x + image.shape[1]] = image
    return template


if __name__ == "__main__":
    download_pdf("test")
