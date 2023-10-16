import time
import logging
import easyocr
import numpy as np
from PIL import Image
from typing import List
from collections import defaultdict
from ultralytics import YOLO

_logger_ = logging.getLogger(__name__)


class ModelHandler:
    def __init__(self, model_path: str = "weights/best.pt"):
        self.model = YOLO(model_path)
        self.reader = easyocr.Reader(["en"], gpu=False)

    def get_text_from_image(self, images: List[Image.Image]) -> str:
        """
        Extract text from images using OCR and YOLOv8 model.

        Args:
        model: The YOLOv8 model.
        reader: The EasyOCR reader for text extraction.

        Returns:
        str: The extracted text from images.
        """
        text_dict = defaultdict(list)
        _logger_.info("Extracting text from images...")
        for image in images:
            # Use the model to predict text regions
            predictions = self.model.predict(image, conf=0.25)
            result = predictions[0]

            start_time = time.time()
            for box in result.boxes:
                x, y, width, height = [round(x) for x in box.xywh[0].tolist()]
                class_name = self.model.names[box.cls[0].item()]
                # prob = round(box.conf[0].item(), 2)

                x1 = x - (width / 2)
                y1 = y - (height / 2)
                x2 = x + (width / 2)
                y2 = y + (height / 2)

                cropped_image = image.crop((x1, y1, x2, y2))
                gray_image = cropped_image.convert("L")

                # Extract text using EasyOCR
                text = self.reader.readtext(np.array(gray_image))
                text = " ".join([txt[1] for txt in text])
                text_dict[class_name].append(text)
        execution_time = time.time() - start_time
        _logger_.info(f"Execution time for OCR: {execution_time:.5f} seconds")
        text_list = [text for v in text_dict.values() for text in v]
        full_text = " ".join(text_list)
        return full_text
