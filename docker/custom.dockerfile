ARG AA_DOCKER_TAG
FROM $AA_DOCKER_TAG

RUN cd /home/allianceauth
COPY /conf/requirements.txt requirements.txt
RUN pip install -r requirements.txt
