# Use official Python image
FROM python:3.13-slim

# Set working directory inside container
WORKDIR /app

# Copy requirements first for caching
COPY requirements.txt /app/

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy the rest of the project
COPY . /app/

# Expose port 8000
EXPOSE 8000

# Run Django server on container start
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
