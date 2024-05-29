FROM python:3.10-bullseye

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# set work directory
WORKDIR /app

# copy project
COPY . /app

# upgrade pip
RUN /opt/venv/bin/python -m pip install --upgrade pip --no-cache-dir setuptools wheel pip-tools

# set env variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
# COPY requirements.in .
RUN pip-compile requirements/requirements.in > requirements/requirements.txt
RUN pip install -r requirements/requirements.txt

EXPOSE 8000

CMD ["python"]