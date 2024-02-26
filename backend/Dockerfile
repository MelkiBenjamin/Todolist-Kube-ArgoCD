From python:alpine3.19

# aller au dossier app
workdir /app

# copier tout les fichier requis
COPY . .

# installer les modules python
RUN pip install -r requirements.txt

# port exposer de l'aplication 
EXPOSE 8000

# execute l'aplication au demarage du container
CMD ["python3", "app.py" ]
