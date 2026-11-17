FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN useradd -m -u 1000 showcase
COPY --chown=showcase:showcase . .
USER showcase
ENV HOME=/home/showcase GRADIO_SERVER_NAME=0.0.0.0 PORT=7860
EXPOSE 7860
CMD ["python", "app.py"]
