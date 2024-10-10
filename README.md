# IA Response

IA Response é um projeto de inteligência artificial que visa gerar respostas a perguntas com base em textos extraídos de livros em formato PDF. O sistema utiliza o modelo GPT-2 para responder às consultas, traduzindo as respostas para o português e filtrando conteúdos sensíveis.

## Funcionalidades

- **Carregamento de Livros:** Extração de texto de arquivos PDF armazenados em uma pasta local.
- **Geração de Respostas:** Utiliza o modelo GPT-2 para responder a perguntas baseadas no texto extraído dos livros.
- **Tradução:** As respostas geradas são traduzidas para o português.
- **Filtragem de Conteúdo Sensível:** Respostas com conteúdo sensível são detectadas e filtradas.

## Estrutura do Projeto

- **app.py:** Código principal do servidor Flask, que gerencia endpoints para carregar livros e gerar respostas.
- **utils.py:** Função para extrair texto de arquivos PDF.
- **prompt_manager.py:** Classe que gera prompts detalhados para o modelo GPT-2.
- **gpt_service.py:** Função que gera respostas usando o modelo GPT-2.
- **translation_service.py:** Serviço que realiza a tradução de texto para o português.

## Pré-requisitos

- Python 3.7 ou superior
- Bibliotecas necessárias:
  ```bash
  pip install flask transformers googletrans PyPDF2 torch
## Passos para Clonar o Repositório

### 1. Instale o Git LFS:

Se ainda não tiver o Git LFS instalado, você pode instalá-lo seguindo as instruções do site oficial: [git-lfs.com](https://git-lfs.com).

- Para sistemas baseados em Debian (como Ubuntu):
    ```bash
    sudo apt-get install git-lfs
    ```
  
- Para sistemas baseados em Red Hat (como CentOS):
    ```bash
    sudo yum install git-lfs
    ```

- Para macOS, use Homebrew:
    ```bash
    brew install git-lfs
    ```

### 2. Inicialize o Git LFS:

Após a instalação, inicialize o Git LFS em sua máquina:
```bash
git lfs install
```

## Clonar o Repositório

Agora você pode clonar o repositório do GPT-2:

```bash
git clone https://huggingface.co/openai-community/gpt2
```
Ou, se você quiser clonar apenas os ponteiros dos arquivos grandes (não os arquivos em si), use o seguinte comando:

```bash
GIT_LFS_SKIP_SMUDGE=1 git clone https://huggingface.co/openai-community/gpt2
```

## Notas Adicionais

- **Clonar com Git LFS:** Se você clonar normalmente, os arquivos grandes (como pesos do modelo) serão baixados automaticamente.
- **Clonar sem os arquivos grandes:** Usar `GIT_LFS_SKIP_SMUDGE=1` é útil se você estiver com pouco espaço em disco ou se não precisar dos arquivos grandes imediatamente. Você pode baixar esses arquivos mais tarde, se necessário, usando `git lfs pull`.








