FROM python:3.9-alpine
ENV PYTHONUNBUFFERED 1
RUN mkdir /opt/id_server
WORKDIR /opt/id_server
COPY ./requirements.txt .
COPY ./auth .
RUN apk add --no-cache gcc musl-dev libffi-dev 
RUN pip3 install --no-cache-dir -r requirements.txt
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]