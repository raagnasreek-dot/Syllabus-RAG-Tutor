import streamlit as st
from pypdf import PdfReader
from rag import add_documents, ask_question


# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="Syllabus AI Tutor",
    page_icon="🎓"
)


# --------------------------------------------------
# Initialize History
# --------------------------------------------------

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


# --------------------------------------------------
# Sidebar - History
# --------------------------------------------------

with st.sidebar:

    st.header("📚 History")

    if st.session_state.chat_history:

        if st.button("🗑️ Clear All"):

            import chromadb

            client = chromadb.PersistentClient(
                path="chroma_db"
            )

            try:
                client.delete_collection(
                    name="syllabus"
                )
            except Exception:
                pass

            st.session_state.chat_history = []

            st.success("History cleared!")

            st.rerun()

        st.divider()

        for index, item in enumerate(
            reversed(st.session_state.chat_history),
            start=1
        ):

            st.markdown(
                f"**{index}. {item['question']}**"
            )

            st.caption(
                item["answer"]
            )

            st.divider()

    else:

        st.info("No history yet.")


# --------------------------------------------------
# Main Page
# --------------------------------------------------

st.title("🎓 Syllabus AI Tutor")

st.write(
    "Ask doubts from your uploaded syllabus."
)


# --------------------------------------------------
# Upload Syllabus
# --------------------------------------------------

uploaded_file = st.file_uploader(
    "Upload your syllabus PDF",
    type=["pdf"]
)


if uploaded_file:

    try:

        reader = PdfReader(uploaded_file)

        text = ""

        for page in reader.pages:
            text += page.extract_text() or ""

        st.info(
            f"📄 **{uploaded_file.name}** uploaded successfully."
        )

    except Exception as e:

        st.error(
            f"❌ Unable to read the PDF.\n\n"
            f"Error: {e}"
        )

        text = ""


    # --------------------------------------------------
    # Process Syllabus
    # --------------------------------------------------

    if st.button("Process Syllabus"):

        if not text.strip():

            st.warning(
                "⚠️ No readable text was found in this PDF."
            )

        else:

            with st.spinner("Processing syllabus..."):

                try:

                    add_documents(
                        text,
                        uploaded_file.name
                    )

                    st.success(
                        "✅ Syllabus processed successfully!"
                    )

                except Exception as e:

                    st.error(
                        f"❌ Failed to process the syllabus.\n\n"
                        f"Error: {e}"
                    )


# --------------------------------------------------
# Ask Question
# --------------------------------------------------

st.divider()

st.subheader("Ask your doubt")

question = st.text_input(
    "Enter your question:"
)


if st.button("Ask AI"):

    if not question.strip():

        st.warning(
            "⚠️ Please enter a question first."
        )

    else:

        with st.spinner("Thinking..."):

            try:

                answer = ask_question(question)

                # Save to history
                st.session_state.chat_history.append(
                    {
                        "question": question,
                        "answer": answer
                    }
                )

                # Show answer below question
                st.subheader("🤖 Answer")

                st.write(answer)

                # Refresh sidebar
                st.rerun()

            except Exception as e:

                st.error(
                    f"❌ Unable to generate an answer.\n\n"
                    f"Error: {e}"
                )