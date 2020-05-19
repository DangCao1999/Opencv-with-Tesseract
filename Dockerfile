FROM python
ENV FLASK_APP app.py
ENV FLASK_ENV development
ENV FLASK_DEBUG true
ENV FLASK_RUN_HOST 0.0.0.0
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN apt-get update
RUN apt-get install -y tesseract-ocr
RUN apt-get install -y libtesseract-dev
COPY . .
CMD ["flask", "run"]