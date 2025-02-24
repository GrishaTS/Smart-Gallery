FROM python:3.12-alpine

WORKDIR /frontend

RUN apk add --no-cache \
    gtk+3.0 \
    libx11 \
    gstreamer \
    gst-plugins-good \
    gst-plugins-bad \
    gst-plugins-base \
    ffmpeg \
    bash \
    libmagic

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "app/main.py"]