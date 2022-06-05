# 044.me - Server Management

Create `config.py` with values for:

```Python
MONGODB_URI = "mongodb+srv://" # MongoDB server/cluster
SECRET_KEY = "" # JWT signing key
ALGORITHM = "HS256" # JWT signing alogirthm
DB_NAME = "dev" # MongoDB database name
```

```Bash
. venv/bin/activate
flask run
```