FROM swipl:9.0.4 AS prolog-base
FROM python:3.11-slim-bookworm

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends \
        libgmp10 \
        libssl3 \
        libarchive13 \
        libdb5.3 \
        libpcre2-8-0 \
        libyaml-0-2 \
        libossp-uuid16 \
        zlib1g \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

COPY --from=prolog-base /usr/lib/swi-prolog /usr/lib/swi-prolog
COPY --from=prolog-base /usr/bin/swipl       /usr/bin/swipl

ENV SWI_HOME_DIR=/usr/lib/swi-prolog
ENV LD_LIBRARY_PATH=/usr/lib/swi-prolog/lib/x86_64-linux:$LD_LIBRARY_PATH

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
