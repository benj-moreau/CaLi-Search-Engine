# CaLi
Experiments with lattice.

# Prelude
Installation in a `virtualenv` is advised.

Assuming you already have `python` and `pip`

install neo4j (recommended community-3.4.0)

Create `/cali_webservice/local_settings.py` like this one (HASHED_ADMIN_PASSWORD should be your SHA256 password):

```python
NEOMODEL_NEO4J_BOLT_URL = 'bolt://user:password@127.0.0.1:7687'
HASHED_ADMIN_PASSWORD = '********************'
SECRET_KEY = '*******************'
```

Then, install dependencies

```bash
pip install -r requirements.txt
```

# Run the server
Navigate to cali folder and execute:

```bash
python manage.py runserver
```
