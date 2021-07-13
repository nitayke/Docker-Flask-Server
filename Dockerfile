FROM python:latest
WORKDIR /flask_server
RUN pip3 install Flask
RUN pip3 install -U flask-cors
COPY server.py server.py
EXPOSE 5000
CMD ["python3", "server.py"]
