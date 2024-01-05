import os
import re
import ast
import json
import openai
import numpy as np
from multiprocessing import Pool
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

    def get_details(self, job_description: str, resume: str) -> str:
        """
        Get the details of resume.

        Args:
            job_description (str): Job description.
            resume (str): Resume.

        Returns:
            str: Details of resume.
        """ 
        sample = """
                 {
                        "name": "John Doe",
                        "email": "john@gmail.com",
                        "phone": "1234567890",
                        "education": ["B.Tech", "M.Tech"],
                        "skills": ["python", "AI/ML", "c++"],
                        "techinical_skills": ["leadership", "quick learner"],
                        "certification": ["xyz", "abc"],
                        "experience": 3,
                        "semantic_frequency": 0.7,
                        "job_title": "Data Scientist",
                        "location": "Bangalore",
                        "achievement": ["xyz", "abc"],
                        "spelling_check_error_percentage": 0.003,
                        "score": 0.72,
                        "speculate": "speculate the candiate resume",
                        "explore": "explore the candidate's resume",
                        "adapt": "check if the candidate is adaptable",
                        "close": "your thought about the candidate",
                 }
                 """
        message = [
            {
                "role": "system",
                "content": f"""
                I'm a recruiter. I am looking for a person who is capable for this job description : {job_description}. 
                Match this job description with applied resume: {resume}. Analyaze his/her ability. You must find the name, email, 
                phone number, education, skills, technical skills, certification, experience, semantic frequency, location, achievement.
                And, judge the candidate score in match percentage 0.00 to 1.00 (the score should not be 0.85 or 0.75) based on the job description mainly on skills, technical skils, certification, experience, semantic frequency, location, achievement.
                And also you must speculate, explore, adapt, close on the candidate candidate. The 
                result will be JSON serializable dictionary as shown in this example: {sample}. Must be JSON serializable. 
                """,
            },
            {"role": "user", "content": f"Judge the candidate resume on the basis of job description."},
        ]
        response = self.text_api.ChatCompletion.create(
            # model="gpt-3.5-turbo",  # gpt-3.5-turbo
            model="gpt-4",
            messages=message,
            temperature=0.1,
            max_tokens=1000,
            frequency_penalty=0.0,
        )
        details = response["choices"][0]["message"]["content"]
        try:
            json.loads(details)
        except json.decoder.JSONDecodeError:
            details = self.fix_json(details)
        return details

    def fix_json(self, details):
        """
        Fix the json string.
        """
        return re.sub(r"([a-zA-Z0-9]+):", r'"\1":', details)