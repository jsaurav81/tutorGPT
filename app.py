import os
from langchain.prompts import PromptTemplate
from langchain.document_loaders import YoutubeLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.chains import LLMChain, RetrievalQA
from langchain.vectorstores import Pinecone
from constants import *
import streamlit as st

DB = None


def retrieval_answer(query):
    llm = model
    template = """Question: {question}

    Answer: Let's think step by step."""

    prompt = PromptTemplate(template=template, input_variables=["question"])
    llm_chain = LLMChain(prompt=prompt, llm=llm)
    ans = llm_chain.run(query)

    return ans


def get_transcript(url):
    loader = YoutubeLoader.from_youtube_url(url, add_video_info=True)
    text = loader.load()
    try:
        text[0].page_content = " ".join(text[0].page_content.split()[:3560])
    except ValueError:
        st.error("This video is not supported!")
        print("Error: The list is empty.")
    # if text:
    #     # Split the page_content and join the first 3560 words
    #     text[0].page_content = " ".join(text[0].page_content.split()[:3560])
    # else:
    #     st.error("This video is not supported!")
    #     print("Error: The list is empty.")
    # text[0].page_content = " ".join(text[0].page_content.split()[:3560])
    return text


def get_retriever(texts):
    documents = texts
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    texts = text_splitter.split_documents(documents)
    embeddings = OpenAIEmbeddings()
    db = FAISS.from_documents(texts, embeddings)
    global DB
    DB = db.as_retriever()
    return DB


def get_transcript_ans(query):
    qa_with_sources = RetrievalQA.from_chain_type(
        llm=model,
        chain_type="stuff",
        retriever=DB,
    )
    query = query
    result = qa_with_sources.run(query)
    return result


def get_transcript_ans2(query, retriever):
    qa_with_sources = RetrievalQA.from_chain_type(
        llm=model,
        chain_type="stuff",
        retriever=retriever,
    )
    query = query
    result = qa_with_sources.run(query)
    return result


def process_url(url):
    text = get_transcript(url)
    get_retriever(text)


def get_from_pinecone(query, subcode):
    docsearch = Pinecone.from_existing_index(index_name, embeddings, namespace=subcode)
    retriever = docsearch.as_retriever()
    return get_transcript_ans2(query, retriever)
