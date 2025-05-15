#CREAREMOS UNA API PARA USUARIOS
from fastapi import FastAPI


#CREAMOS EL ROUTER:
from fastapi import APIRouter #importamos el modulo APIRouter de fastapi para crear un router.

#IMPORTAMOS LA CLASE BASEMODEL de PYDANTIC: esta clase nos permite crear modelos de datos que se pueden usar para validar y serializar datos
#en este caso nos servira para definir una entidad(los usuarios).
from pydantic import BaseModel
"""
Normalmente usamos la variable app asignanadole las funciones de FastAPI, pero en este caso creamos un router para poder usarlo en el main.py y no tener que repetir el mismo codigo.
app = FastAPI() #le asignamos a una variable las funciones de FastAPI
"""

#En este caso llamamos a la api por medio de @router, ya no de app, ya que no es la raiz principal de la API.
#le asignamos a una variable las funciones de APIRouter, que nos permite crear un router para nuestra API.
router = APIRouter(prefix="/users" 
                   ,tags=["users"]
                   ,responses={404: {"description": "Not Found"}})

#Esta es la forma menos habitual de crear nuestro API:

#GET: una operacion que nos permite leer/obtener datos.
@router.get("/usersjson")
async def usersjson():
    return  [{"name": "Edward", "surname": "Alcala", "age": 17, "url": "https://edward.com"},
             {"name": "Rex", "surname": "Star", "age": 17, "url": "https://rex.com"},
             {"name": "Santiago", "surname": "Gallo", "age": 17, "url": "https://santiago.com"}]
#usamos el get para leer los datos de usuarios que pusimos en forma key:value, haciendo un json.

#PARA CREAR UN API MAS EFICIENTE Y ORGANIZADO:
#DEFINIMOS LA ENTIDAD: a partir de "class", asignamos el nombre user y podemos darle el atributo "basemodel", que le da la capacidad de crear una entidad.
class User(BaseModel):
    id: int
    name: str
    surname: str
    age: int
    url: str
#lo que contiene el "class" son los datos que queremos y categorizamos el tipo de dato que debera contener.

#Definimos dentro de una variablelos usuarios que queremos que se muestren en el API.
users_list = [User(id= 1, name="Edward", surname="Alcala", age=17, url="https://edward.com"),
              User(id=2, name="Rex", surname="Star", age=17, url="https://rex.com"),
              User(id=3, name="Santiago", surname="Gallo", age=17, url="https://santiago.com")]

#Creamos nuestra funcion para mostrar los usuarios en el API: (mucho mas eficiente, organizado y corto que el anterior)
@router.get("") #la dejo vacia ya que ya tiene predefinido el prefijo "/users"
async def users():
    return users_list


#PARAMETROS PARA PATH Y QUERY
#Creamos una funcion que nos permita buscar un usuario por su id:
def search_user(id: int):
    users = filter(lambda user: user.id == id, users_list)#FILTER: funcion de orden superior que nos permite filtrar datos de una lista
    #en este caso hacemos un lambda que identifica al usuario por su id, el contenido esta en userl_list.
    try:
        return list(users)[0]#FINALEMENTE se retornan la variable users en forma de lista, le damos el [0], para que solo acceda al primer resultado.
    except:
        return {"error": "No se ha encontrado el usuario"}
#Hacemos un try para evitar que el servidor se caiga si no encuentra un usuario asociado a X id.
#El except se encarga de dar el mensaje si no se encuentra el usuario.


#PARAMETROS PARA EL PATH: podemos mostrar un usuario en especifico, a traves del valor de su id.
@router.get("/{id}") #le agregamos el parametro /{id}
async def user(id: int): #establecemos que en la clase user, el parametro id es de tipo int.
    return search_user(id) #le damos el atributo id que la variable search_user necesita para funcionar.
#para probarlo, le agregamos al path el id que deseamos: http://127.0.0.1:8000/user/1

#PARAMETROS PARA EL QUERY: nos permiten igualar un key y un value desde la url a diferencia del path, que solo nos permite igualar un value (/user/1)
@router.get("/") #solo le agregamos un /
async def user(id: int): 
    return search_user(id)
#para probarlo http://127.0.0.1:8000/user/?id=1 #le damos el key(id) y el value que busquemos.


#PUT: nos permite actualizar datos en el API
#Actualizamos un usuario en el API:
@router.put("") 
async def user(user: User):
    found = False #creamos una variable que nos permitira saber si el usuario fue encontrado.
    for index, saved_user in enumerate(users_list): #recorremos la lista de usuarios.
        if saved_user.id == user.id: #si el id del usuario guardado es igual al id del usuario que queremos actualizar.
            users_list[index] = user #actualizamos el usuario.
            found = True #cambiamos el estado de found a True cuando se encuentra el usuario que queremos actualizar.
    if not found: #si no se encuentra el usuario.
        return {"error": "El usuario no se ha actualizado"} #retornamos un mensaje de error.
    else: #si se encuentra el usuario.
        return user #retornamos el usuario actualizado.
#para probarlo, asignamos Put, le agregamos al path en el body escribimos el json la informacion del usuario actualizado.


#DELETE: nos permite eliminar datos en el API
@router.delete("/{id}") #le agregamos el parametro /{id} que es obligatorio para poder eliminar un usuario.
async def user(id: int): #le damos el atributo id con el que identificaremos al usuario que queremos eliminar (debe ser de tipo int)
    found = False
    for index, saved_user in enumerate(users_list): 
        if saved_user.id == id: #se comprueba si hay un id igual al id del usuario que queremos eliminar.
            del users_list[index] #eliminamos el usuario.
            found = True #cambiamos el estado de found a True cuando se encuentra el usuario que queremos eliminar.
            return ({"message": "Usuario eliminado"})
    else:
        return {"error": "No se ha eliminado el usuario"} #retornamos un mensaje de error si no se encuentra el usuario.
#para probarlo, le agregamos al path con el valor del id a eliminar ej: http://127.0.0.1:8000/user/4


"""
#POST: nos permite crear nuevos datos en el API

#Crearemos un nuevo usario en el API:
@router.post("/") #le agregamos un / para que sea mas facil de identificar el path.

async def user(user: User): #le damos el atributo user, que debe ser de la class User.

    if type(search_user(user.id)) == User: #si el tipo de dato (user.id)que retorna la funcion search_user, es igual a uno de la class User.
        
        return {"error": "El usuario ya existe"} #retornamos un mensaje de error, ya que ya existe un usario con ese id.
    else:
        users_list.append(user) #si no existe, agregamos el nuevo usuario a la lista de usuarios.

        return user #retornamos el usuario que se acaba de agregar.

#Seleccionando que es un POST y desde el url agregamos el path y en el body escribimos el json la informacion del nuevo usuario.
"""


#HTTP STATUS CODE: nos permite conocer el estado del codigo, los usaremos en la funciones de nuestro API.
from fastapi import HTTPException #importamos la clase HTTPException de fastapi para manejar los errores.

#en este post creamos un nuevo usuario, se le establece el parametros del status_code 201, que indica que se ha creado un nuevo recurso.
@router.post("/", response_model=User, status_code=201) #le agregamos el response_model, que nos permite definir el modelo de respuesta que queremos que retorne la funcion.
async def user(user: User): 
    if type(search_user(user.id)) == User: 
        raise HTTPException(status_code=404, detail="El usuario ya existe") #si el usuario ya existe, lanzamos una excepcion con el status code.
    #Raise: lanza la excepcion/error en el programa que se esta ejecutando.
    #Detail: es otro parametro que nos permite dar un mensaje de error.
    else:
        users_list.append(user) 
        return user
