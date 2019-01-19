# Elastic Search Indexer

## Description

A Python module for bulk indexing a dumped data set against an Elasticsearch Cluster.  The purpose of this module
is to serve as a learning tool and may serve well as a CI hook to a static data set for analysis and functional testing
for those tuning certain queries or algorithms.

## Index Definition

An index definition contains the following information

1.  The name of the index.
2.  List of document types for the index. The first in is considered the default, and the rest processed in order.
3.  Settings, defining at a minimum the number of primary shards and replicas.
4.  For each document type in the formerly mentioned list, a mapping for that document type.

Why are mappings required?

Because you should always be making them.  If you aren't making mappings, then you are likely not putting enough effort
and thought into what is going into your index and why.

### Example

The following example index called comicbook is based on an example index from https://github.com/royrusso/elasticsearch-sample-index

The data file can be found in data/superhero.def of this project.

This example will be replaced by a full mapping in the classifieds space shortly.

```json
{
    "index_settings": {
      "indexname": "comicbook",
      "doctypes": ["superhero"],

      "settings": {
        "number_of_shards": 1,
        "number_of_replicas": 0
      },

      "mappings": {
        "superhero": {
          "properties": {
            "_source": { "enabled": false },
            "_all": { "enabled": false },
            "name": { "type": "string", "index": "analyzed", "store": "true", "similarity": "BM25" },
            "summary": { "type": "string", "index": "analyzed", "store": "true", "similarity": "BM25" }
          }
        }
      }
    }
}
```

## Data Set

The data set file used for indexing should be a JSON list of the documents to be indexed.  Documents will be processed
in order, and therefore any parent document should preceed a child document.

Every document must contain:

1.  The meta _id field to be used as the document's id (Only for ES2x. 5x can auto gen on bulk index) 
2.  All other fields that make up the document

Note, any other meta fields included in the document definition will be passed along, however only the _id is required.

### Example
The following is a snippet from the example dataset in data/superhero.json

```json

[
  {
    "_id":1,
    "name":"Superman",
    "summary":"Superman is an American fictional character, a comic book superhero who appears in comic books" 
  },
  {
    "_id":2,
    "name":"Spider-Man",
    "summary":"Spider-Man is a fictional character, a comic book superhero who appears in comic books published by Marvel Comics."
  },
]

```

## Usage
```
esindexer [-h] [-r] index_file data_file es_host es_port

positional arguments:
  index_file     Path to file containing index definition
  data_file      Path to file containing json dump of documents to index
  es_host        Elasticsearch Host to index against
  es_port        The ES port to use. Note that sniffing is off so point to an ingest node/data node.

optional arguments:
  -h, --help     show this help message and exit
  -r, --replace  Overwrite index if it already exists
```

# Developing

elastic-indexer uses Python 2.7, which is the target runtime on Ubuntu 14.04.
As with any modern python project, you should build this project inside
a virtual environment:

    virtualenv .venv
    source .venv/bin/activate
    # hack hack hack
    deactivate

Not using a virtual environment is highly discouraged.

# Building and deploying a new image to deb repo

After you are satisfied with your changes you should, inside your
virtualenv,

1. bump the version number for esindexer in setup.py and commit the change
2. do a `gnumake dist` to build the debs
3. `gnumake upload` which will upload the new artifacts (you will need a user and pass for ecg repo)

Note that uploading the artifacts requires the requests package.
