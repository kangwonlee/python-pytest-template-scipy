# begin Dockerfile

FROM ghcr.io/kangwonlee/edu-base-raw:14e3e21

USER root

RUN git clone --depth=1 --branch v0.3.13 https://github.com/kangwonlee/gemini-python-tutor /app/temp/ \
    && mkdir -p /app/ai_tutor/ \
    && mv /app/temp/*.py /app/ai_tutor \
    && mv /app/temp/locale/ /app/ai_tutor/locale/

RUN uv pip install --system --requirement /app/temp/requirements.txt \
    && rm -rf /app/temp \
    && chown -R runner:runner /app/ai_tutor/

USER runner

WORKDIR /tests/

RUN mkdir -p /tests/

COPY tests/* /tests/

RUN python3 -c "import pytest; import requests; import glob; files = glob.glob('/tests/test_*.py'); print('Found', len(files), 'files:', files); assert files, 'No files in /tests/!'"

WORKDIR /app/

# end Dockerfile
