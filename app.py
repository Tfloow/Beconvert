from flask import Flask, abort, render_template, request, make_response, send_file, send_from_directory, session
from flask_babel import Babel, _
# _ to evaluate the text and translate it
import sqlite3

# To handle apscheduler
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.memory import MemoryJobStore
from contextlib import asynccontextmanager
import atexit

# check if Windows or linux
import platform
WINDOWS = platform.system() == "Windows"
LINUX = platform.system() == "Linux"
# manage the lock mechanism
if LINUX:
    from lock import *
if WINDOWS:
    from filelock import FileLock

import datetime as dt


# Homemade modules
from logger_config import *
from convert import *

from dotenv import load_dotenv
# Load .env into process environment
load_dotenv()

SupportedFileTypes = {
    "Markdown": ".md",
    "CSV": ".csv",
    "HTML": ".html",
    "Word": ".docx",
    "Jupyter": ".ipynb",
    "JSON": ".json",
    "LaTeX": ".tex",
    "OpenDoc": ".odt",
    "RichText": ".rtf"
}

SupportedOutputFileTypes = {
    "PDF": ".pdf",
    "Markdown": ".md",
    "HTML": ".html",
    "Word": ".docx",
    "Jupyter": ".ipynb",
    "JSON": ".json",
    "LaTeX": ".tex",
    "OpenDoc": ".odt",
    "RichText": ".rtf",
    "PowerPoint": ".pptx"
}

app = Flask(__name__)

LANGUAGES=["en"]
wanted_language = None

def get_locale():
    return request.accept_languages.best_match(["en", "fr", "nl"])


babel = Babel(app, locale_selector=get_locale)

def cookie_premium_check():
    cookie = request.cookies.get("PRO_KEY", None)
    PRO_ACCESS = os.getenv("SECRET_KEY_PRO_FEATURES", None)
    
    if PRO_ACCESS is not None:
        return PRO_ACCESS
    
    # If not found, check /etc/secrets
    secret_path = "/etc/secrets/.env"
    if os.path.exists(secret_path):
        with open(secret_path, "r") as f:
            PRO_ACCESS = f.read().split("=")[1].strip('"')
    else:
        PRO_ACCESS = False

    logger.info(f"Cookie: {cookie}, Env: {PRO_ACCESS}")

    if cookie != PRO_ACCESS:
        logger.warning("User is not premium")
        PRO_ACCESS = False
    else:
        PRO_ACCESS = True
        logger.info("User is premium")

    return PRO_ACCESS

@app.route("/")
def index():
    logger.info("Index page accessed")
    return render_template("index.html", SupportedFileTypes=SupportedFileTypes, SupportedOutputFileTypes=SupportedOutputFileTypes)

@app.route("/conversion")
def conversion(warning=False):
    input_type = request.cookies.get("input_type", "Markdown")   # default = Markdown
    output_type = request.cookies.get("output_type", "PDF") # default = PDF

    logger.info(f"Conversion page accessed: {input_type} to {output_type}")
    return render_template("conversion.html", ID=None, FILE_IN=input_type, FILE_OUT=output_type, SupportedFileTypes=SupportedFileTypes, SupportedOutputFileTypes=SupportedOutputFileTypes, warning=warning)

# Todo

@app.route("/guide")
def guide():
    logger.info("Guide page accessed")
    return render_template("guide.html")

@app.route("/info")
def info():
    logger.info("Info page accessed")
    return render_template("guide.html")

@app.route("/invoice")
def invoice(ID=None, error=False,warning=False, file_out_type=".pdf"):
    logger.info("Invoice page accessed")
    # Check .env file and compare with saved cookie
    PRO_ACCESS = cookie_premium_check()

    return render_template("invoice.html", ID=ID, error=error, warning=warning, PRO_ACCESS=PRO_ACCESS, SupportedOutputFileTypes=SupportedOutputFileTypes, file_out_type=file_out_type)

