FROM python:3.9
WORKDIR .
COPY ./app ./app/
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt 
COPY ./app ./app/
EXPOSE 5000
CMD ["python", "-m", "app.app"]
ENV FLASK_ENV=development