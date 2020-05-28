FROM python:3.8-alpine

WORKDIR /flatsniper
ADD . /flatsniper
RUN pip3 install --no-cache-dir pipenv &&\
    pipenv install --deploy --clear --ignore-pipfile
EXPOSE 8080

CMD [ "pipenv","run", "python", "app.py"]