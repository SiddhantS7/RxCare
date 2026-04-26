from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]

DATA_DIR = BASE_DIR / "data"

KNOWLEDGE_BASE_DIR = DATA_DIR / "knowledge_base"
VECTOR_STORE_DIR = DATA_DIR / "vector_store"
PRESCRIPTIONS_DIR = DATA_DIR / "prescriptions"
