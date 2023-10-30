import base64
from io import BytesIO
from PIL import Image
from typing import List
from app import schemas

# from app.lib.models import ModelHandler
from app.lib.apis import APIHandler


class Matcher:
    def __init__(self) -> None:
        # self.model_handler = ModelHandler()
        self.api_handler = APIHandler()

    @staticmethod
    def base64_to_image(base64_string):
        img_data = base64.b64decode(base64_string)
        return Image.open(BytesIO(img_data))

    def process(self, images: str, jd_images: str) -> List[str]:
        """
        Process the job description and resume.

        Args:
            images (List[Image.Image]): List of images.
            jd_images (List[Image.Image]): List of images.

        Returns:
            str: text in resume.
            float: Similarity score.
            str: Details of resume.
        """
        resume = self.api_handler.extract_text(images)
        job_description = self.api_handler.extract_text(jd_images)
        print("Done processing resume!")
        similarity_score = self.api_handler.get_similarity(job_description, resume)
        details = self.api_handler.get_details(job_description, resume)
        print("Done processing!")
        return resume, job_description, similarity_score, details
