import os
import requests
from bs4 import BeautifulSoup
import zipfile
from urllib.parse import urljoin

# URL do site
URL = "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-dasociedade/atualizacao-do-rol-de-procedimentos"
# Diretório de saída
OUTPUT_DIR = "anexos"

# Cabeçalhos para simular uma requisição do navegador
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}

def baixar_pdfs():
    # Realiza o GET na URL do site com os cabeçalhos
    response = requests.get(URL, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    # Encontra todos os links de anexos PDF
    links = [a["href"] for a in soup.find_all("a", href=True) if ".pdf" in a["href"]]

    # Imprime todos os links encontrados para depuração
    print("Links encontrados para PDF:")
    for link in links:
        print(link)
    
    # Cria a pasta de saída, caso não exista
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Baixa cada PDF
    for link in links:
        # Garante que o link esteja completo, usando urljoin para combinar a URL base com o link
        pdf_url = urljoin(URL, link)
        
        # Extrai o nome do arquivo PDF a partir do URL
        pdf_name = pdf_url.split("/")[-1]
        pdf_path = os.path.join(OUTPUT_DIR, pdf_name)

        # Baixa o PDF com os cabeçalhos
        pdf_response = requests.get(pdf_url, headers=headers)
        
        # Verifica se o download foi bem-sucedido
        if pdf_response.status_code == 200:
            with open(pdf_path, "wb") as f:
                f.write(pdf_response.content)
            print(f"✅ Baixado: {pdf_name}")
        else:
            print(f"❌ Falha no download: {pdf_name}")

    # Compacta os PDFs em um único arquivo ZIP
    zip_filename = "anexos.zip"
    with zipfile.ZipFile(zip_filename, "w") as zipf:
        for file_name in os.listdir(OUTPUT_DIR):
            zipf.write(os.path.join(OUTPUT_DIR, file_name), file_name)

    print(f"✅ Arquivo ZIP criado: {zip_filename}")

if __name__ == "__main__":
    baixar_pdfs()
