# Python image to use.
FROM python:3.9

# Set the working directory to /app
WORKDIR /app

# WORKDIR /app/VirtualBot
# copy the requirements file used for dependencies
# COPY requirements.txt .
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

EXPOSE 8080
# Run app.py when the container launches
ENTRYPOINT ["python", "interact.py"]
