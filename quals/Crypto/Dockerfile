FROM python:latest

# Install node for asset building
RUN apt-get update && apt-get install socat -y

# Create and switch to a user called app
RUN useradd -ms /bin/bash app
WORKDIR /home/app

# Install pycryptodome using pip for the specific user
RUN pip install pycryptodome

# Set the PATH environment variable to include the user-specific Python binaries
ENV PATH="/home/app/.local/bin:${PATH}"

# Copy across dependencies and install them
RUN chown -R app:app /home/app
USER app