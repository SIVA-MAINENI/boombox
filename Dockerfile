FROM python:3

ENV FLASK_ENV=development
ENV FLASK_APP=/flaskProject/app.py
ENV LISTEN_PORT=5000

RUN mkdir flaskProject

COPY . flaskProject


WORKDIR flaskProject

#RUN pip3 install --upgrade pip3
RUN pip install pipreqs
RUN python3 -m pip install pyacrcloud

RUN cd /flaskProject && pipreqs .
RUN cd /flaskProject && pip install -r requirements.txt

EXPOSE 5000

ENTRYPOINT ["python3"]
CMD ["app.py"]

EXPOSE 5000