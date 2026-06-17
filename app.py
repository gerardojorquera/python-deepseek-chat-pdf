import streamlit as st
import os
<<<<<<< HEAD
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
#import streamlit.components.v1 as components
=======
from langchain_community.document_loaders import PDFPlumberLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM
>>>>>>> c968b148650b749864631e185efdbcf15381ae21

template = """
Eres un asistente especializado en procesar y responder preguntas en español. Tu tarea es:
1. Analizar el contexto proporcionado en español
2. Entender la pregunta en español
3. Generar una respuesta clara y concisa en español

<<<<<<< HEAD
Si no encuentras la respuesta en el contexto, simplemente indica que no lo sabes.
Limita tu respuesta a tres oraciones maximo.

Pregunta: {question}
Contexto: {context}
Respuesta (en español):
=======
Si no encuentras la respuesta en el contexto, simplemente indica que no la sabes.
Limita tu respuesta a tres oraciones maximo.

Pregunta: {question} 
Contexto: {context}
Respuesta (en español)
>>>>>>> c968b148650b749864631e185efdbcf15381ae21
"""

pdfs_directory = 'pdfs/'
db_directory = 'vectordb'

<<<<<<< HEAD
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
=======
os.makedirs(db_directory, exist_ok=True)

embeddings = OllamaEmbeddings(model='deepseek-r1:14b')
vector_store = Chroma(persist_directory=db_directory, embedding_function=embeddings)
model = OllamaLLM(model='deepseek-r1:14b')

>>>>>>> c968b148650b749864631e185efdbcf15381ae21
def upload_pdf(file):
    with open(pdfs_directory + file.name, "wb") as f:
        f.write(file.getbuffer())

<<<<<<< HEAD
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
=======
def load_pdf(file_path):
    loader = PDFPlumberLoader(file_path)
    documents = loader.load()
    return documents

def split_text(documents):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        add_start_index=True
    )
    return text_splitter.split_documents(documents)

def index_docs(documents):
    vector_store.add_documents(documents)
    vector_store.persists()

def retrieve_docs(query):
    return vector_store.similarity_search(query)

>>>>>>> c968b148650b749864631e185efdbcf15381ae21
def answer_question(question, documents):
    context = "\n\n".join([doc.page_content for doc in documents])
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | model
    return chain.invoke({"question": question, "context": context})

<<<<<<< HEAD
# st (Grafica)
uploaded_file = st.file_uploader(
    "Subir o cargar un archivo PDF",
=======
uploaded_file = st.file_uploader(
    "Subir PDF",
>>>>>>> c968b148650b749864631e185efdbcf15381ae21
    type="pdf",
    accept_multiple_files=False
)

if uploaded_file:
    upload_pdf(uploaded_file)
    documents = load_pdf(pdfs_directory + uploaded_file.name)
<<<<<<< HEAD
    chunked_documents = split_text(documents)
    index_docs(chunked_documents)

    question = st.chat_input("Escribe aquí tu pregunta...")
=======
    chuncked_documents = split_text(documents)
    index_docs(chuncked_documents)
    st.success('Archivo cargado exitosamente')

    """question = st.chat_input("Escribe tu pregunta aqui...")
>>>>>>> c968b148650b749864631e185efdbcf15381ae21
    if question:
        st.chat_message("user").write(question)
        related_documents = retrieve_docs(question)
        answer = answer_question(question, related_documents)
        st.chat_message("assistant").write(answer)
<<<<<<< HEAD
 
# 1. Configurar la página (SIEMPRE DEBE IR PRIMERO)
st.set_page_config(
    page_title="HIS IA Chatbot PDF", # El título de la pestaña del navegador
    page_icon="ico/robot_tierno.ico", # El icono de la pestaña (puede ser un emoji o ruta a imagen)
    layout="centered" # Opcional: "centered" o "wide"
)

# 2. El resto del contenido de tu aplicación
st.title("HIS IA Chatbot PDF ¡Bienvenido!")
st.write("Esta aplicación tiene por objetivo que puedas subir o cargar un archivo PDF y después puedas hacerle preguntas en base a su contenido.")
st.write("*** Pasos: ***")
st.write("1. Subir o cargar un archivo PDF")
st.write("2. Escribir una pregunta y presionar la tecla <ENTER>")
st.write("3. Esperar a la respuesta. En la parte superior derecha aparecerán unos iconos que indican si se esta procesando")
=======
    """
>>>>>>> c968b148650b749864631e185efdbcf15381ae21
