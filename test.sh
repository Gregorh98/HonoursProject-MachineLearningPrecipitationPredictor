uwsgi --socket 0.0.0.0:8000 --protocol=http --enable-threads --threads=2 -w weatherApp:app

