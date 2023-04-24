FROM tensorflow/tensorflow:latest

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

CMD ["flask", "run", "--host=0.0.0.0"]
