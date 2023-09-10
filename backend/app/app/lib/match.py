from PIL import Image
from typing import List
from app.lib.models import ModelHandler
from app.lib.apis import APIHandler

class Matcher:
    def __init__(self) -> None:
        self.model_handler = ModelHandler()
        self.api_handler = APIHandler()

    def process(self, images: List[Image.Image], job_description: str) -> List[str]:
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
        resume = self.model_handler.get_text_from_image(images)
        similarity_score = self.api_handler.get_similarity(job_description, resume)
        details = self.api_handler.get_details(job_description, resume)
        return resume, similarity_score, details
        