# Use an official Python image with Debian-based OS
FROM python:3.9


# Install required dependencies
RUN apt-get update && apt-get install -y \
    sqlite3 \
    libsqlite3-dev

# Set working directory inside the container
WORKDIR /app

# Copy project files into the container
COPY . .

# Install Python dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Run Django migrations and collect static files
RUN python manage.py migrate --noinput


# Expose port 8000 for Django
EXPOSE 8000

# Command to run the Django server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
