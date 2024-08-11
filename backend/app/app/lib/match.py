import json
import time
import base64
from io import BytesIO
from PIL import Image
from typing import List
from multiprocessing import Pool
# from app.lib.models import ModelHandler
from app.lib.apis import APIHandler


def process_data(args):
    handler = APIHandler()
    resume = handler.extract_text(args[0])
    job_description = handler.extract_text(args[1])
    return [*args, handler.get_details(job_description, resume)]

def execute_process(resumes: List[str], job_description: str, file_names: List[str], num_process: int = 4) -> List[str]:
    inputs = [(resume, job_description, file_name) for resume, file_name in zip(resumes, file_names)]
    with Pool(num_process) as pool:
        outputs = pool.map(process_data, inputs)
    return outputs

class Matcher:
    @staticmethod
    def base64_to_image(base64_string):
        img_data = base64.b64decode(base64_string)
        return Image.open(BytesIO(img_data))

    def process(self, resumes: List[str], file_names: List[str],  job_description: str, num_process: int = 4) -> List[str]:
        """
        Process the job description and resume.

        Args:
            resumes (List[Image.Image]): List of resumes.
            job_description (str): Job description.

        Returns:
            str: text in resume.
            float: Similarity score.
            str: Details of resume.
        """
        outputs = execute_process(resumes, job_description, file_names, num_process)
        print(f'[INFO] Processing 4 ')
        return outputs

def process_resume(images: List[str], file_names: List[str], 
job_description: List[str], num_process: int = 4):
    start_time = time.time()
    outputs = execute_process(images, job_description, file_names, num_process)
    processed_outputs = {}
    for resume, jobd, file_name, details in outputs:
        try:
            details = json.loads(details)
        except json.decoder.JSONDecodeError:
            processed_outputs[file_name] = "Error"
            continue
        if isinstance(details['job_title'], str):
            details['job_title'] = [details['job_title']]
        processed_outputs[file_name] = {
            "name": details["name"],
            "score": details["score"],
            "records": details,
            "is_ready": True,
            "resume": resume,
            "job_description": jobd,
        }
    end_time = time.time()
    print(f"[INFO] Time taken: {end_time - start_time:.2f}s")
    return processed_outputs