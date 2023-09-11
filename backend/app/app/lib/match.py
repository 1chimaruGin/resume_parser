import base64
from io import BytesIO
from PIL import Image
from typing import List
from app.lib.models import ModelHandler
from app.lib.apis import APIHandler

class Matcher:
    def __init__(self) -> None:
        self.model_handler = ModelHandler()
        self.api_handler = APIHandler()
    
    @staticmethod
    def base64_to_image(base64_string):
        img_data = base64.b64decode(base64_string)
        return Image.open(BytesIO(img_data))

    def process(self, images: str, job_description: str) -> List[str]:
        """
        Process the job description and resume.

        Args:
            images (List[Image.Image]): List of images.
            job_description (str): Job description.

        Returns:
            str: text in resume.
            float: Similarity score.
            str: Details of resume.
        """
        images = [self.base64_to_image(img) for img in images]
        print("step 1 done")
        resume = self.model_handler.get_text_from_image(images)
        print("step 2 done")
        similarity_score = self.api_handler.get_similarity(job_description, resume)
        print("step 3 done")
        details = self.api_handler.get_details(job_description, resume)
        return resume, similarity_score, details
        