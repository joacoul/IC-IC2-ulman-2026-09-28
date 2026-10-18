FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY consulta.py ./
CMD ["python", "consulta.py"]