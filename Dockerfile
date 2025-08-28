# Start from the pre-built audiveris image
FROM toprock/audiveris
FROM alpine:latest
# Install a Python runtime for the web application
RUN apk add --no-cache python3 py3-pip

# Copy the web application files into the image
COPY . /app
WORKDIR /app

# Install Flask
RUN python -m pip install flask

# Set the entrypoint to run the Flask application
CMD ["python3", "app.py"]
