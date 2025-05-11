# begin Dockerfile

FROM ghcr.io/kangwonlee/edu-scipy:0.2.4

USER root

# remove previous version ai tutor
RUN rm -rf /app/ai_tutor

# copy new version ai tutor
RUN git clone --depth=1 --branch v0.3.2 https://github.com/kangwonlee/gemini-python-tutor /app/temp/ \
    && mkdir -p /app/ai_tutor/ \
    && mv /app/temp/*.py /app/ai_tutor \
    && mv /app/temp/locale/ /app/ai_tutor/locale/

USER runner
WORKDIR /tests/

RUN mkdir -p /tests/
COPY tests/* /tests/

RUN python3 -m pip install --no-cache-dir --upgrade pip

# Test before push
RUN which python3 \
  && python3 -c "import pandas as pd; print(pd.__file__); import requests; import pytest; import glob; files = glob.glob('/tests/test_*.py'); print('Found', len(files), 'files:', files); assert files, 'No files in /tests/!'"

WORKDIR /app/

# end Dockerfile
