# Use an official Python runtime as a parent image
FROM python:3.12

# Set the working directory in the container
WORKDIR /RAGRARIAN

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/etc/poetry python3 -

# Update PATH
ENV PATH="/etc/poetry/bin:$PATH"

# Copy the pyproject.toml and poetry.lock files to the working directory
COPY pyproject.toml poetry.lock /RAGRARIAN/

# Configure Poetry
RUN poetry config virtualenvs.create false

# Install project dependencies
RUN poetry install --no-root --no-ansi

# Copy the rest of the application code to the working directory
COPY Rag_app /RAGRARIAN/Rag_app

# Copy the start.sh script to the /RAGRARIAN directory
COPY start.sh /RAGRARIAN/start.sh

# Make start.sh executable
RUN chmod +x /RAGRARIAN/start.sh

# Make port 8000 available for FastAPI
EXPOSE 8000

# Make port 8501 available for Streamlit
EXPOSE 8501

# Debug: List the contents of the /RAGRARIAN directory to ensure files are present
RUN ls -la /RAGRARIAN

# We'll override this in docker-compose.yml for each service
CMD ["/RAGRARIAN/start.sh"]