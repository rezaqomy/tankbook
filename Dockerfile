FROM python:3.12

WORKDIR /app

COPY requirements.txt .  
COPY requirements/ ./requirements/

RUN pip install --no-cache-dir -r requirements.txt

COPY start.sh /start.sh
RUN chmod +x /start.sh
CMD ["sh","start.sh"]

COPY . .
