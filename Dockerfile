FROM python:3.10

WORKDIR /Movierecommd

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["streamlit","run","app.py","0.0.0.0"]

