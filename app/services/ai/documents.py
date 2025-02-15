import os
from typing import Optional, Dict, Any
import PyPDF2
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI

class DocumentAnalysisService:
    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        self.embeddings = OpenAIEmbeddings()
        self.llm = OpenAI(temperature=0)

    async def analyze_pdf(
        self,
        file_path: str,
        queries: Optional[list[str]] = None
    ) -> Dict[str, Any]:
        """
        Analyse un document PDF et répond à des questions spécifiques si fournies.
        """
        try:
            # Charger et analyser le PDF
            loader = PyPDFLoader(file_path)
            pages = loader.load()
            
            # Obtenir le nombre de pages
            with open(file_path, 'rb') as file:
                pdf = PyPDF2.PdfReader(file)
                page_count = len(pdf.pages)

            # Diviser le texte en chunks
            docs = self.text_splitter.split_documents(pages)
            
            # Créer une base de connaissances vectorielle
            vectorstore = FAISS.from_documents(docs, self.embeddings)
            
            results = {
                "page_count": page_count,
                "document_type": "pdf",
                "analysis": {}
            }

            # Si des questions sont fournies, y répondre
            if queries:
                qa_chain = load_qa_chain(self.llm, chain_type="stuff")
                for query in queries:
                    docs = vectorstore.similarity_search(query)
                    results["analysis"][query] = qa_chain.run(input_documents=docs, question=query)

            return results
        except Exception as e:
            raise Exception(f"Erreur lors de l'analyse du document: {str(e)}")

    async def extract_text(self, file_path: str) -> str:
        """
        Extrait le texte brut d'un document PDF.
        """
        try:
            loader = PyPDFLoader(file_path)
            pages = loader.load()
            return "\n".join([page.page_content for page in pages])
        except Exception as e:
            raise Exception(f"Erreur lors de l'extraction du texte: {str(e)}")
