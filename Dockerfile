FROM ghcr.io/kangwonlee/edu-scipy:0.2.4

USER runner
WORKDIR /tests/

RUN mkdir -p /tests/
COPY tests/* /tests/

COPY requirements.txt requirements.txt
RUN python3 -m pip install --no-cache-dir --upgrade pip && python3 -m pip install --no-cache-dir --requirement requirements.txt

RUN which python3 && python3 -c "import pandas as pd; print(pd.__file__);import glob; files = glob.glob('/tests/test_*.py'); print('Found', len(files), 'files:', files); assert files, 'No files in /tests/!'"

WORKDIR /app/
