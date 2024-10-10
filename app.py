import os
import logging
from flask import Flask, request, jsonify
from utils import extract_text_from_pdf
from prompt_manager import PromptManager
from gpt_service import generate_response
from translation_service import translation_service  # Importar o serviço de tradução

# Configuração de logging
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

# Variável global para armazenar o texto do livro
book_texts = ""

# Caminho para a pasta contendo os PDFs
PDF_FOLDER = ""


def load_books_from_folder(folder_path):
    """
    Carrega o texto de todos os livros em uma pasta.

    Args:
        folder_path (str): O caminho para a pasta contendo os arquivos PDF.

    Global Variables:
        book_texts (str): Variável global que armazena todo o texto extraído dos livros.
    """
    global book_texts
    book_texts = ""  # Reinicia a variável global
    for filename in os.listdir(folder_path):
        if filename.endswith(".pdf"):  # Verifica se o arquivo é um PDF
            file_path = os.path.join(folder_path, filename)
            logging.info(f"Carregando o livro: {file_path}")
            book_texts += extract_text_from_pdf(file_path)  # Extrai texto do PDF e adiciona à variável global


@app.route('/load_books_from_folder', methods=['POST'])
def load_books_from_folder_endpoint():
    """
    Endpoint para carregar livros a partir de uma pasta.

    Método:
        POST
    Respostas:
        - 200: Livros carregados com sucesso.
        - 500: Erro ao carregar os livros.
    """
    try:
        load_books_from_folder(PDF_FOLDER)  # Carrega os livros da pasta definida
        return jsonify({"message": "Books loaded successfully."})
    except Exception as e:
        logging.error(f'Error loading books: {str(e)}')
        return jsonify({"error": str(e)}), 500  # Retorna erro em caso de falha


@app.route('/predict', methods=['POST'])
def predict():
    """
    Endpoint para gerar uma resposta baseada em um texto fornecido.

    Método:
        POST
    Requisições:
        - text (str): O texto a ser processado.

    Respostas:
        - 200: Resposta gerada com sucesso.
        - 400: Erro na solicitação (texto não fornecido).
        - 500: Erro ao gerar a resposta.
    """
    try:
        data = request.get_json()
        text = data.get('text')  # Obtém o texto da solicitação
        logging.info(f'Questão recebida: {text}')

        if not text:
            return jsonify({"error": "Não consegui gerar texto"}), 400  # Retorna erro se o texto não for fornecido

        # Gerar resposta usando a função generate_response
        response_text = generate_response(text, book_texts)

        # Limitar a resposta para 1400 caracteres antes da tradução
        if len(response_text) > 1400:
            response_text = response_text[:1400]

        # Traduzir a resposta para o português
        translated_response = translation_service.translate_to_portuguese(response_text)

        # Verifica se a tradução foi bem-sucedida
        if not translated_response or "Desculpe, não consegui entender sua pergunta" in translated_response:
            translated_response = "Desculpe, não consegui entender sua pergunta. Por favor, tente novamente."

        response = {"resposta": translated_response}
        return jsonify(response)

    except Exception as e:
        logging.error(f'Error generating response: {str(e)}')
        return jsonify({"error": str(e)}), 500  # Retorna erro em caso de falha


if __name__ == '__main__':
    # Executa o servidor Flask na porta 5000
    app.run(port=5000)
