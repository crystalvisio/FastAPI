# Use official version of python.
FROM python:3.12.3

# Set the working directory inside the container.
WORKDIR /src/

# Copy the requirements file into the container at /src/ directory.
COPY requirements.txt /src/

# Install the required Python packages from requirements.txt.
RUN pip install --no-cache-dir -r /src/requirements.txt

# Copy the entire application code into the container.
COPY . /src/

# Run Alembic migrations to ensure the database schema is up to date,
# and then start the FastAPI application using Uvicorn.
CMD ["sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000"]