FROM python:3.10-slim

# ติดตั้ง build-essential สำหรับ C compiler
RUN apt-get update \
    && apt-get install -y build-essential \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . /app

# คัดลอกไฟล์ requirements.txt และติดตั้ง packages ที่จำเป็น
RUN pip install --upgrade pip
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port the app runs on
EXPOSE 5001

CMD ["python", "app.py"]
