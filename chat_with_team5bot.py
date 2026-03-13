import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

import streamlit as st
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings, OllamaLLM
from langchain_community.vectorstores import FAISS
from langchain_classic.chains import RetrievalQA
from langchain_core.prompts import PromptTemplate
import tempfile
import time



OLLAMA_LLM_MODEL = "llama3.1"
OLLAMA_EMBEDDING_MODEL = "mxbai-embed-large"

llm = OllamaLLM(
    model=OLLAMA_LLM_MODEL,
    temperature=0.3
)

embeddings = OllamaEmbeddings(
    model=OLLAMA_EMBEDDING_MODEL
)




prompt_template = """
You are a financial analyst assistant specialized in analyzing 10-K reports
for Amazon, Microsoft, and Alphabet.

Rules:
- Search the full document text first (including all pages shown).
- Use ONLY the provided context to answer the question.
- Do not invent numbers or financial information.
- If the answer cannot be found in the documents, say:
  "I cannot find this information in the provided 10-K documents."
- Provide clear and concise answers.
    


Context:
{context}

Question:
{question}

Answer:
"""

PROMPT = PromptTemplate(
    template=prompt_template,
    input_variables=["context", "question"]
)



st.set_page_config(page_title="Chat with 10-K Reports")
st.title("📄💬 Financial 10-K Chatbot")

st.markdown("""
This chatbot analyzes **10-K reports from Amazon, Microsoft, and Alphabet**.

You can ask questions like:
- financial performance
- revenue and cash
- business risks
""")



uploaded_files = st.file_uploader(
    "Upload 10-K PDF files",
    accept_multiple_files=True,
    type=["pdf"]
)


if uploaded_files:

    documents = []

    # Only process PDFs once
    if "vector_store" not in st.session_state:

        with st.spinner("Processing PDF documents..."):

            with tempfile.TemporaryDirectory() as temp_dir:

                for file in uploaded_files:

                    temp_file_path = os.path.join(temp_dir, file.name)

                    with open(temp_file_path, "wb") as f:
                        f.write(file.getbuffer())

                    loader = PyPDFLoader(temp_file_path)
                    documents.extend(loader.load())


               
                text_splitter = RecursiveCharacterTextSplitter(
                    chunk_size=1000,
                    chunk_overlap=200
                )

                docs = text_splitter.split_documents(documents)


                

                st.session_state.vector_store = FAISS.from_documents(
                    docs,
                    embeddings
                )


        st.success("PDFs processed successfully! You can now ask questions.")


    

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:

        with st.chat_message(message["role"]):
            st.markdown(message["content"])


   

    user_input = st.chat_input("Ask a question about the 10-K reports...")

    if user_input:

        st.session_state.messages.append(
            {"role": "user", "content": user_input}
        )

        with st.chat_message("user"):
            st.markdown(user_input)



        retriever = st.session_state.vector_store.as_retriever(
            search_type="mmr",
            search_kwargs={
                "k": 8,
                "fetch_k": 30,
                "lambda_mult": 0.5
            }
        )


      

        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            retriever=retriever,
            chain_type="stuff",
            return_source_documents=True,
            chain_type_kwargs={
                "prompt": PROMPT
            }
        )


      

        with st.spinner("Thinking..."):

            response = qa_chain.invoke(
                {"query": user_input}
            )

            response_text = response["result"]


    

        with st.chat_message("assistant"):

            message_placeholder = st.empty()
            full_response = ""

            for chunk in response_text.split():

                full_response += chunk + " "
                message_placeholder.markdown(full_response)

                time.sleep(0.03)


      
        st.session_state.messages.append(
            {"role": "assistant", "content": response_text}
        )



        with st.expander("View Retrieved Document Chunks"):

            for i, doc in enumerate(response["source_documents"]):

                st.markdown(f"### Chunk {i+1}")

                st.markdown(doc.page_content)

                st.markdown(
                    f"📄 Source page: {doc.metadata.get('page','unknown')}"
                )

                st.markdown("---")

else:

    st.info("Upload PDF files to start chatting.")
