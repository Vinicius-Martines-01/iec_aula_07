# 1. Use uma imagem base Python oficial leve
FROM python:3.11-slim

# 2. Defina variáveis de ambiente para evitar arquivos .pyc e buffer de logs
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3. Defina o diretório de trabalho
WORKDIR /app


# 5. Copie o restante do código da aplicação
COPY . .

EXPOSE 3000
# 6. Comando para rodar a aplicação (exemplo para um script)
CMD ["python", "main.py"]
