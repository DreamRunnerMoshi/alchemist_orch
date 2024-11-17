# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /alchemist_web

# Copy the requirements file into the container
COPY requirements.txt /alchemist_web

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . /alchemist_web/

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=mysite.settings

# Expose port 8000 for the application
EXPOSE 8000

# Run database migrations and start the application
CMD ["sh", "-c",  "python manage.py migrate && daphne -b 0.0.0.0 -p 8000 mysite.asgi:application"]
#CMD ["sh", "-c", "ls -la /alchemist_web && ls -la /alchemist_web/mysite"]