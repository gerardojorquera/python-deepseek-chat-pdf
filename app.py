import streamlit as st
import os
#from langchain_community.document_loaders import PDFPlumberLoader
#from langchain_community.document_loaders import PyPDFLoader
from langchain_unstructured import UnstructuredLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
# BORRA ESTA LÍNEA COMENTADA:
# from langchain_community.vectorstores import Chroma  
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM
from langchain_community.vectorstores.utils import filter_complex_metadata

template = """
Eres un asistente especializado en procesar y responder preguntas en español. Tu tarea es:
1. Analizar el contexto proporcionado en español
2. Entender la pregunta en español
3. Generar una respuesta clara y concisa en español

Si no encuentras la respuesta en el contexto, simplemente indica que no lo sabes.
Limita tu respuesta a tres oraciones maximo.

Pregunta: {question}
Contexto: {context}
Respuesta (en español):
"""

pdfs_directory = 'pdfs/'
db_directory = 'vectordb'

# Verifica si existe el directorio de la base de datos
os.makedirs(db_directory, exist_ok=True)

#embeddings = OllamaEmbeddings(model="deepseek-r1:14b")
# Cambia el modelo viejo por el de embeddings dedicado
# ASEGÚRATE de que el string sea idéntico a este y no esté llamando a deepseek o llama:
embeddings = OllamaEmbeddings(model="nomic-embed-text")

# base vectorial
vector_store = Chroma(persist_directory=db_directory, embedding_function=embeddings)

# modelo para las respuestas
model = OllamaLLM(model='deepseek-r1:14b')

# fx para cargar o subir los pdf
def upload_pdf(file):
    with open(pdfs_directory + file.name, "wb") as f:
        f.write(file.getbuffer())

# fx para cargar o leer un pdf        
def load_pdf(file_path):
    loader = UnstructuredLoader(file_path) # <-- Usa el parámetro correcto
    documents = loader.load()
    return documents

# toma el pdf y lo divide en trozos o partes mas pequeñas
def split_text(documents):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, #caracteres
        chunk_overlap=200, #traslapar => contexto chunk anterior
        add_start_index=True # agrega el indice inicial al texto original
    )
    return text_splitter.split_documents(documents)

# guardar los documentos o embedding y se guardan en el disco
def index_docs(documents):
    # 1. Limpia espacios en blanco iniciales o finales de los fragmentos
    for doc in documents:
        doc.page_content = doc.page_content.strip()
    
    # 2. Filtra fragmentos que hayan quedado totalmente vacíos
    clean_documents = [doc for doc in documents if doc.page_content]
    
    # 3. ELIMINA METADATOS COMPLEJOS (Solución al ValueError)
    # Esto convertirá o eliminará los diccionarios internos como {'points': ...}
    clean_documents = filter_complex_metadata(clean_documents)
    
    # 4. Guarda de forma segura los documentos procesados
    if clean_documents:
        vector_store.add_documents(clean_documents)



# recibe la pregunta del usuario y busqueda por similitud
def retrieve_docs(query):
    return vector_store.similarity_search(query)

# toma la pregunta y los documentos y entrega la respuesta
def answer_question(question, documents):
    context = "\n\n".join([doc.page_content for doc in documents])
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | model
    return chain.invoke({"question": question, "context": context})

# st (Grafica)
uploaded_file = st.file_uploader(
    "Subir PDF",
    type="pdf",
    accept_multiple_files=False
)

if uploaded_file:
    upload_pdf(uploaded_file)
    documents = load_pdf(pdfs_directory + uploaded_file.name)
    chunked_documents = split_text(documents)
    index_docs(chunked_documents)

    question = st.chat_input("Escribe tu pregunta aqui...")
    if question:
        st.chat_message("user").write(question)
        related_documents = retrieve_docs(question)
        answer = answer_question(question, related_documents)
        st.chat_message("assistant").write(answer)