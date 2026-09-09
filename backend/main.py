from fastapi.middleware.cors import CORSMiddleware
from llm.ollama_client import generate_answer
from fastapi import FastAPI, UploadFile, File
from database import (init_db,add_file,get_files,delete_file_record)
from rag.splitter import split_text
from vector_store.chroma_db import (add_documents,search_documents,delete_documents)
import os
import fitz


app = FastAPI(
    title="Enterprise RAG Assistant"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

init_db()


UPLOAD_DIR = "uploads"


if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)



@app.get("/")
def home():
    return {
        "message": "Enterprise RAG Assistant API"
    }



@app.post("/upload")
async def upload_file(
    file: UploadFile = File(...)
):

    file_path = os.path.join(
        UPLOAD_DIR,
        file.filename
    )


    content = await file.read()


    with open(file_path, "wb") as f:
        f.write(content)


    return {
        "filename": file.filename,
        "message": "文件上传成功"
    }



@app.post("/parse")
async def parse_pdf(
    file: UploadFile = File(...)
):

    file_path = os.path.join(
        UPLOAD_DIR,
        file.filename
    )


    content = await file.read()


    with open(file_path, "wb") as f:
        f.write(content)



    # 打开PDF
    pdf = fitz.open(file_path)


    text = ""


    for page in pdf:
        text += page.get_text()

    chunks = split_text(text)

    count = add_documents(
        chunks,
        file.filename
    )

    add_file(
        file.filename,
        os.path.getsize(file_path)
    )

    page_count = len(pdf)

    pdf.close()

    return {
        "filename": file.filename,
        "pages": page_count,
        "text_length": len(text),
        "chunks": count,
        "message": "文本已经向量化并保存"
    }

@app.post("/search")
async def search(
    question: str
):

    results = search_documents(
        question
    )


    documents = results["documents"][0]


    return {
        "question": question,
        "results": documents
    }


@app.post("/chat")
async def chat(question: str):

    results = search_documents(
        question
    )


    documents = results["documents"][0]

    metadatas = results.get(
        "metadatas",
        [[]]
    )[0]

    distances = results.get(
        "distances",
        [[]]
    )[0]


    context = "\n\n".join(
        documents
    )


    answer = generate_answer(
        question,
        context
    )


    sources = []


    for index, document in enumerate(documents):

        metadata = (
            metadatas[index]
            if index < len(metadatas)
            else {}
        )


        distance = (
            distances[index]
            if index < len(distances)
            else None
        )


        similarity = None


        if distance is not None:

            similarity = round(
                max(0, 1 - distance),
                4
            )


        sources.append({
            "filename": metadata.get(
                "filename",
                "未知文档"
            ),
            "content": document,
            "score": similarity
        })


    return {
        "question": question,
        "answer": answer,
        "sources": sources
    }


@app.get("/files")
def list_files():

    return get_files()


@app.delete("/files/{filename}")
def delete_file(filename: str):

    file_path = os.path.join(
        UPLOAD_DIR,
        filename
    )


    # 删除本地文件

    if os.path.exists(file_path):

        os.remove(file_path)



    # 删除向量库

    deleted_chunks = delete_documents(
        filename
    )


    # 删除数据库记录

    delete_file_record(
        filename
    )


    return {
        "filename": filename,
        "deleted_chunks": deleted_chunks,
        "message": "文件删除成功"
    }