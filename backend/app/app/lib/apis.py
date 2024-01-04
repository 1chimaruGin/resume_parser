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
            engine="davinci-similarity",  # "text-similarity-davinci-001"
        )
        embedding_a = resp["data"][0]["embedding"]
        embedding_b = resp["data"][1]["embedding"]
        similarity_score = np.dot(embedding_a, embedding_b)
        return similarity_score

    def get_details(self, job_description: str, resume: str) -> str:
        """
        Get the details of resume.

        Args:
            job_description (str): Job description.
            resume (str): Resume.

        Returns:
            str: Details of resume.
        """
        algoritm = \
        """
        Compare the resume with the job description and score the resume based on the following criteria:
        Skills Match (25 points):
        - Keywords: 10 * (Number of Keywords Matched / Total Keywords)
        - Technical Skills: 7 * (Number of Technical Skills Matched / Total Technical Skills)
        - Cross-Functional Skills: 3 * (Number of Cross-Functional Skills Matched / Total Cross-Functional Skills)
        - Works in the same industry as the job description: 5 (Yes/No)
        - Certifications: 3 * (Number of Certifications Matched / Total Certifications)
        Experience (20 points):
        - Years of Experience: 7 * (Number of Years of Experience / Maximum Years for Full Points)
        - Achievements: 5 * (Number of Achievements / Total Achievements)
        - Progression: 4 * (Progression Level / Maximum Progression Level)
        - Average year job tenure (anything over 5 years is full points): 4 (Yes/No)
        - In the current position for at least 1 year: 1 (Yes/No)
        Education (10 points):
        - Relevance to Role: 4 * (Relevance Level / Maximum Relevance Level)
        - Advanced Degrees: 1 (Yes/No)
        - Academic Achievements: 1 (Yes/No)
        - Continued Education: 1 (Yes/No)
        - Alignment with Job Requirements: 3 * (Alignment Level / Maximum Alignment Level)
        Keywords and Semantics (20 points):
        - Keyword Frequency: 3 * (Frequency Level / Maximum Frequency Level)
        - Semantic Analysis: 4 * (Semantic Analysis Level / Maximum Semantic Analysis Level)
        - Contextual Language: 3 * (Contextual Language Level / Maximum Contextual Language Level)
        Job Title Relevance (10 points):
        - Alignment with Role: 3 * (Alignment Level / Maximum Alignment Level)
        - Progression: 3 * (Progression Level / Maximum Progression Level)
        - Consistency: 2 * (Consistency Level / Maximum Consistency Level)
        - Industry Standardization: 2 * (Standardization Level / Maximum Standardization Level)
        Location (5 points):
        - Local: 5 (Yes/No)
        - Willingness to Relocate: 2 (Yes/No)
        - Experience in Different Locations: 1 (Yes/No)
        Achievements (5 points):
        - Impactful Achievements: 5 * (Impact Level / Maximum Impact Level)
        - Consistency: 3 * (Consistency Level / Maximum Consistency Level)
        - Alignment with Goals: 4 * (Alignment Level / Maximum Alignment Level)
        Formatting (5 points):
        - Spelling errors 0-1 errors: 5
        - Spelling errors 2-3 errors: 3
        - Spelling errors more than 4: 0
        Final Score: Sum of Scores from all Categories (output should be as a percentage)
        """
        sample = """
                 {
                        "name": "John Doe",
                        "email": "john@gmail.com",
                        "phone": "1234567890",
                        "education": ["B.Tech", "M.Tech"],
                        "score": 0.8,
                        "skills": ["python", "AI/ML", "c++"],
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
                Match this job description with applied resume. Analyaze his/her ability. You must find the name, email, 
                phone number, education, skills, resume and job description match score(it is calculate based on this steps {algoritm}. Provide only score, no other words).
                And also you must speculate, explore, adapt, close on the candidate candidate. The 
                result will be JSON serializable dictionary as shown in this example: {sample}. Must be JSON serializable. 
                """,
            },
            {"role": "user", "content": f"This is applied resume. {resume}"},
        ]
        response = self.text_api.ChatCompletion.create(
            # model="gpt-3.5-turbo",  # gpt-3.5-turbo
            model="gpt-4",
            messages=message,
            temperature=0.0,
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