FROM python:3.8

ENV DASH_DEBUG_MODE True
EXPOSE 8050

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt

WORKDIR /dash
CMD ["python", "main.py"]