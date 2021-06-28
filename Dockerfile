FROM python:3.8
#FROM tiangolo/meinheld-gunicorn-flask:python3.7
#FROM tiangolo/uwsgi-nginx-flask:python3.8
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt

EXPOSE 5000

# command to run on container start

CMD python models.py ; python main.py