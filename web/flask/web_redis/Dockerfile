FROM python:3.6-alpine3.7

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
EXPOSE 22334
CMD [ "python", "./main.py" ]