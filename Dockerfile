FROM python:3.9

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt
RUN apt-get update && apt-get install -y default-libmysqlclient-dev build-essential

COPY . .

EXPOSE 8001

CMD ["python", "manage.py", "runserver", "0.0.0.0:8001"]
