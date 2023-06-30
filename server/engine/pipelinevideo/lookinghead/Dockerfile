FROM python:3.9.12

WORKDIR /app

RUN apt-get update
RUN apt install -y libgl1

COPY ./lookinghead/requirements.txt requirements.txt
COPY ./lookinghead/lookinghead.py lookinghead.py
COPY ./lookinghead/person_looking.py person_looking.py
RUN pip3 install -r requirements.txt

COPY ./config/* ./
COPY ./helpers/* ./

ENTRYPOINT [ "python3" ]
CMD [ "lookinghead.py" ]