FROM python:3.10

RUN pip3 install --upgrade pip

ADD . .

RUN pip3 --no-cache-dir install -r requirements.txt

CMD [ "python", "./api.py" ]

# Add your instructions to dockerize the application
# App must run on port 8000
