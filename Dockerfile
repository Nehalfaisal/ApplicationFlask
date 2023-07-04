# Base image
FROM python:3.10.6

# Set working directory
WORKDIR /root/flask_App/Flask-Applicaion

# Copy requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install -r requirements.txt

# Copy application code
COPY . .

# Expose the application port
EXPOSE 5000

# Set the entry point command
CMD ["python", "app.py", "--host=db", "--port=3306"]
