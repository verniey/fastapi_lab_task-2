FROM python:3.10-slim

WORKDIR /app

RUN pip install --upgrade pip
RUN pip install pip-tools

COPY requirements.in .
RUN pip-compile --output-file requirements.txt requirements.in
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
