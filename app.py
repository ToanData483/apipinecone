from flask import Flask, request, jsonify
from sentence_transformers import SentenceTransformer
from pinecone import Pinecone
import os

# Cấu hình
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
INDEX_NAME = "lybot"

# Khởi tạo
app = Flask(__name__)
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index(INDEX_NAME)

@app.route("/query", methods=["POST"])
def query():
    data = request.get_json()
    user_query = data.get("query", "")

    if not user_query:
        return jsonify({"error": "Thiếu nội dung 'query'"}), 400

    query_vector = model.encode(user_query).tolist()
    results = index.query(vector=query_vector, top_k=5, include_metadata=True)

    chunks = [match["metadata"]["text"] for match in results["matches"]]
    answer = "\\n---\\n".join(chunks)

    return jsonify({"answer": answer})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
