FROM python:slim

WORKDIR /app

COPY setup.py .
COPY requirements.txt .
COPY src src

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install .

EXPOSE 5000

CMD [ "python3", "./src/main.py" ]
