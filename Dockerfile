# Use the Python app service base image
FROM appsvc/python:3.12

# Set the working directory inside the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . .

# Install the required Python packages
RUN pip install -r requirements.txt

# Expose port 8000 to the outside world
EXPOSE 8000

# Command to run the Flask application
CMD ["python", "app.py"]
