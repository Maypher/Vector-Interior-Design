FROM python:3

WORKDIR /app/

COPY ./common/requirements.txt ./common/
COPY ./admin/requirements.txt ./admin/

RUN pip install --no-cache-dir -r ./admin/requirements.txt

COPY ./common/ ./common/
COPY ./admin/ ./admin/

ENV PYTHONPATH=/app/

CMD ["python", "-u", "admin/src/app.py", "migrate"]
