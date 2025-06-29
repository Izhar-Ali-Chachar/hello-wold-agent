from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
from langchain_chroma import Chroma


pdf_path = 'hello.pdf'

pdf_loader = PyPDFLoader(pdf_path)

pages = pdf_loader.load()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

pages_split = text_splitter.split_documents(pages)

