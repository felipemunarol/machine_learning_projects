FROM python:latest
WORKDIR /home/felipe/machine_learning_projects/docker/NLP
COPY . .
RUN pip install -r /home/felipe/machine_learning_projects/docker/NLP/requirements.txt
# Command that runs when container starts
CMD ["python", "/home/felipe/machine_learning_projects/docker/NLP/text_processing.py"]