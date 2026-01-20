# Use the official Python image.
# https://hub.docker.com/_/python
FROM python:3.12-alpine

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Create a non-root user
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

# Set the working directory
WORKDIR /app

# Install uv
RUN pip install uv

# Copy the requirements and install dependencies
COPY pyproject.toml /app/
RUN uv pip install --system --no-cache -r pyproject.toml

# Copy the rest of the application code
COPY . /app

# Chown the app directory
RUN chown -R appuser:appgroup /app

# Switch to the non-root user
USER appuser

# Expose the port the app runs on
EXPOSE 8000

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
