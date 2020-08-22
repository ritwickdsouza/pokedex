FROM python:3.8.5
WORKDIR /home/user/app
ADD ./requirements.txt /home/user/app/
RUN pip install -r requirements.txt
ADD . /home/user/app
RUN pip install -e .
CMD ["flask", "run"]
