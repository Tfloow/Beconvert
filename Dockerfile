# Base image (Debian slim + Python)
FROM python:3.12-slim


# Install system dependencies
RUN apt-get update && \
    apt-get install -y curl tar texlive-latex-extra texlive-lang-greek pandoc texlive-xetex make && \
    rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy your app and the run.sh script
COPY . .

# Install the required templates for pandoc
# Inspired by pandoc/extra
ENV PANDOC_DATA_HOME=/usr/local/share/pandoc
ENV PANDOC_TEMPLATES_DIR=/usr/local/share/pandoc/templates

# Invoice zip archive
ENV INVOICE_ARCHIVE=https://github.com/mrzool/invoice-boilerplate/archive/master.zip

#RUN cd pandoc-templates/invoice; make; cat *.log




# Install system dependencies if needed inside run.sh
# (run.sh can handle downloading Pandoc or other tools)
RUN pip install -r requirements.txt


# Expose the port your app runs on
EXPOSE 8000

# Start your app with Gunicorn
CMD ["gunicorn", "app:app", "-b", "0.0.0.0:8000"]
