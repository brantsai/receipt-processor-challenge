ARG PYTHON_VERSION=3.12.7
FROM python:${PYTHON_VERSION}-slim

WORKDIR /app

COPY . .

RUN python -m pip install -r requirements.txt

EXPOSE 8000

# Run the application.
CMD ["python", "app.py"]
