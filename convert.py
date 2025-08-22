# Uses pandoc and docker to run the conversion
import subprocess
import random
import os
import time
import shutil
from logger_config import *

TYPE_EXTENSION = {
    "markdown": "md",
    "pdf": "pdf",
    "html": "html",
    "word": "docx",
    "powerpoint": "pptx"
}

# create pseudo-random sequence like XXXXX-XXXXX-XXXXX-XXXXX-XXXXXX
def new_conversion_ID():
    ID = "-".join("".join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", k=5)) for _ in range(5))
    try:
        os.makedirs(f"uploads/{ID}", exist_ok=False)
    except OSError:
        print("Directory already exists")
    return ID

def convert_files(type_in, type_out,ID):
    input_ext = TYPE_EXTENSION.get(type_in)
    output_ext = TYPE_EXTENSION.get(type_out)

    if not input_ext or not output_ext:
        print("Unsupported conversion types")
        return None

    PANDOC_DOCKER = False
    PWD = os.getcwd()
    if PANDOC_DOCKER:
        # Call the conversion tool (e.g., pandoc) here
        
        cmd=f"docker run --rm --volume {PWD}/uploads/{ID}:/data pandoc/extra input.{input_ext} -o output.{output_ext}" #--template eisvogel --listings --number-sections"
    else:
        cmd=f"pandoc uploads/{ID}/input.{input_ext} -o uploads/{ID}/output.{output_ext}"# --pdf-engine=xelatex --template eisvogel --listings --number-sections"
    
    logger.info(PWD)
    result = subprocess.run(cmd, shell=True, capture_output=True)

    logger.info(result.stdout.decode("utf-8"))
    logger.error(result.stderr.decode("utf-8"))

    # Return pdf
    return f"uploads/{ID}/output.{output_ext}"

# Remove folders created over 24 hours ago
HOUR_OLD = 0.1
def remove_old_uploads():
    now = time.time()
    for folder in os.listdir("uploads"):
        folder_path = os.path.join("uploads", folder)
        if os.path.isdir(folder_path):
            folder_creation_time = os.path.getctime(folder_path)
            if now - folder_creation_time > HOUR_OLD * 60 * 60:  # 24 hours in seconds
                shutil.rmtree(folder_path)