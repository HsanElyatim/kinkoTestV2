FROM python:3.9-slim

# Install necessary system packages
RUN apt-get update && apt-get install -y \
    libpq-dev \
    wget \
    unzip \
    xvfb \
    x11-utils \
    curl \
    ca-certificates \
    gnupg \
    firefox-esr \
    && rm -rf /var/lib/apt/lists/* \
    && curl -L https://github.com/mozilla/geckodriver/releases/download/v0.30.0/geckodriver-v0.30.0-linux64.tar.gz | tar xz -C /usr/local/bin \
    && chmod +x /usr/local/bin/geckodriver 

# Adding trusting keys to apt for repositories
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -

# Adding Google Chrome to the repositories
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'

# Updating apt to see and install Google Chrome
RUN apt-get -y update

# Install Google Chrome
RUN apt-get install -y google-chrome-stable && apt-get clean

# Download the Chrome Driver
RUN LATEST_CHROMEDRIVER_VERSION=$(curl -s https://chromedriver.storage.googleapis.com/LATEST_RELEASE) \
    && wget -O /tmp/chromedriver.zip https://chromedriver.storage.googleapis.com/$LATEST_CHROMEDRIVER_VERSION/chromedriver_linux64.zip \
    && unzip /tmp/chromedriver.zip -d /usr/local/bin/ \
    && chmod +x /usr/local/bin/chromedriver \
    && rm /tmp/chromedriver.zip

# Set display port as an environment variable
ENV DISPLAY=:99

# Set the working directory
WORKDIR /KinkoTestV2

# Copy and install Python dependencies
COPY requirements.txt /KinkoTestV2/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . /KinkoTestV2

# Set the entrypoint
ENTRYPOINT ["python", "-u", "main.py"]

# Default command if no other command is provided
CMD []
