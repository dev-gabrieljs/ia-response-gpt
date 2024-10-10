from utils import extract_text_from_pdf


def load_book(pdf_path):
    """Carrega o texto de um livro a partir de um caminho de arquivo PDF."""
    book_texts = extract_text_from_pdf(pdf_path)
    return book_texts
