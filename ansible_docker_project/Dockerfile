# Use Python official image
FROM python:3.11

# Set working directory
WORKDIR /app

# Copy files to container
COPY app.py /app

# Install Flask
RUN pip install Flask

# Expose port 5000
EXPOSE 5000

# Run the app
CMD ["python", "app.py"]


