# Use Python 3.10 image as the base
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Copy only the requirements file to the container
COPY requirements.txt requirements.txt

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code to the container
COPY . .

# Expose the port for Streamlit (default is 8501)
EXPOSE 8501

# Run the Streamlit application
CMD ["streamlit", "run", "spread_monitor.py", "--server.port=8501", "--server.address=0.0.0.0"]
