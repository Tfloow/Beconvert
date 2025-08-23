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

def convert_files(type_in, type_out,ID, filename="input.md"):
    output_ext = type_out

    PANDOC_DOCKER = False
    PWD = os.getcwd()
    if PANDOC_DOCKER:
        # Call the conversion tool (e.g., pandoc) here

        cmd=f"docker run --rm --volume {PWD}/uploads/{ID}:/data pandoc/extra {filename} -o output{output_ext}" #--template eisvogel --listings --number-sections"
    else:
        cmd=f'pandoc "uploads/{ID}/{filename}" -o uploads/{ID}/output{output_ext}'# --pdf-engine=xelatex --template eisvogel --listings --number-sections"

    logger.info(PWD)
    logger.info(cmd)
    result = subprocess.run(cmd, shell=True, capture_output=True)

    logger.info(result.stdout.decode("utf-8"))
    if result.stderr:
        logger.error(result.stderr.decode("utf-8"))
        
    # Check if the file exists
    if os.path.exists(f"uploads/{ID}/output{output_ext}"):
        logger.info(f"Conversion successful: uploads/{ID}/output{output_ext}")
        return f"uploads/{ID}/output{output_ext}"
    else:
        logger.error(f"Conversion failed: uploads/{ID}/output{output_ext} not found")
        return False

def create_invoice_pdf(ID, extension_in="md", extension_out=".pdf"):
    if extension_in != "md":
        logger.warning("Dummy invoice - TODO")
        ID = "00000-00000-00000-00000-00000-DBG"
    
    cmd=f"cd pandoc-templates/invoice-2; make {ID} OUTPUT_FILE_TYPE={extension_out}"

    result = subprocess.run(cmd, shell=True, capture_output=True)

    logger.info(result.stdout)
    for line in result.stdout.splitlines():
        logger.info(f"STDOUT: {line}")
    if result.stderr:
        logger.error(result.stderr)

    if os.path.exists(f"uploads/{ID}/output{extension_out}"):
        logger.info(f"Invoice created successfully: uploads/{ID}/output{extension_out}")
        return f"uploads/{ID}/output{extension_out}"
    else:
        logger.error(f"Conversion failed: uploads/{ID}/output{extension_out} not found")
        return False

# Remove folders created over 24 hours ago
HOUR_OLD = 0.1
def remove_old_uploads():
    now = time.time()
    try:
        for folder in os.listdir("uploads"):
            folder_path = os.path.join("uploads", folder)
            if os.path.isdir(folder_path):
                folder_creation_time = os.path.getctime(folder_path)
                if now - folder_creation_time > HOUR_OLD * 60 * 60:  # 24 hours in seconds
                    if "00000-00000-00000-00000-00000-DBG" not in folder_path:
                        shutil.rmtree(folder_path)
    except:
        os.mkdir("uploads")