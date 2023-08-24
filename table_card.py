import pandas as pd
import argparse
import os

parser = argparse.ArgumentParser(
    description='Bu')
parser.add_argument('-csv', '--csv', metavar='', type=str, required=True,
                    help='path to the card_gene_count.csv (from panvita results)')
parser.add_argument('-tsv', '--tsv', metavar='', type=str, required=True,
                    help='path to the aro_index.tsv (From panvita database)')
parser.add_argument('-o', '--output', metavar='', type=str, required=True,
                    help='path to where you want the output results')

args = parser.parse_args()

folder_input_csv = os.path.expanduser(f'{args.csv}')
folder_input_tsv = os.path.expanduser(f'{args.tsv}')
folder_output = os.path.expanduser(f'{args.output}') + "resultados_do_script_card.csv"

# Carrega os arquivos CSV em DataFrames do Pandas
panvita_gene_count = pd.read_csv(f'{folder_input_csv}', sep=';')
database_card_tsv = pd.read_csv(f'{folder_input_tsv}', sep='\t')

# Lista de genes do primeiro arquivo
genes = panvita_gene_count['Genes']


# criando uma lista de genes para usar
lista_de_genes = []
for cada_gene in genes:
    lista_de_genes.append(cada_gene)

""" BUSCANDO AS INFOS DOS GENES NO .TSV """

def buscador_gene_compound(lista_de_genes, database_card_tsv, gene_to_drug_class, gene_to_resistence_mechanism):
    # Itera sobre cada gene na lista
    for cada_gene in lista_de_genes:
        filtro = database_card_tsv["CARD Short Name"] == cada_gene
        if filtro.any():
            valor_drug_class = database_card_tsv.loc[filtro, "Drug Class"].iloc[0]
            gene_to_drug_class[cada_gene] = valor_drug_class
            
            valor_resistence_mechanism = database_card_tsv.loc[filtro, "Resistance Mechanism"].iloc[0]
            gene_to_resistence_mechanism[cada_gene] = valor_resistence_mechanism
            
gene_to_drug_class = {}
gene_to_resistence_mechanism = {}

# Chama a função para buscar os resultados e atualizar os dicionários
buscador_gene_compound(lista_de_genes, database_card_tsv, gene_to_drug_class, gene_to_resistence_mechanism)

drug_class = []
for valor in gene_to_drug_class.values():
    drug_class.append(valor)

resistence_mechanism = []
for valor in gene_to_resistence_mechanism.values():
    resistence_mechanism.append(valor)
    
    
""" Criar um DataFrame do pandas para a tabela """

data = {
    "Gene": lista_de_genes,
    "Resistence Mechanism": resistence_mechanism,
    "Drug Class": drug_class
    
    
}
df = pd.DataFrame(data)

# Salvar a tabela em um arquivo CSV
df.to_csv(f'{folder_output}', index=False)



