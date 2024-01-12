# Databricks notebook source
# visualizando oq tem dentro da Camada Silver
dbutils.fs.ls("/mnt/imoveis/Silver")

# COMMAND ----------

# lendo os arquivos da camada silver
caminho = "dbfs:/mnt/imoveis/Silver/dados_tratado"
df = spark.read.format("delta").load(caminho)

# COMMAND ----------

display(df)

# COMMAND ----------

dados_detalhados = df.select("anuncio.*", "anuncio.endereco.*")
display(dados_detalhados)

# COMMAND ----------

#Removendo colunas
dados_detalhados = dados_detalhados.drop("caracteristicas", "endereco")

# COMMAND ----------

display(dados_detalhados)

# COMMAND ----------

# Salvando em formato Delta na pasta Gold
salvando_gold = "dbfs:/mnt/imoveis/Gold/dataset_imoveis"
dados_detalhados.write.format("delta").mode("overwrite").save(salvando_gold)


# COMMAND ----------


