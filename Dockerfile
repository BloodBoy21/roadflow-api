FROM python:3.12.9

WORKDIR /app


COPY . .

RUN pip install --no-cache-dir -r requirements.txt

RUN prisma generate

ENV PORT=8080

# Run FastAPI with Uvicorn
CMD ["python","main.py"]