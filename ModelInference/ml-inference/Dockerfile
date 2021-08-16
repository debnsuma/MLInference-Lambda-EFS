# Pull the base image with python 3.8 as a runtime for your Lambda
FROM public.ecr.aws/lambda/python:3.8

# Copy the earlier created requirements.txt file to the container
COPY requirements.txt ./

# Install the python requirements from requirements.txt
RUN python3.8 -m pip install -r requirements.txt 

# Create the model directory for mounting the EFS 
RUN mkdir -p /mnt/ml

# Copy the earlier created app.py file to the container
COPY app.py ./

# Set the CMD to your handler
CMD ["app.lambda_handler"]
