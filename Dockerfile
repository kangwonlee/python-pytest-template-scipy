FROM ghcr.io/kangwonlee/edu-scipy:0.2.4

USER runner
WORKDIR /tests/

RUN mkdir -p /tests/
COPY tests/* /tests/

RUN python3 -c "import glob; files = glob.glob('/tests/test_*.py'); print('Found', len(files), 'files:', files); assert files, 'No files in /tests/!'"

WORKDIR /app/
