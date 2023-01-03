FROM python:3

ENV PYTHONNUNBUFFERED 1

WORKDIR /code

COPY requirements.txt .
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python3","manage.py","runserver"]