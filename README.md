# 🎓 Syllabus AI Tutor

### A Retrieval-Augmented Generation-Based Web Tutor for Syllabus-Specific Doubt Resolution

Syllabus AI Tutor is a web-based AI learning assistant that allows students to upload their syllabus PDF and ask questions about the uploaded content.

The system uses Retrieval-Augmented Generation (RAG) to retrieve relevant information from the syllabus and generate a simple answer using a local Ollama LLM.

---

## ✨ Features

- Upload syllabus PDFs
- Extract text from PDFs
- Split syllabus content into chunks
- Generate text embeddings
- Store embeddings in ChromaDB
- Perform semantic search
- Retrieve relevant syllabus content
- Generate answers using a local LLM
- Add additional custom information
- Simple Streamlit interface
- No Gemini API
- No OpenAI API
- Runs using Ollama locally

---

## 🏗️ Architecture

```text
Student
   ↓
Upload Syllabus PDF
   ↓
PyPDF
   ↓
Text Extraction
   ↓
Text Chunking
   ↓
SentenceTransformer
   ↓
Generate Embeddings
   ↓
ChromaDB
   ↓
Student asks Question
   ↓
Question Embedding
   ↓
Semantic Search
   ↓
Retrieve Relevant Chunks
   ↓
Build Context
   ↓
Ollama llama3.2:3b
   ↓
Generate Answer
   ↓
Streamlit