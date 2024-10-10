import torch
from transformers import GPT2Tokenizer, GPT2LMHeadModel
import logging
import re

from prompt_manager import PromptManager

# Configuração do logging
logging.basicConfig(level=logging.INFO)

# Carregar o tokenizer e o modelo GPT-2
tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
model = GPT2LMHeadModel.from_pretrained('gpt2')

# Definir comprimento máximo de entrada e resposta
MAX_INPUT_LENGTH = 100
MAX_OUTPUT_LENGTH = 300

# Palavras-chave para filtrar respostas indesejadas
SENSITIVE_KEYWORDS = [
    'morte', 'morto', 'falecimento', 'sexo', 'sexualidade', 'violência', 'assassinato',
    'suicídio', 'drogas', 'abuso', 'tráfico', 'crime', 'esquizofrenia', 'doença mental',
    'vírus', 'epidemia', 'pandemia', 'acidente', 'trauma', 'tortura', 'aborto', 'autópsia',
    'câncer', 'tumor', 'hospital', 'paliativo', 'agonia', 'sofrimento', 'violação',
    'assédio', 'harassment', 'abuso sexual', 'estupro', 'assassinato', 'sequestro', 'radiação',
    'veneno', 'armas', 'tiroteio', 'guerra', 'terrorismo', 'perseguição', 'separação', 'divórcio'
]


def contains_sensitive_content(text: str) -> bool:
    """
    Verifica se o texto contém palavras ou frases sensíveis.

    Args:
        text (str): O texto a ser verificado.

    Returns:
        bool: Retorna True se o texto contiver conteúdo sensível, caso contrário, False.
    """
    return any(keyword in text.lower() for keyword in SENSITIVE_KEYWORDS)


def generate_response(question: str, context: str) -> str:
    """
    Gera uma resposta para a pergunta dada, com base no contexto fornecido.

    Args:
        question (str): A pergunta a ser respondida.
        context (str): O contexto que será usado para gerar a resposta.

    Returns:
        str: A resposta gerada pelo modelo GPT-2.
    """
    # Cria o prompt com a pergunta e o contexto
    prompt = (f"Se a pergunta é sobre um conceito, uma prática recomendada, ou uma abordagem específica, ofereça uma "
              f"explicação clara. "
              f"{context}\nQuestion: {question}\nAnswer:")

    # Tokeniza o prompt
    inputs = tokenizer.encode(prompt, return_tensors='pt')
    attention_mask = torch.ones(inputs.shape, dtype=torch.long)

    # Truncar o prompt se for muito longo
    if inputs.shape[1] > MAX_INPUT_LENGTH:
        inputs = inputs[:, -MAX_INPUT_LENGTH:]

    # Gerar resposta
    outputs = model.generate(
        inputs,
        max_length=MAX_INPUT_LENGTH + MAX_OUTPUT_LENGTH,
        num_return_sequences=1,
        temperature=0.3,
        top_k=15,
        top_p=0.2,
        repetition_penalty=3.9,
        pad_token_id=tokenizer.eos_token_id,
        do_sample=True
    )

    # Decodificar a resposta
    response_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    # Remover o prompt da resposta
    response_text = response_text[len(prompt):].strip()
    logging.info(f'Gerando resposta: {response_text}')

    # Filtrar respostas sensíveis
    if contains_sensitive_content(response_text):
        response_text = "Desculpe, não consigo fornecer uma resposta para esta pergunta."

    # Responder se não conseguiu entender
    if not response_text or "Desculpe, não consegui entender sua pergunta" in response_text:
        response_text = "Desculpe, não consegui entender sua pergunta. Por favor, tente novamente."

    return response_text
