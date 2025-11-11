FROM python:3.13-slim-trixie

WORKDIR /infoqr

COPY requirements.txt ./
RUN apt update \
    && apt install -y --no-install-recommends locales \
    && rm -rf /var/lib/apt/lists/* \
    && sed -i '/es_AR.UTF-8/s/^# //g' /etc/locale.gen \
    && locale-gen \
    && pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

ENV LANG=es_AR.UTF-8 \
    LANGUAGE=es_AR:es \
    LC_ALL=es_AR.UTF-8

COPY app app
USER nobody:nogroup

EXPOSE 8000
CMD ["gunicorn", "--bind=0.0.0.0:8000", "--workers=4", "app:create_app()"]