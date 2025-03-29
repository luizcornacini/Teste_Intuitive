import tabula
import pandas as pd
import zipfile
import os

# Função para extrair dados do PDF
def extrair_dados_pdf(pdf_file):
    """
    Extrai todas as tabelas de um arquivo PDF e as concatena em um único DataFrame.
    """
    try:
        # Usando tabula para extrair todas as tabelas do PDF
        print(f"Extraindo dados do arquivo PDF: {pdf_file}")
        tabelas = tabula.read_pdf(pdf_file, pages='all', multiple_tables=True, lattice=True)
        
        # Caso o PDF tenha tabelas em várias páginas, concatenamos todas
        if len(tabelas) == 0:
            raise ValueError("Nenhuma tabela foi encontrada no PDF.")
        
        # Concatenando todas as tabelas extraídas em um único DataFrame
        df = pd.concat(tabelas, ignore_index=True)
        print(f"Dados extraídos com sucesso. Total de {len(df)} linhas.")
        return df
    except Exception as e:
        print(f"Erro ao extrair dados do PDF: {e}")
        raise

# Função para substituir abreviações
def substituir_abreviacoes(df):
    """
    Substitui abreviações comuns nas colunas por descrições completas.
    """
    substituicoes = {
        'OD': 'Odontologia',
        'AMB': 'Ambulatório'
    }

    # Substituindo as abreviações nas colunas do DataFrame
    for abreviacao, descricao in substituicoes.items():
        df.replace(abreviacao, descricao, inplace=True)
    
    print("Abreviações substituídas com sucesso.")
    return df

# Função para salvar em CSV e compactar
def salvar_e_compactar(df, nome_arquivo):
    """
    Salva o DataFrame em formato CSV e compacta esse arquivo em um arquivo ZIP.
    """
    # Caminho para o arquivo CSV
    csv_file = f'{nome_arquivo}.csv'

    try:
        # Salvando o DataFrame em CSV
        df.to_csv(csv_file, index=False, encoding='utf-8')
        print(f"Arquivo CSV salvo como {csv_file}.")
        
        # Compactando o arquivo CSV em um arquivo ZIP
        zip_filename = f'Teste_{nome_arquivo}.zip'
        with zipfile.ZipFile(zip_filename, 'w') as zipf:
            zipf.write(csv_file, os.path.basename(csv_file))
        
        # Removendo o CSV após compactação para economizar espaço
        os.remove(csv_file)
        print(f"Arquivo ZIP criado: {zip_filename}")
    except Exception as e:
        print(f"Erro ao salvar ou compactar os dados: {e}")
        raise

# Função principal para orquestrar as etapas
def transformar_dados(pdf_file, nome_arquivo):
    """
    Executa todo o processo de transformação: extrai dados, substitui abreviações,
    salva em CSV e compacta em ZIP.
    """
    try:
        # Etapa 1: Extrair os dados da tabela do PDF
        df = extrair_dados_pdf(pdf_file)
        
        # Etapa 2: Substituir abreviações nas colunas
        df = substituir_abreviacoes(df)
        
        # Etapa 3: Salvar como CSV e compactar em ZIP
        salvar_e_compactar(df, nome_arquivo)
        
    except Exception as e:
        print(f"Erro durante o processo de transformação de dados: {e}")

# Chamada principal
if __name__ == "__main__":
    # Caminho para o PDF do Anexo I (coloque o caminho correto do arquivo PDF)
    pdf_file = r'file:///C:/Users/Luiz/Desktop/teste/anexos/Anexo_I_Rol_2021RN_465.2021_RN627L.2024.pdf'
    
    # Nome do arquivo a ser gerado (use seu nome ou algo descritivo)
    nome_arquivo = 'Luiz_Carlos_Cornacini_Filho'
    
    # Executando a transformação de dados
    transformar_dados(pdf_file, nome_arquivo)
