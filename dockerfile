# -------- Real-Estate Flask App --------
FROM python:3.11-slim

# 1. install Python deps
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt

# 2. copy the whole project (incl. realestate_app/  & migrations/)
COPY . .

# 3. environment
ENV FLASK_APP=realestate_app/app.py \
    PYTHONUNBUFFERED=1 \
    FLASK_RUN_HOST=0.0.0.0 \
    FLASK_DEBUG=0             
    # set 1 for hot-reload inside container

# 4. default cmd is replaced by compose
CMD ["flask", "run"]
