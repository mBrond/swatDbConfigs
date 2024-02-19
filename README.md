# Configurações de BD para análise e uso no SWAT
O presente repositório tem como finalidade facilitar o acesso aos dados do Harmonized World Soil Database (HWSD)
via sqlite, e realizar consultas através do identificador MU_GLOBAL.

##  mdb2sqlite.py
Realiza a conversão de qualquer banco de dados do Microsoft Acess (.mdb) para Sqlite. Imprime na tela o header de cada coluna.
A função contida no arquivo possuí dois parâmetros:
  - filename_in: caminho do arquivo do banco de dados .mdb.
Não inclusão do parâmetro considera o arquivo HWSD.mdb no diretório atual.
  - filename_out: caminho onde o arquivo do banco de dados .sqlite será criado

##  clip_HWSD.ipynb
Chama mdb2sqlite.py e realiza a conversão do banco de dados.
O arquivo consulta na versão sqlite do HWSD as informações dos códigos MU_GLOBAL inseridos.
Os dados consultados são inseridos em um arquivo .csv. Códigos inválidos são desconsiderados. 
É necessário definir as seguintes variáveis para:
  - mu_global: lista com os MU_GLOBAL que serão consultados.
  - csvPath: caminho onde é criado o .csv resultante. Por padrão, o arquivo é nomeado de mu_globalCodes.csv. 
Definição como string vazia cria o arquivo no diretório atual.
  - mdbPath: 
Definição como string vazia cria o arquivo no diretório atual.
  - sqlitePath: caminho e nome do arquivo HWSD.sqlite 
