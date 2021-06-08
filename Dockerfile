FROM python:3.9-alpine

COPY . .
RUN pip install -r requirements.txt

CMD ["python3", "main.py"]
