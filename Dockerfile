FROM gorialis/discord.py:3.9-alpine

WORKDIR /app

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "bot.py"]