@app.route("/shipping")
def shipping_label():
    logger.info("Shipping label page accessed")
    return render_template("guide.html")


UPLOAD_FOLDER = "uploads"

# To render PDF files
@app.route("/uploads/<ID>/<filename>")
def uploaded_file(ID, filename):
    folder = os.path.join(UPLOAD_FOLDER, ID)
    file_path = os.path.join(folder, filename)
    if os.path.exists(file_path):
        return send_from_directory(folder, filename)
    else:
        abort(404)

# URL /FROM-TO format will pick input to output format
@app.route("/convert/<input_format>-<output_format>", methods=["POST"])
def convert(input_format, output_format):
    logger.info(f"Conversion requested: {input_format} to {output_format}")
    
    uploaded_file = request.files["file"]
    if uploaded_file.filename == "":
        return conversion(warning=True)
    
    ID = new_conversion_ID()
    
    # Save to disk
    uploaded_file.save(f"uploads/{ID}/{uploaded_file.filename}")

    input_type = request.cookies.get("input_type", "Markdown")   # default = Markdown
    output_type = request.cookies.get("output_type", "PDF") # default = PDF

    output_file = convert_files(SupportedFileTypes[input_format], SupportedOutputFileTypes[output_format], ID, filename=uploaded_file.filename)

    if not output_file:
        return render_template("conversion.html", ID=None, FILE_IN=input_type, FILE_OUT=output_type, SupportedFileTypes=SupportedFileTypes, SupportedOutputFileTypes=SupportedOutputFileTypes, error=True)
    
    return render_template("conversion.html", ID=ID, FILE_IN=input_type, FILE_OUT=output_type, SupportedFileTypes=SupportedFileTypes, SupportedOutputFileTypes=SupportedOutputFileTypes)
    return send_file(
        output_file,
        mimetype="application/pdf",
        as_attachment=False,   # forces download
        download_name=f"{uploaded_file.filename.split('.')[0]}_by_Beconvert.pdf"  # filename shown to user
    )
    
@app.route("/invoice/create", methods=["POST"])
def create_invoice():
    logger.info("Create invoice requested")


    uploaded_file = request.files["file"]
    if uploaded_file.filename == "":
        logger.info("Empty invoice file")
        return invoice(warning=True)
    
    PRO_ACCESS = cookie_premium_check()
    ID = new_conversion_ID()

    extension_out = SupportedOutputFileTypes[request.cookies.get("output_type_invoice", "PDF")] # default = PDF
    
    if not PRO_ACCESS and extension_out != ".pdf":
        logger.warning("User is not premium and requested non-PDF output")
        extension_out = ".pdf"

    # Save to disk
    extension = uploaded_file.filename.split(".")[-1]
    uploaded_file.save(f"uploads/{ID}/input.{extension}")

    filepath = create_invoice_pdf(ID, extension_in=extension, extension_out=extension_out)

    if not filepath:
        return invoice(error=True)
    
    ID = filepath.split("/")[-2]
    return invoice(ID=ID, file_out_type=extension_out)

# Setup Scheduler to periodically check the status of the website
# When the scheduler need to be stopped
if WINDOWS:
    fd = FileLock("myfile.lock")
else:
    fd = acquire("myfile.lock")
RECHECK_AFTER = 60*60  # seconds

if fd is None:
    logger.error("[LOG]: Could not acquire lock, exiting.")
    scheduler = None
else:
    jobStores = {
        "default": MemoryJobStore()
    }

    scheduler = BackgroundScheduler(jobstores=jobStores, timezone="UTC")

    scheduler.add_job(
        func=remove_old_uploads,
        trigger="interval",
        seconds=RECHECK_AFTER,
        next_run_time=dt.datetime.utcnow(),  # run immediately at startup
        id="cleanup_job",
        replace_existing=True,
    )

    scheduler.start()
    logger.info("[LOG]: Scheduler started")

    # Ensure scheduler shuts down on exit
    atexit.register(lambda: scheduler.shutdown(wait=False))
    
if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=8080)