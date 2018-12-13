# Introduction
CaLi is a lattice base model for license ordering. This repository contains the prototype of a search engine based on a CaLi ordering that allows to find resources of the Web whose licenses are compatible or compliant with a target license.

This prototype uses the ODRL CaLi ordering based on the [ODRL set of actions](https://www.w3.org/TR/odrl-vocab/#actionConcepts) and the following Deontic Lattice:
`Undefined <= Permissions <= Duty <= Prohibition`
(actions can be either permitted, obliged, prohibited or not specified (i.e., undefined). In this deontic lattice, the undefined status is the least restrictive and the prohibited one the most restrictive.)

To use our search engine, go to the [CaLi online demonstrator](http://cali.priloo.univ-nantes.fr/) or [Install a local version](#Installation) to run our experiments (see [Execute experiment](#execute-experiment))

# Installation
Installation in a `virtualenv` is recommended.

Assuming you already have `python` and `pip`

## Neo4j
Install neo4j (recommended version: community-3.4.0)

[Set an initial password](https://neo4j.com/docs/operations-manual/current/configuration/set-initial-password/) for neo4j.

## Configure CaLi
Create `/cali_webservice/local_settings.py` like this one:
```python
NEOMODEL_NEO4J_BOLT_URL = 'bolt://user:password@127.0.0.1:7687'
HASHED_ADMIN_PASSWORD = '********************'
SECRET_KEY = '*******************'
```
if user is not set, default user is `neo4j`
HASHED_ADMIN_PASSWORD should be a SHA256 hashed password.
Hash your custom password [Here](https://passwordsgenerator.net/sha256-hash-generator/). It will be used to access admin api of CaLi.
Django SECRET_KEY can be generated [Here](https://www.miniwebtool.com/django-secret-key-generator/)

## Dependencies
Then, install dependencies

```bash
pip install -r requirements.txt
```

## Run the server
Navigate to cali folder and execute:

```bash
python manage.py runserver
```
CaLi WebApp is accessible at: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

You can now try the [search engine](#search-engine) or [run experiments](#execute-experiment).

## In case of errors

CaLi uses the bolt connector to communicate with Neo4j.

If connection is not working, check bolt configuration in Neo4j directory in file `conf/neo4j.conf` and update `/cali_webservice/local_settings.py`.

# Search Engine

An [online version of CaLi](http://cali.priloo.univ-nantes.fr/) is also available.

## Build Creative Commons CaLi ordering

To create a CaLi classification, Post an array of licenses objects at `http://127.0.0.1:8000/api/ld/licenses`.

Notice that actions in `permissions`, `obligations`, `prohibitions` should contain only [ODRL actions](https://www.w3.org/TR/odrl-vocab/#actionConcepts).

The following example classifies Creative Commons licenses:

(Do not forget to replace YOUR_ADMIN_PASSWORD)
```bash
curl -X POST \
  http://127.0.0.1:8000/api/ld/licenses \
  -H 'Admin-Password: YOUR_ADMIN_PASSWORD' \
  -H 'Content-Type: application/json' \
  -d '[
    {
        "resources": [],
        "obligations": [
            "Notice",
            "Attribution"
        ],
        "labels": [
            "CC BY-NC"
        ],
        "prohibitions": [
            "CommericalUse"
        ],
        "permissions": [
            "DerivativeWorks",
            "Distribution",
            "modify",
            "Reproduction"
        ]
    },
    {
        "resources": [],
        "obligations": [
            "Notice",
            "Attribution",
            "ShareAlike"
        ],
        "labels": [
            "CC BY-NC-SA"
        ],
        "prohibitions": [
            "CommericalUse"
        ],
        "permissions": [
            "DerivativeWorks",
            "Distribution",
            "modify",
            "Reproduction"
        ]
    },
    {
        "resources": [],
        "obligations": [
            "Notice",
            "Attribution"
        ],
        "labels": [
            "CC BY-ND"
        ],
        "prohibitions": [
            "DerivativeWorks",
            "modify"
        ],
        "permissions": [
            "Distribution",
            "Reproduction",
            "CommericalUse"
        ]
    },
    {
        "resources": [],
        "obligations": [
            "Notice",
            "Attribution"
        ],
        "labels": [
            "CC BY"
        ],
        "prohibitions": [],
        "permissions": [
            "DerivativeWorks",
            "Distribution",
            "modify",
            "Reproduction",
            "CommericalUse"
        ]
    },
    {
        "resources": [],
        "obligations": [
            "Notice",
            "Attribution"
        ],
        "labels": [
            "CC BY-NC-ND"
        ],
        "prohibitions": [
            "DerivativeWorks",
            "modify",
            "CommericalUse"
        ],
        "permissions": [
            "Distribution",
            "Reproduction"
        ]
    },
    {
        "resources": [],
        "obligations": [
            "Notice",
            "Attribution",
            "ShareAlike"
        ],
        "labels": [
            "CC BY-SA"
        ],
        "prohibitions": [],
        "permissions": [
            "DerivativeWorks",
            "Distribution",
            "modify",
            "Reproduction",
            "CommericalUse"
        ]
    },
    {
        "resources": [],
        "obligations": [],
        "labels": [
            "CC-Ze"
        ],
        "prohibitions": [],
        "permissions": [
            "DerivativeWorks",
            "Distribution",
            "modify",
            "Reproduction",
            "CommericalUse"
        ]
    }
]'
```

The generated graph is visible at [http://127.0.0.1:8000/ld/graph](http://127.0.0.1:8000/ld/graph).

Notice that graph is also available through Neo4j HTTP Browser at [http://localhost:7474/browser/](http://localhost:7474/browser/). (Port is set in `conf/neo4j.conf` in Neo4j directory)

You will be able to execute custom [Cypher queries](https://neo4j.com/docs/developer-manual/current/get-started/cypher/) on CaLi classification.

## Search feature
With search feature, you can:
 - `Find resources whose licenses are compatible with a specific license`
 - `Find resources whose licenses are compliant with a specific license`

Result is ordered by restrictiveness

To enable search feature, add resources in `resources` keys of license objects.

Here is an example of licensed resources:
```json
{
        "permissions": [
            "DerivativeWorks",
            "Distribution",
            "modify",
            "Reproduction",
            "CommericalUse"
        ],
        "obligations": [],
        "labels": [
            "CC-Ze"
        ],
        "prohibitions": [],
        "resources": [
            {
                "description": "A Queryable Dump of the LOD Cloud",
                "uri": "http://lod-a-lot.lod.labs.vu.nl/LOD-a-lot",
                "label": "LOD-a-lot"
            },
            {
                "description": "Enipedia is an active exploration into the applications of wikis and the semantic web for energy and industry issues. Through this we seek to create a collaborative environment for discussion, while also providing the tools that allow for data from different sources to be connected, queried, and visualized from different perspectives.",
                "uri": "http://enipedia.tudelft.nl/sparql",
                "label": "Enipedia - Energy Industry Data"
            },
            {
                "description": "Conversion of various NASA datasets into RDF, starting with the spacecraft data from the NSSDC master catalog.",
                "uri": "http://api.kasabi.com/dataset/nasa/apis/sparql",
                "label": "NASA Space Flight & Astronaut data"
            },
            {
                "description": "This data set maps the locations of crashes involving bikes in the Chapel Hill Region of North Carolina.",
                "uri": "https://data.opendatasoft.com/explore/api/tpf/bicycle-crash-data-chapel-hill-region@townofchapelhill",
                "label": "Bicycle Crashes"
            }
        ]
    }
```

Search will be available at [http://127.0.0.1:8000/ld/](http://127.0.0.1:8000/ld/)

## Reset CaLi ordering

To remove a classifications use the following HTTP request:

(Do not forget to replace YOUR_ADMIN_PASSWORD)
```bash
curl -X DELETE \
  http://127.0.0.1:8000/api/ld/licenses \
  -H 'Admin-Password: YOUR_ADMIN_PASSWORD' \
  -H 'Content-Type: application/json'
```

# Execute experiment

Experiment api is available at `/api/licenses/experiment`. you can pass 2 HTTP parameters:

| Parameter |          Values          | Description                     |
|-----------|:------------------------:|---------------------------------|
| structure | `lattice` `linear_order` | structure of the set of license |
| order     |    `rand` `asc` `desc`   | Restrictiveness order           |


For example, the following experiment will classify all possible licenses of a vocabulary of 7 actions, in a random order using infimum, supremum and median algorithm.

(Do not forget to replace YOUR_ADMIN_PASSWORD)
```bash
curl -X GET   'http://127.0.0.1:8000/api/licenses/experiment/?structure=lattice&order=rand'   -H 'Admin-Password: YOUR_ADMIN_PASSWORD'
```

Result is available in `experimental_results/` folder in `CSV` format file containing time and number of node to visit in order to classify each license using the three algorithms.

## Experiment of the paper

Experiment of the paper can be executed with the following HTTP request:

```bash
curl -X GET   'http://127.0.0.1:8000/api/licenses/experiment/algo?step=100&executions=3'   -H 'Admin-Password: YOUR_ADMIN_PASSWORD'
```

It evaluate our algorithm by ordering 20 subsets of licenses of different sizes from the CC_CaLi ordering. Size of subsets is incremented by 100 up to 2187 licenses. Here, Each subset is created and sorted 3 times randomly. Result contains average of the number of comparisons and time to sort each subset. Result is stored in `experimental_results/`.
