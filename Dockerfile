# Imagem base
FROM python:3.10-slim

# Diretório de trabalho dentro do container
WORKDIR /app

# Copia os arquivos para dentro do container
COPY . .

RUN apt-get update && apt-get install -y imagemagick

# Instala dependências
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copia a política ajustada para o local correto
COPY utils/policy.xml /etc/ImageMagick-6/policy.xml

# Expõe a porta que o Gunicorn vai usar
EXPOSE 5000

# Comando para iniciar a API com Gunicorn
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
