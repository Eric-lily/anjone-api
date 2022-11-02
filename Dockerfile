FROM python:3.9

EXPOSE 5000

WORKDIR /project/anjone-api

COPY anjone-api /project/anjone-api/

COPY test.db /

RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

ENTRYPOINT ["uwsgi", "--ini", "uwsgi.ini"]
