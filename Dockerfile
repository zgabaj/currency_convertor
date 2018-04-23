FROM python:3.4.4         
ADD . /kiwi
WORKDIR /kiwi
EXPOSE 8080
RUN pip install -r requirements.txt
ENTRYPOINT ["python", "web_api.py"]