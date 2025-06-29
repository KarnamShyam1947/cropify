# Use the official TensorFlow 2.13.0 CPU base image
FROM tensorflow/tensorflow:2.13.0

# Set the working directory in the container
WORKDIR /app

# Copy only the requirements first for better cache usage
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Now copy the rest of the application code
COPY . .

# Expose the port used by Gunicorn
EXPOSE 8000

# Run the Flask app with Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "App:app"]
