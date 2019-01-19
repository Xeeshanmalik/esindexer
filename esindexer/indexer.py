import ijson

from elasticsearch import Elasticsearch
from elasticsearch.helpers import parallel_bulk


class Indexer:
    def __init__(self, host, port):
        """
        Create a new Indexer around elasticsearch cluster.

        Args:
            es (elasticsearch.ElasticSearch): connection to cluster
        """
        self.es = Elasticsearch([{'host': host, 'port': port}], sniff_on_start=False)
        self.indices = self.es.indices

    def create_index(self, index_name, index_settings, overwrite=False):
        """
        Create a new index in an elasticsearch cluster.

        Args:
            index_name (string): The name of the index to be created
            index_settings (dict): The elastic search index settings.
                http://www.elastic.co/guide/en/elasticsearch/reference/current/indices-templates.html
            overwrite (optional[bool]): whether or not to overwrite an existing index. Default False.
        """

        if not self.indices.exists(index_name):
            self.indices.create(index_name, index_settings)
        elif overwrite:
            self.indices.delete(index_name)
            self.indices.create(index_name, index_settings)

    def add_mappings(self, index_name, doctype, mapping):
        """
        Add one or more mappings to an index if they don't already exist.

        Args:
           index_name (string): The name of the index to add mappings to.
           doctype (string): Document type to create mapping for.
           mapping (dict): The mapping for ``doctype``
               http://www.elastic.co/guide/en/elasticsearch/reference/current/indices-put-mapping.html
        """
        if not self.indices.exists_type(index_name, doctype):
            self.indices.put_mapping(doctype, mapping, index_name)

    def index_documents(self, documents_path, default_doctype, index_name):
        """
        Bulk index a set of documents into an elastic search index.
        Note that by default, documents are overwritten if they are already in the index.

        Args:
            documents_path (string): The full system path to the document json collection.

                {
                    _type: optional(doctype)
                    _id: <document id>
                    'field_1':'val_1',...'field_n':'val_n'
                }

            default_doctype (string): default doctype for documents that don't specify ``_type``.
            index_name (string): list of document types to create mappings from.

        Returns:
            (success count, document errors)
        """
        with open(documents_path) as document_file:
            documents = ijson.items(document_file, "item")
            items = (dict({'_type': doc.get('_type', default_doctype), '_index': index_name}, **doc) for doc in
                     documents)
            results = parallel_bulk(self.es, items, chunk_size=1000, raise_on_exception=False, raise_on_error=False)

            success_count = 0
            fail_count = 0
            for success, info in results:
                if not success:
                    fail_count += 1
                else:
                    success_count += 1
                print("{0} Documents Indexed {1} Documents Failed\r".format(success_count, fail_count)),
            print

            self.indices.flush(index_name, wait_if_ongoing=True, force=False)
