#CREAREMOS UNA API PARA USUARIOS USANDO MONGODB
#en la extension de mondoDB para establecer la CONEXIÓN con el servidor local, usamos "mongodb://localhost"
#INSTALAMOS: "pip install pymongo" 
#para EJECUTARLO en el cmd: sudo mongod --dbpath "path/de/la/base/de/datos" 
from fastapi import APIRouter, HTTPException, status, HTTPException, FastAPI
from pydantic import BaseModel

from db.models.user import User #importamos la clase User de models, que nos permite crear un modelo de datos para los usuarios.
from db.client import db_client #importamos la clase db_client de la base de datos, que nos permite conectarnos a la base de datos.
from db.schemas.user import user_schema, user_schema_list #importamos la funcion user_schema de schemas, que nos permite transformar los datos.
from bson import ObjectId #importamos la clase ObjectId  que nos permite trabajar con los ids de mongodb.


router = APIRouter(prefix="/usersdb" 
                   ,tags=["users"]
                   ,responses={status.HTTP_404_NOT_FOUND: {"description": "Not Found"}})

#GET:
@router.get("", response_model=list[User]) #la dejo vacia ya que ya tiene predefinido el prefijo "/usersdb"
async def users():
    return user_schema_list(db_client.users.find()) #retorna todos los usuarios que se encuentran en la base de datos, con la función user_schema_list.
#find es un method que nos permite buscar todos los usuarios en la base de datos.


#CREAMOS FUNCIÓN: "search_user" función generica para todos los operadores, para tener un criterio de busqueda segun el email.
def search_user(field: str, key): #field es el campo por el que se va a buscar y key es el valor que se va a buscar.
    try:
        user = db_client.users.find_one({field: key}) #buscamos el campo y el valor en la base de datos.
        return User(**user_schema(user)) #retornamos el user del email ya transformado a un objeto de tipo User.
    except:
        return {"error": "No se ha encontrado el user"}
#cuando la usemos solo debemos especificar el campo (email, username, id) y el valor que queremos buscar.

"""
"search_user_by_email" para tener un criterio de busqueda que si es especifico, segun el email del usuario.
def search_user_by_email(email: str):
    try:
        user = db_client.users.find_one({"email": email}) #buscamos el email en la base de datos.
        return User(**user_schema(user)) #si se encuentra el email, lo transformamos a un objeto de tipo User y lo retornamos.
    except:
        return {"error": "No se ha encontrado el email"} #si no se encuentra el email se retorna un error.
"""

#POST:vamos agregar UN usuario a la base de datos (etiquetamos el search_user que ya no usaremos así)
@router.post("", response_model=User, status_code=status.HTTP_201_CREATED) 
async def user(user: User): 
    if type(search_user("email",user.email)) == User: #si no se encuentra el email, se sigue el flujo, d elo contrario levanta el error.
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El usuario ya existe")
    
    user_dict = dict(user) #creamos un diccionario con los datos del usuario que nos llega por el body.
    del user_dict["id"] #eliminamos el id que nos entraria cómo null por defecto en el dict, así mongodb se encargara de generarlo el mismo.

    id = db_client.users.insert_one(user_dict).inserted_id #llamamos a db_client y le damos el archivero y nombre de la colección que se creara para guardar al info.
    #el method para agregar el usuario, el usario a guardar y agragamos la propiedad que inserta el id que genera mongodb.

    new_user = user_schema(db_client.users.find_one({"_id": id})) #buscamos el id que se generó en el db para comprobar que se guardó correctamente usadno la funcion de transformacion (user_schema) con el method (find_one).
    #user_schema tranforma el obejto porque si no nos devolveria un objeto distinto a "User" (se pone _id porque es el id que genera mongodb al guardar el usuario).

    return User(**new_user) #retornamos el nuevo usuario que se guardó en la base de datos, transformado a un objeto de tipo User.


#PARAMETROS PARA EL PATH (buscar un usuario por su id)
@router.get("/{id}") 
async def user(id: str): 
    return search_user("_id", ObjectId(id)) #se comprueba el id en db usando ObjectId


#PUT: actualizar un usuario
@router.put("") 
async def user(user: User):
    user_dict = dict(user) #creamos un diccionario con los datos del usuario que nos llega por el body.
    del user_dict["id"] #eliminamos el id para que este elemento no se actualice.
    try:
        db_client.users.find_one_and_replace({"_id": ObjectId(user.id)}, user_dict) #actualizamos el usuario en la base de datos, si existe, se actualiza.
    except:
        return {"error": "No se ha actualizado el user"}
    return search_user("_id", ObjectId(user.id)) #retornamos el usuario actualizado


#DELETE: borrar un usuario por su id
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT) 
async def user(id: str): 
    found = db_client.users.find_one_and_delete({"_id": ObjectId(id)}) #buscamos el id en la base de datos y lo eliminamos.
    if not found: #si no se encuentra el id, se retorna un error.
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user no encontrado")


