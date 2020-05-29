FROM python:3.8-alpine

ENV PYTHONPATH "${PYTHONPATH}:/flatsniper"
ENV PYTHONUNBUFFERED=TRUE

WORKDIR /flatsniper
COPY Pipfile Pipfile.lock /flatsniper/
RUN pip install --no-cache-dir 'pipenv==2018.11.26' && pipenv install --system --deploy
RUN mkdir data
COPY . /flatsniper
EXPOSE 8080

CMD ["python", "app.py"]