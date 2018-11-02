FROM python:3-slim

RUN pip install gunicorn
RUN pip install flask
RUN pip install flask_cors
RUN mkdir /recommend
COPY . recommend
WORKDIR /recommend
ENV PYTHONPATH=/recommend
EXPOSE 5400
ENTRYPOINT ["bash"]
CMD ["run_recommend_service.sh"]
