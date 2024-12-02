# Base image
FROM ubuntu:20.04

# Install Python and required packages
RUN apt-get update && \
    apt-get install -y python3.10 python3-pip wget unzip && \
    apt-get clean

# Install MetaTrader5 Terminal
RUN wget -O mt5.zip "https://download.mql5.com/cdn/web/metaquotes.software.corp/metaeditor5setup.exe" && \
    unzip mt5.zip -d /opt/mt5 && \
    rm mt5.zip

# Set environment variables for MetaTrader
ENV PATH="/opt/mt5:${PATH}"

# Set working directory
WORKDIR /app

# Copy application files
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose Streamlit default port
EXPOSE 8501

# Start Streamlit
CMD ["streamlit", "run", "spread_monitor.py", "--server.port=8501", "--server.address=0.0.0.0"]
