from pathlib import Path
from typing import Optional

import fitz
from langchain_community.document_loaders import TextLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from src.langchain_section.config.setting import setting

SUPPORTED_EXTENSIONS = {".txt", ".pdf"}


def load_pdf_with_tables(file_path: Path) -> list[Document]:
    """Carga PDF preservando estructura de tablas con pymupdf"""
    docs = []
    pdf = fitz.open(str(file_path))

    for page_num, page in enumerate(pdf):  # type: ignore
        blocks = page.get_text("blocks")
        blocks.sort(key=lambda b: (b[1], b[0]))

        page_text = "\n".join(block[4].strip() for block in blocks if block[4].strip())

        if page_text:
            docs.append(
                Document(
                    page_content=page_text,
                    metadata={
                        "file_name": file_path.name,
                        "file_type": "pdf",
                        "page": page_num,
                        "source": str(file_path),
                    },
                )
            )

    pdf.close()
    return docs


def load_file(file_path: Path) -> list[Document]:
    """Carga un archivo y retorna una lista de Documents de Langchain"""
    if not file_path.exists():
        raise FileNotFoundError(f"Archivo no encontrado: {file_path}")

    extension = file_path.suffix.lower()
    if extension not in SUPPORTED_EXTENSIONS:
        raise ValueError(f"Extensión '{extension}' no soportada.")

    print(f" Cargando: {file_path.name}", end=" ")
    docs: list[Document] = []

    if extension == ".pdf":
        docs = load_pdf_with_tables(file_path)

    elif extension == ".txt":
        loader = TextLoader(str(file_path), encoding="utf-8")
        docs = loader.load()
        for doc in docs:
            doc.metadata.update(
                {
                    "source": str(file_path),
                    "file_name": file_path.name,
                    "file_type": "txt",
                }
            )

    print(f"→ {len(docs)} página/s")
    return docs


def load_directory(directory_path: Path) -> list[Document]:
    """Carga todos los archivos soportados en una carpeta"""
    if not directory_path.exists():
        directory_path.mkdir(parents=True, exist_ok=True)
        print(f"Carpeta creada: {directory_path}")
        print("Agrega archivos .txt o .pdf y vuelve a ejecutar")
        return []

    all_files = []
    for ext in SUPPORTED_EXTENSIONS:
        all_files.extend(directory_path.glob(f"*{ext}"))
        all_files.extend(directory_path.glob(f"*{ext.upper()}"))
    all_files = list(set(all_files))

    if not all_files:
        print(f" No se encontraron archivos en: {directory_path}")
        print("Agrega archivos .txt o .pdf y vuelve a ejecutar")
        return []

    print(f"Archivos encontrados en {directory_path}:")
    all_docs = []
    errors = []

    for file_path in sorted(all_files):
        try:
            docs = load_file(file_path)
            all_docs.extend(docs)
        except Exception as e:
            errors.append((file_path.name, str(e)))
            print(f" Error cargando {file_path.name}: {e}")

    if errors:
        print(f"\n ❌ {len(errors)} archivo(s) con error, ✅ {len(all_docs)} cargados.")
    else:
        print(f"\n ✅ {len(all_files)} archivo(s) → {len(all_docs)} páginas totales")

    return all_docs


def split_documents(
    docs: list[Document],
    chunk_size: Optional[int] = None,
    chunk_overlap: Optional[int] = None,
) -> list[Document]:
    """Divide los documentos en chunks para indexación"""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size or setting.CHUNK_SIZE,
        chunk_overlap=chunk_overlap or setting.CHUNK_OVERLAP,
        separators=["\n\n", "\n", ". ", " ", ""],
        add_start_index=True,
    )
    chunks = splitter.split_documents(docs)
    print(
        f"{len(docs)} página/s → {len(chunks)} chunks "
        f"(tamaño: ~{chunk_size or setting.CHUNK_SIZE} chars, "
        f"overlap: {chunk_overlap or setting.CHUNK_OVERLAP})"
    )
    return chunks
