FROM python:3.11.4-bookworm

RUN apt-get update && apt-get install -y git

WORKDIR /app

COPY requirements.txt requirements.txt

# RUN pip install virtualenv

# RUN virtualenv venv

# RUN chmod -R 777 venv

# RUN venv/bin/activate



RUN pip install --upgrade cython

RUN pip install numpy
RUN pip install pandas

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python3", "manage.py", "runserver","0.0.0.0:8000"]