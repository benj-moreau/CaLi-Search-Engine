# CaLi
Experiments with lattice.

# Prelude
Installation in a `virtualenv` is advised.

Assuming you already have `python` and `pip`

Install neo4j (recommended community-3.4.0)

[Set an initial password](https://neo4j.com/docs/operations-manual/current/configuration/set-initial-password/) for neo4j.

Create `/cali_webservice/local_settings.py` like this one (HASHED_ADMIN_PASSWORD should be your SHA256 password):
```python
NEOMODEL_NEO4J_BOLT_URL = 'bolt://user:password@127.0.0.1:7687'
HASHED_ADMIN_PASSWORD = '********************'
SECRET_KEY = '*******************'
```
if user is not set, default user is `neo4j`
Django SECRET_KEY can be generated [Here](https://www.miniwebtool.com/django-secret-key-generator/)
Hash your custom password [Here](https://passwordsgenerator.net/sha256-hash-generator/). It will be used to access admin api of CaLi.

Then, install dependencies

```bash
pip install -r requirements.txt
```

# Run the server
Navigate to cali folder and execute:

```bash
python manage.py runserver
```
CaLi WebApp is accessible at: `http://127.0.0.1:8000/``

# In case of errors

Cali uses the bolt connector to communicate with neo4j.
if connection is not working, check bolt configuration in neo4j folder `conf/neo4j.conf`.
and update `/cali_webservice/local_settings.py`.
