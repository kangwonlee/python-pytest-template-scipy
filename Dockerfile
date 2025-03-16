FROM ghcr.io/kangwonlee/edu-scipy:0.2.4

USER runner
WORKDIR /tests/

RUN mkdir -p /tests/
COPY tests/* /tests/

USER root

# Download the latest installer
ADD https://astral.sh/uv/install.sh /uv-installer.sh

# Run the installer then remove it
RUN sh /uv-installer.sh && rm /uv-installer.sh

# Ensure the installed binary is on the `PATH`
ENV PATH="/root/.local/bin/:$PATH"

USER runner

COPY pyproject.toml pyproject.toml
RUN uv sync

RUN python3 -c "import glob; files = glob.glob('/tests/test_*.py'); print('Found', len(files), 'files:', files); assert files, 'No files in /tests/!'"

WORKDIR /app/
