FROM python:3.11

WORKDIR /app

RUN pip install --upgrade pip

COPY trading/requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY trading/ .

COPY utils/ ./utils/

COPY models/ ./models/

COPY scalers/ ./scalers/

CMD ["python", "main.py"]