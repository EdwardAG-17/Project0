from pymongo import MongoClient #importamos la clase para establecer la conexión con MongoDB.

#Base de Datos Local
"""
db_client = MongoClient().local #como estamos trabajando en local no le pasamos parámetros.
#Si le damos el .local nos conecta a la base de datos local directamente, no sería necesario mencionarlo cuando llamamos al db en "users_db.py"
#(solo porque trabajamos en local, en un servidor remoto, tendríamos que especificar el db al que queremos conectarnos).
"""

#Base de Datos Remota
db_client = MongoClient(
    "mongodb+srv://edward1720:Projecto1MongodbAtlas@cluster0.ku6bo6m.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0").test