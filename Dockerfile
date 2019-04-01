FROM ubuntu
FROM python:3.6-jessie

WORKDIR /final_projectV1
COPY . /final_projectV1

RUN pip install pandas
RUN pip install sklearn
RUN pip install spacy
RUN python -m spacy download en
RUN python -m spacy download en_core_web_md


CMD ["python", "-m", "qna.question_classifier.qclassifier"]
