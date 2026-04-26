from pathlib import Path
import pickle
import faiss
from sentence_transformers import SentenceTransformer

from backend.config.settings import KNOWLEDGE_BASE_DIR, VECTOR_STORE_DIR


def build_vector_store():
    texts = []
    metadata = []

    for txt_file in Path(KNOWLEDGE_BASE_DIR).rglob("*.txt"):
        content = txt_file.read_text(encoding="utf-8")
        texts.append(content)
        metadata.append({"source": str(txt_file)})

    if not texts:
        raise ValueError("No knowledge base documents found")

    model = SentenceTransformer("all-MiniLM-L6-v2")
    embeddings = model.encode(texts, convert_to_numpy=True)

    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)

    VECTOR_STORE_DIR.mkdir(parents=True, exist_ok=True)

    faiss.write_index(index, str(VECTOR_STORE_DIR / "index.faiss"))
    with open(VECTOR_STORE_DIR / "meta.pkl", "wb") as f:
        pickle.dump(metadata, f)

    print(f"✅ Loaded {len(texts)} documents")
    print("✅ Vector store saved successfully")


if __name__ == "__main__":
    build_vector_store()
