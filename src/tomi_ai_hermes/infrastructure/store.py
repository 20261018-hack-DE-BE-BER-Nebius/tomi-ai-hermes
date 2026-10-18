"""LanceDB evidence and vector tables; vectors are never invented as a fallback."""

import json
from pathlib import Path

import lancedb
import pyarrow as pa

from tomi_ai_hermes.domain.evidence import Document, EvidenceError, sha256


class EvidenceStore:
    def __init__(
        self,
        path: Path | str,
        dimensions: int,
        model: str,
        revision: str = "",
        storage_options: dict[str, str] | None = None,
    ):
        self.revision = revision
        if not str(path).startswith("az://"):
            Path(path).mkdir(parents=True, exist_ok=True)
        self.db = lancedb.connect(str(path), storage_options=storage_options or None)
        self.dimensions, self.model = dimensions, model
        schema = pa.schema(
            [
                ("document_id", pa.string()),
                ("corpus", pa.string()),
                ("text_sha256", pa.string()),
                ("document_json", pa.string()),
            ]
        )
        self.documents = self.db.create_table("documents", schema=schema, exist_ok=True)
        name = "vectors_" + sha256(f"{model}:{revision}:{dimensions}")[:12]
        vector_schema = pa.schema(
            [
                ("document_id", pa.string()),
                ("text_sha256", pa.string()),
                ("embedding_model", pa.string()),
                ("vector", pa.list_(pa.float32(), dimensions)),
            ]
        )
        self.vectors = self.db.create_table(name, schema=vector_schema, exist_ok=True)

    @classmethod
    def from_config(cls, config):
        location, options = config.evidence_storage()
        return cls(
            location,
            config.embed_dimensions,
            config.embed_model,
            config.embed_revision,
            storage_options=options,
        )

    def save(self, document: Document):
        self.save_many([document])

    def save_many(self, documents: list[Document]):
        rows = [
            {
                "document_id": document.document_id,
                "corpus": document.corpus,
                "text_sha256": document.text_sha256,
                "document_json": json.dumps(document.to_dict()),
            }
            for document in documents
        ]
        self.documents.merge_insert(
            "document_id"
        ).when_matched_update_all().when_not_matched_insert_all().execute(rows)

    def all(self, corpus: str | None = None) -> list[Document]:
        rows = self.documents.to_arrow().to_pylist()
        return [
            Document(**json.loads(row["document_json"]))
            for row in rows
            if not corpus or row["corpus"] == corpus
        ]

    def get(self, document_id: str) -> Document | None:
        return next((doc for doc in self.all() if doc.document_id == document_id), None)

    def save_vectors(self, documents: list[Document], vectors: list[list[float]]):
        if len(documents) != len(vectors) or any(len(vector) != self.dimensions for vector in vectors):
            raise EvidenceError("Vector storage dimensions or counts differ")
        rows = [
            {
                "document_id": doc.document_id,
                "text_sha256": doc.text_sha256,
                "embedding_model": self.model,
                "vector": vector,
            }
            for doc, vector in zip(documents, vectors)
        ]
        self.vectors.merge_insert(
            "document_id"
        ).when_matched_update_all().when_not_matched_insert_all().execute(rows)

    def search(self, vector: list[float], limit: int) -> list[dict]:
        if self.vectors.count_rows() == 0:
            return []
        return self.vectors.search(vector).distance_type("cosine").limit(limit).to_list()

    def counts(self) -> dict:
        return {
            "documents": self.documents.count_rows(),
            "vectors": self.vectors.count_rows(),
            "historical_pages": len(self.all("britannica")),
            "wikipedia_articles": len(self.all("wikipedia")),
        }
