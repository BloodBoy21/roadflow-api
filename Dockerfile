FROM python:3.12

WORKDIR /app


COPY . .

RUN pip install --no-cache-dir -r requirements.txt


RUN prisma generate

ENV PORT=80
EXPOSE 80

# Run FastAPI with Uvicorn
CMD ["python","main.py"]
