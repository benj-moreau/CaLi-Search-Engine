# Introduction
CaLi is a lattice-based model for license orderings. This repository contains the source code of
1. the prototype of a search engine based on a CaLi ordering and
2. the experiments made for our research paper to analyse the algorithm we implemented to produce CaLi orderings.

Our code uses the ODRL CaLi ordering ⟨A, DL, C<sub>L</sub>, C<sub>→</sub>⟩ such that:
* A is the set of 72 actions of ODRL (e.g., cc:Distribution, cc:ShareAlike),
* DL is the deontic lattice `Undefined <= Permissions <= Duty <= Prohibition` (actions can be either permitted, obliged, prohibited or not specified; in this deontic lattice, the undefined status is the least restrictive and the prohibited one the most restrictive),
* C<sub>L</sub> and
* C<sub>→</sub> are sets of constraints.

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

## Build Linked Data and Souce Code Ordering

Orderings of the online demonstrator can be built by executing commands in `./linked_data_ordering.sh`for Linked Data and `./source_code_ordering.sh` for source code. (Do not forget to replace YOUR_ADMIN_PASSWORD).

Notice that actions in `permissions`, `obligations`, `prohibitions` should contain only [ODRL actions](https://www.w3.org/TR/odrl-vocab/#actionConcepts).

## Search feature
With search feature, you can:
 - `Find resources whose licenses are compatible with a specific license`
 - `Find resources whose licenses are compliant with a specific license`

Result is ordered by restrictiveness

Search is available at [http://127.0.0.1:8000/ld/](http://127.0.0.1:8000/ld/) for Linked Data and [http://127.0.0.1:8000/rep/](http://127.0.0.1:8000/rep/) for Source Code.

Notice that graph is also available through Neo4j HTTP Browser at [http://localhost:7474/browser/](http://localhost:7474/browser/). (Port is set in `conf/neo4j.conf` in Neo4j directory)

You will be able to execute custom [Cypher queries](https://neo4j.com/docs/developer-manual/current/get-started/cypher/) on CaLi classification.

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
We evaluate our algorithm by ordering 20 subsets of licenses of different sizes from the CC_CaLi ordering. Size of subsets is incremented by 100 up to 2187 licenses. Each subset is created and sorted 3 times randomly. Results contain the average of the number of comparisons and the time to sort each subset. Results are stored in [experimental_results/](expermiental_results/).

# Algorithms

The goal of the next 3 algorithms is to insert and classify a license in a CaLi ordering graph in linear time O(n).

We use a heuristic, based on the restrictiveness of the new license (l<sub>i</sub>), to chose between two strategies, to insert a license traversing the graph
- from the greatest lower bound (Infimum I), or
- from the least upper bound (Supremum S).

This heuristic reduces the average number of comparisons to insert a node.

To do this, Algorithm 1 calculates the relative position of the new license (level<sub>l<sub>i</sub></sub>) from the number of actions that it obliges and prohibits.
The median of levels (level_median<sub>G</sub>) of the existing graph is calculated from the median of the number of prohibited and obliged actions of existing licenses in the graph G.
Depending on these numbers, a strategy is chosen to find the place of the new license in the graph.

<img src="algorithms/algo_median.png" width="600">

Algorithm 2 adds the license to the CaLi ordering Graph (G) and inserts it starting from the greatest lower bound (Infimum I). This algorithm checks if the new license is valid using the constraints on licenses (C<sub>L</sub>) defined in the CaLi Ordering.

<img src="algorithms/add_license.png" width="600">

Algorithm 3 recursively classifies the new license in the graph starting from the license (l<sub>j</sub>).
Its goal is to find the first license compliant with the new license that is the least restrictive license compliant with the new license. This algorithm checks if the restrictive relation is also a compatible with relation using compatibility constraints of the CaLi ordering (C<sub>-></sub>) with is_compatible function.

<img src="algorithms/classify_license.png" width="600">
