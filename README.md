# node
The Local Training Node for The Sentinel AI

## 1. Installation
1. Python Dependencies ```pip3 install -r requirements.txt```
2. Gunicorn ```pip3 install gunicorn```

## 2. Running the code

### 2.1 http

```
python app.py > app.log
```


```
gunicorn app:app --workers 1 --bind 0.0.0.0:5001 --log-file app.log --access-logfile access.log --log-level DEBUG &
```

### 2.2 https
```
sudo gunicorn3 --workers 3 --certfile '/etc/letsencrypt/live/sentinel-node1.anudit.dev/fullchain.pem' --keyfile '/etc/letsencrypt/live/sentinel-node1.anudit.dev/privkey.pem' --log-file app.log --access-logfile access.log --log-level DEBUG -b 0.0.0.0:443 app:app &
```
