FROM python:3.11-slim as builder

WORKDIR /app

RUN pip install --no-cache-dir pipenv

COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

FROM python:3.11-alpine as app

WORKDIR /app

# Copy the dependencies from the builder stage
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /app /app

EXPOSE 7600

CMD ["uvicorn", "main:app", "--reload", "--port", "7600"]
