import PyPDF2


def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extrai texto de um arquivo PDF.

    Args:
        pdf_path (str): O caminho para o arquivo PDF do qual o texto será extraído.

    Returns:
        str: O texto extraído do PDF. Se ocorrer algum erro, retorna uma string vazia.
    """
    text = ""
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfFileReader(file)

            # Verifique se o PDF está criptografado
            if reader.isEncrypted:
                try:
                    reader.decrypt('')  # Tenta descriptografar o PDF sem senha
                except Exception as e:
                    print(f"Não foi possível descriptografar o PDF: {e}")
                    return text

            # Extraia texto de cada página
            for page_num in range(reader.numPages):
                page = reader.getPage(page_num)
                page_text = page.extract_text()  # Extrai texto da página
                if page_text:
                    text += page_text  # Adiciona o texto extraído
                else:
                    print(f"Texto não extraído da página {page_num + 1}")

    except FileNotFoundError:
        print(f"Arquivo não encontrado: {pdf_path}")
    except PyPDF2.PdfReadError as e:
        print(f"Erro ao ler o PDF: {e}")
    except Exception as e:
        print(f"Erro inesperado: {e}")

    return text
