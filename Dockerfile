FROM ubuntu
FROM python:3.6-jessie

WORKDIR /final_projectV1
COPY . /final_projectV1

RUN pip install --default-timeout=3000 --trusted-host pypi.python.org -r requirements-docker.txt

RUN python -m spacy download en
RUN python -m spacy download en_core_web_md
ENV ELASTICSEARCH_VER 6.1.2
EXPOSE 80 9200 9300

CMD ["python", "-m", "qna.question_classifier.qclassifier"]
