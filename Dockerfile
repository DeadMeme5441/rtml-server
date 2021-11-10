FROM python:3.9

WORKDIR /code

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

EXPOSE 8000

RUN mkdir /code/files

COPY ./src /code/src

CMD ["uvicorn", "src.index:app", "--host", "0.0.0.0", "--port", "8000"]
