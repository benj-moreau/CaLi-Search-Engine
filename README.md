# Introduction
CaLi is a lattice-based model for license orderings. This repository contains the source code of 
1. the prototype of a search engine based on a CaLi ordering and 
2. the experiments made for our research paper to analyse the algorithm we implemented to produce CaLi orderings.

Our code uses the ODRL CaLi ordering ⟨A, DL, CL, C→⟩ such that:
* A is the set of 72 actions of ODRL (e.g., cc:Distribution, cc:ShareAlike), 
* DL is the deontic lattice `Undefined <= Permissions <= Duty <= Prohibition` (actions can be either permitted, obliged, prohibited or not specified; in this deontic lattice, the undefined status is the least restrictive and the prohibited one the most restrictive),
* CL and
* C→ are sets of constraints.

If you simply want to see the usability of our apporach, see our online demonstrator [CaLi online demonstrator](http://cali.priloo.univ-nantes.fr/).

If you want to test our prototype or verify our experiments you should make a [local installation](#Installation). Then, you can either build the prototype of our search engine (see [Search engine](#search-engine)) or execute our experiments (see [Execute experiment](#execute-experiment)).


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
        "resources": [
          {
            "label": "TAXREF-LD: Linked Data French Taxonomic Register",
            "uri": "http://taxref.mnhn.fr/sparql",
            "description": "TAXREF-LD is the Linked Data representation of TAXREF, the French national taxonomical register for fauna, flora and fungus, that covers mainland France and overseas territories. It accounts for over 500000 scientific names."
			    }
        ],
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
        "resources": [
          {
            "label": "RDFLicense",
            "uri": "http://purl.org/NET/rdflicense",
            "description": "This dataset contains 126 licenses (suitable for general works, data, etc.) expressed as RDF.This work is the joint effort of OEG-UPM (Víctor Rodríguez-Doncel) and INRIA (Serena Villata). The editors have not acted in behalf of any of the license issuers, do not claim the legal value of this RDF-version of the licenses, and explicitly decline any responsibility in their use."
			    }
        ],
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
        "resources": [
          {
            "label": "LOD-a-lot",
            "uri": "http://lod-a-lot.lod.labs.vu.nl/LOD-a-lot",
            "description": "A Queryable Dump of the LOD Cloud"
          }
        ],
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

## Build Linked Data and Souce Code Ordering

Orderings of the online demonstrator can be built by executing commands in `./linked_data_ordering.sh`for Linked Data and `./source_code_ordering.sh` for source code. (Do not forget to replace YOUR_ADMIN_PASSWORD).

## Search feature
With search feature, you can:
 - `Find resources whose licenses are compatible with a specific license`
 - `Find resources whose licenses are compliant with a specific license`

Result is ordered by restrictiveness

Search is available at [http://127.0.0.1:8000/ld/](http://127.0.0.1:8000/ld/) for Linked Data and [http://127.0.0.1:8000/rep/](http://127.0.0.1:8000/rep/) for Source Code.

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

We implemented an algorithm that can sort any set of n licenses using the DL see before in approximately n^2/2 comparisons. 
Experiment of the paper can be executed with the following HTTP request:

(Only on local version ! Do not forget to replace YOUR_ADMIN_PASSWORD)
```bash
curl -X GET   'http://127.0.0.1:8000/api/licenses/experiment/algo?step=100&executions=3'   -H 'Admin-Password: YOUR_ADMIN_PASSWORD'
```
We evaluate our algorithm by ordering 20 subsets of licenses of different sizes from the CC_CaLi ordering. Size of subsets is incremented by 100 up to 2187 licenses. Each subset is created and sorted 3 times randomly. Results contain the average of the number of comparisons and the time to sort each subset. Results are stored in [results](https://github.com/benjimor/CaLi/tree/master/expermiental_results).
