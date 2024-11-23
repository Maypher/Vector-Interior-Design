FROM python:3

WORKDIR /app/

COPY ./common/requirements.txt ./common/
COPY ./user/requirements.txt ./user/

RUN pip install --no-cache-dir -r ./user/requirements.txt

COPY ./common/ ./common/
COPY ./user/ ./user/

ENV PYTHONPATH=/app/

CMD ["python", "-u", "user/src/app.py"]
