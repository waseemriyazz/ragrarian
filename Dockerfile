# Use an official Python runtime as a parent image
FROM python:3.12

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install Poetry
RUN pip install poetry

# Install project dependencies
RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi

# Make port 8000 available for FastAPI
EXPOSE 8000

# Make port 8501 available for Streamlit
EXPOSE 8501

# Define environment variable
ENV PYTHONPATH=/app

# Create a shell script to run both services
RUN echo '#!/bin/bash\n\
poetry run uvicorn main:app --host 0.0.0.0 --port 8000 &\n\
poetry run streamlit run frontend/streamlit.py' > /app/start.sh \
&& chmod +x /app/start.sh

# Set the entry point to our start script
CMD ["/app/start.sh"]