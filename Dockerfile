FROM python:3.10-slim

WORKDIR /app
COPY . /app

RUN pip install --upgrade pip --root-user-action=ignore
RUN pip install -r requirements.txt --root-user-action=ignore


EXPOSE 8501
CMD ["streamlit", "run", "app.py"]
