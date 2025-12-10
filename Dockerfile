# Base Image
FROM python:3.11-slim

# 2. Prevent Python from writing .pyc files and enable unbuffered logs
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set Working Directory
WORKDIR /app

# Copy requirements
COPY requirements.txt .
# Install Dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy Files
COPY . .

# Last command. actually starts the process
CMD ["python","-m", "gunicorn", "-b", "0.0.0.0:$PORT", "app", "--callable", "create_app"]
# CMD gunicorn -b 0.0.0.0:8080 run:app