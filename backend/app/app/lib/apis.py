import os
import openai
import numpy as np
from app import schemas
from google.cloud import vision
from google.cloud.vision_v1 import types
from typing import List


os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"/app/app/lib/credentials.json"

class APIHandler:
    def __init__(self, vision_api: vision = vision, text_api: openai = openai) -> None:
        self.vision_api = vision_api.ImageAnnotatorClient()
        self.text_api = text_api
        self.text_api.organization = "org-Dl6EDMxJ4HCZdOD7Wr7te5pe"
        self.text_api.api_key = "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"

    def extract_text(self, encoded_images: List[str]) -> str:
        """
        Extract text from image.

        Args:
            encoded_image (str): Encoded image.

        Returns:
            str: Extracted text.
        """
        resume = ""
        for image in encoded_images:
            image = types.Image(content=image)
            response = self.vision_api.text_detection(image=image)
            texts = response.text_annotations
            full_text = " ".join([text.description for text in texts])
            resume += " " + full_text
        return resume

    def get_similarity(self, job_description: str, resume: str) -> float:
        """
        Get the similarity between job description and resume.

        Args:
            job_description (str): Job description.
            resume (str): Resume.

        Returns:
            float: Similarity score.
        """
        resp = self.text_api.Embedding.create(
            input=[job_description, resume], 
            engine="davinci-similarity" # "text-similarity-davinci-001"
        )
        embedding_a = resp["data"][0]["embedding"]
        embedding_b = resp["data"][1]["embedding"]
        similarity_score = np.dot(embedding_a, embedding_b)
        return similarity_score
    
    def get_details(self, job_title: str, industry: str, job_description, resume: str) -> str:
        """
        Get the details of resume.

        Args:
            job_description (str): Job description.
            resume (str): Resume.

        Returns:
            str: Details of resume.
        """
        message = [
            {
                "role": "system",
                "content": f"""
                I'm a recruiter. I am looking for a person who is capable for ths (job title {job_title}) and (job description {job_description}). 
                Match this job description with applied resume and list their name, contact information, skills, strength and weakness in json format, the key are (name, contact_info, skills, strength, weakness).
                It must be json serializable.
                Remember the same resume and job description pair must output the same answer.
                """,
            },
            {"role": "user", "content": f"This is applied resume. {resume}"},
        ]
        response = self.text_api.ChatCompletion.create(
            model="gpt-4", # gpt-3.5-turbo
            messages = message,
            temperature=0.2,
            max_tokens=1000,
            frequency_penalty=0.0
        )
        return response["choices"][0]["message"]["content"]
