from googletrans import Translator
import logging


class TranslationService:
    def __init__(self):
        """
        Inicializa o serviço de tradução com um tradutor do Google.
        """
        self.translator = Translator()

    def translate_to_portuguese(self, text: str) -> str:
        """
        Traduz o texto fornecido para o português, com limite de 1600 caracteres.

        Args:
            text (str): O texto a ser traduzido.

        Returns:
            str: O texto traduzido para o português, ou uma mensagem de erro em caso de falha.
        """
        # Trunca o texto para não exceder 1600 caracteres
        if len(text) > 1600:
            text = text[:1600]

        try:
            # Realiza a tradução do texto para o português
            translated = self.translator.translate(text, dest='pt')
            return translated.text
        except Exception as e:
            # Registra um erro se a tradução falhar
            logging.error(f'Error translating text: {str(e)}')
            return "Desculpe, ocorreu um erro ao traduzir a resposta."


# Instanciar o serviço de tradução globalmente
translation_service = TranslationService()
