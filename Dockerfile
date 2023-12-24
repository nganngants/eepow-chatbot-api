FROM python:3.11

EXPOSE 8080
ENV PORT 8080

RUN groupadd -g 1000 userweb && \
    useradd -r -u 1000 -g userweb userweb

WORKDIR /home
RUN chown userweb:userweb /home

USER userweb

COPY . /home
RUN python3 -m pip install --upgrade pip

RUN pip install -r /home/requirements.txt

CMD python3 /home/model.py