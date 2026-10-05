import chromadb
from sentence_transformers import SentenceTransformer
import ollama


# ==================================================
# CONFIGURATION
# ==================================================

EMBEDDING_MODEL = "all-MiniLM-L6-v2"
OLLAMA_MODEL = "llama3.2:3b"

CHROMA_PATH = "chroma_db"
COLLECTION_NAME = "syllabus"

CHUNK_SIZE = 500
TOP_K_RESULTS = 8


# ==================================================
# EMBEDDING MODEL
# ==================================================

model = SentenceTransformer(
    EMBEDDING_MODEL
)


# ==================================================
# CHROMADB
# ==================================================

client = chromadb.PersistentClient(
    path=CHROMA_PATH
)

collection = client.get_or_create_collection(
    name=COLLECTION_NAME
)


# ==================================================
# ADD DOCUMENTS
# ==================================================

def add_documents(text, source):
    """
    Splits text into chunks, creates embeddings,
    and stores the information in ChromaDB.
    """

    chunks = []

    # ----------------------------------------------
    # Text Chunking
    # ----------------------------------------------

    for start in range(
        0,
        len(text),
        CHUNK_SIZE
    ):

        chunk = text[
            start:start + CHUNK_SIZE
        ]

        if chunk.strip():
            chunks.append(chunk)


    if not chunks:
        return


    # ----------------------------------------------
    # Generate Embeddings
    # ----------------------------------------------

    embeddings = model.encode(
        chunks
    ).tolist()


    # ----------------------------------------------
    # Generate Unique IDs
    # ----------------------------------------------

    ids = [
        f"{source}_{index}"
        for index in range(len(chunks))
    ]


    # ----------------------------------------------
    # Store in ChromaDB
    # ----------------------------------------------

    collection.add(
        ids=ids,
        documents=chunks,
        embeddings=embeddings,
        metadatas=[
            {
                "source": source
            }
            for _ in chunks
        ]
    )


# ==================================================
# ASK QUESTION
# ==================================================

def ask_question(question):
    """
    Retrieves relevant information from ChromaDB
    and uses Ollama to generate the final answer.
    """

    # ----------------------------------------------
    # Convert Question to Embedding
    # ----------------------------------------------

    question_embedding = model.encode(
        [question]
    ).tolist()


    # ----------------------------------------------
    # Semantic Search
    # ----------------------------------------------

    results = collection.query(
        query_embeddings=question_embedding,
        n_results=TOP_K_RESULTS
    )


    # ----------------------------------------------
    # Check Search Results
    # ----------------------------------------------

    if (
        not results["documents"]
        or not results["documents"][0]
    ):

        return (
            "I could not find this topic "
            "in the uploaded syllabus."
        )


    # ----------------------------------------------
    # Build Context
    # ----------------------------------------------

    context = "\n\n".join(
        results["documents"][0]
    )


    # ----------------------------------------------
    # RAG Prompt
    # ----------------------------------------------

    prompt = f"""
You are a syllabus-specific AI tutor.

Your job is to help students understand
information from their uploaded syllabus.

Use the provided syllabus context as your
primary source of information.

================ SYLLABUS CONTEXT ================

{context}

================ STUDENT QUESTION ================

{question}

===================================================

Instructions:

1. Answer the question using information
   available in the syllabus context.

2. If the question asks for a list,
   list the relevant items found in the context.

3. If the question asks for an explanation,
   explain it in simple and clear language.

4. If the question is broad,
   summarize the relevant information available
   in the context.

5. Do not invent information that is not
   supported by the syllabus context.

6. If the context contains useful information
   related to the question, answer using it.

7. Only say:

"I could not find this topic in the uploaded syllabus."

when the retrieved context genuinely contains
no useful information related to the question.

8. Keep the answer simple and student-friendly.
"""


    # ----------------------------------------------
    # Generate Answer using Ollama
    # ----------------------------------------------

    response = ollama.chat(
        model=OLLAMA_MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )


    return response[
        "message"
    ][
        "content"
    ]