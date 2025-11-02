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

# Add environment variables for superuser
ENV DJANGO_SUPERUSER_USERNAME=root
ENV DJANGO_SUPERUSER_PASSWORD=root

# Run migrations and create superuser, then start server
CMD ["sh", "-c", "python manage.py migrate && python manage.py createsuperuser --noinput && python manage.py runserver 0.0.0.0:8000"]
