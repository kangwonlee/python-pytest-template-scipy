# begin Dockerfile
FROM python:3.11.11-alpine


RUN apk add --no-cache git


RUN adduser runner --uid 1001 --disabled-password
USER runner


WORKDIR /app


COPY requirements.txt /requirements.txt
RUN python3 -m pip install --upgrade pip && \
    python3 -m pip install --no-cache-dir --user --requirement /requirements.txt


# Optional: Add AI tutor for LLM-generated test feedback
# RUN git clone --depth=1 --branch v0.2.1 https://github.com/kangwonlee/gemini-python-tutor /app/temp/ && \
#     python3 -m pip install --no-cache-dir --user --requirement /app/temp/requirements.txt && \
#     mkdir -p /app/ai_tutor/ && \
#     mv /app/temp/*.py /app/ai_tutor || true && \
#     mv /app/temp/locale/ /app/ai_tutor/locale/ && \
#     rm -rf /app/temp


CMD ["python3", "-m", "pytest", "--version"]
# end Dockerfile
