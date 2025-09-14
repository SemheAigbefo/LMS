# Use official Python runtime
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create librarians.txt if it doesn't exist
RUN echo "LIB001" > librarians.txt && \
    echo "LIB002" >> librarians.txt && \
    echo "ADMIN123" >> librarians.txt

# Set environment variables for PostgreSQL
ENV DB_HOST=localhost
ENV DB_NAME=lms
ENV DB_USER=postgres
ENV DB_PASSWORD=postgreSem
ENV DB_PORT=5432

# Run the application
CMD ["python", "LibraryMS.py"]