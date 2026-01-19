FROM python:3.10-alpine

RUN adduser -D server
WORKDIR /home/server

# Copy requirements first as to not disturb cache for other changes.
COPY requirements.txt .

# Install dependencies
RUN apk add -U --no-cache libpq-dev build-base git zlib-dev jpeg-dev

RUN pip3 install -r requirements.txt && \
  pip3 install gunicorn

USER server

# Finally, copy the entire source.
COPY . .

ENV FLASK_APP cam.py
EXPOSE 5000
ENTRYPOINT ["gunicorn", "-b", ":5000", "--access-logfile", "-", "--error-logfile", "-", "cam:app"]
