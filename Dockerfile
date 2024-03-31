FROM python:3.11.8-slim

ENV PYTHONUNBUFFERED=1

RUN pip install --no-cache-dir --upgrade pip
WORKDIR /code
COPY requirements.txt .
RUN pip install --no-cache-dir -r /code/requirements.txt
COPY . .

EXPOSE 9777

#ENTRYPOINT ["/bin/bash", "-c", "/code/run_prod.sh"]
CMD ["gunicorn", "main:app", "--workers", "5", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:9777"]
