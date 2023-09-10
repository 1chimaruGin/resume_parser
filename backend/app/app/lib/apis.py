import openai
import numpy as np


class APIHandler:
    def __init__(self, api: openai = openai) -> None:
        self.api = api
        self.api.organization = "org-Dl6EDMxJ4HCZdOD7Wr7te5pe"
        self.api.api_key = "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"

    def get_similarity(self, job_description: str, resume: str) -> float:
        """
        Get the similarity between job description and resume.

        Args:
            job_description (str): Job description.
            resume (str): Resume.

        Returns:
            float: Similarity score.
        """
        resp = self.api.Embedding.create(
            input=[job_description, resume], 
            engine="davinci-similarity" # "text-similarity-davinci-001"
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
        message = [
            {
                "role": "system",
                "content": f"I'm a recruiter. This is a job description {job_description}. Match this job description with applied resume and list their contact information, skills, strength and weakness. Remember the same resume and job description pair must output the same answer.",
            },
            {"role": "user", "content": f"This is applied resume. {resume}"},
        ]
        response = openai.ChatCompletion.create(
            model="gpt-4", # gpt-3.5-turbo
            messages = message,
            temperature=0.2,
            max_tokens=1000,
            frequency_penalty=0.0
        )
        return response["choices"][0]["message"]["content"]
        