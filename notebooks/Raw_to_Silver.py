# Databricks notebook source
#O código fornecido está utilizando o comando dbutils.fs.mount para montar um ponto de montagem (mount point) no Databricks, permitindo o acesso aos dados armazenados no Azure Data Lake Storage. Aqui está uma explicação passo a passo do código:
#source: Especifica a URI do seu Data Lake Storage. No exemplo, está usando o protocolo wasbs (Azure Blob Storage com suporte para HTTPS).
#mount_point: Indica o caminho onde o Data Lake será montado no sistema de arquivos do Databricks. No exemplo, está sendo montado em /mnt/imoveis/.
#extra_configs: Permite fornecer configurações adicionais. Neste caso, está sendo utilizado para passar a chave de conta de armazenamento como uma configuração adicional.
#scopo nós criamos a conexão no databricks e a key, vem do key vault azure

# COMMAND ----------

dbutils.fs.mount(
    source = "wasbs://imoveis@sadatalakerafael.blob.core.windows.net/"
    ,mount_point = "/mnt/imoveis/"
    ,extra_configs = {"fs.azure.account.key.sadatalakerafael.blob.core.windows.net" :dbutils.secrets.get(scope = "scopo-kv-kvdatabricks-datafactory", key = "secret-batabricks")}
)

# COMMAND ----------

# visualizando oq tem dentro do container imoveis
dbutils.fs.ls("/mnt/imoveis")

# COMMAND ----------

# visualizando oq tem dentro da pasta raw
dbutils.fs.ls("/mnt/imoveis/Raw")

# COMMAND ----------

local = "dbfs:/mnt/imoveis/Raw/dados_brutos_imoveis.json"
dados = spark.read.json(local)

# COMMAND ----------

display(dados)

# COMMAND ----------

#dropando colunas 
dados = dados.drop("imagens", "usuario")
display(dados)

# COMMAND ----------

#Criando coluna de identificação
from pyspark.sql.functions import col


# COMMAND ----------

# estou criando uma coluna com o id de cada linha
camada_silver = dados.withColumn("id", col("anuncio.id"))
display(camada_silver)

# COMMAND ----------

# Salvando em formato Delta na pasta especificada
salvando_silver = "dbfs:/mnt/imoveis/Silver/dados_tratado"
camada_silver.write.format("delta").mode("overwrite").save(salvando_silver)


# COMMAND ----------


