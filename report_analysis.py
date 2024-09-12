from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
import os

def process_annual_report(uploaded_file, openai_api_key):
    # Save uploaded file to a temporary location
    with open("temp_report.pdf", "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Load and split the document
    loader = PyPDFLoader("temp_report.pdf")
    documents = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
    )
    docs = text_splitter.split_documents(documents)

    # Create embeddings and store in FAISS index
    embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
    vectorstore = FAISS.from_documents(docs, embeddings)

    # Remove temporary file
    os.remove("temp_report.pdf")

    return vectorstore

def answer_question_from_report(question, vectorstore, openai_api_key):
    # Retrieve relevant documents
    docs = vectorstore.similarity_search(question, k=4)

    # Load QA chain
    llm = OpenAI(temperature=0, openai_api_key=openai_api_key)
    chain = load_qa_chain(llm, chain_type="stuff")

    # Get the answer
    answer = chain.run(input_documents=docs, question=question)

    # Extract sources (actual text content)
    sources = [doc.page_content for doc in docs]

    return answer, sources
