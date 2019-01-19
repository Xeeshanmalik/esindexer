#!/usr/bin/env python

import json
import argparse

from indexer import Indexer


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("index_file", help="Path to file containing index definition")
    parser.add_argument("data_file", help="Path to file containing json dump of documents to index")
    parser.add_argument("es_host", help="Elasticsearch Host to index against")
    parser.add_argument("es_port", help="Elasticsearch Host Transport Port")
    parser.add_argument("-r", "--replace", action="store_true", help="Overwrite index if it already exists")

    args = parser.parse_args()

    index_config_path = args.index_file
    documents_path = args.data_file
    host = args.es_host
    port = args.es_port

    overwrite = True if args.replace else False

    with open(index_config_path) as data_file:
        index_config = json.load(data_file)

    index_settings = index_config['index_settings']
    index_name = index_settings['indexname']
    doctypes = index_settings['doctypes']

    indexer = Indexer(host, port)
    indexer.create_index(index_name, index_settings['settings'], overwrite=overwrite)

    for doctype in doctypes:
        indexer.add_mappings(index_name, doctype, index_settings['mappings'][doctype])
        indexer.index_documents(documents_path, doctype, index_name)


if __name__ == '__main__':
    main()
