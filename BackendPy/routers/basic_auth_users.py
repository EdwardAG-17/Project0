#AUTENTICACIÓN BASICA DE USUARIOS
#importamos FastAPI y BaseModel de pydantic para crear la API y definir el modelo de datos.
from fastapi import FastAPI, APIRouter
from pydantic import BaseModel
from fastapi import HTTPException

from fastapi import Depends, status
#Depends: se utiliza para obtener dependencias de FastAPI, en este caso, si el usario esta o no autenticado.
#status: se utiliza para definir los códigos de estado de las respuestas de la API.

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
#OAuth2PasswordBearer: esquema de autenticación que permite a los usuarios enviar sus credenciales para obtener un token de acceso.
#OAuth2PasswordRequestForm: es el formulario que se utiliza para recibir las credenciales del usuario en una solicitud POST.

router = APIRouter()

#le asignamos una variable al esquema de autenticación y le damos un parametro de url que gestiona la autenticación del usuario.
oauth2 = OAuth2PasswordBearer("/login") #ruta de url para la autenticación del usuario, "login" vendria siendo nuestro token de acceso.


#MODELO DE DATOS para la información de los usuarios.
class User(BaseModel):
    username: str
    full_name: str
    email: str
    disabled: bool

#MODELO DE DATOS para la contraseña del usuario.
class UserDB(User):
    password: str
#Este modelo hereda de la clase User, y le agrega el atributo password.


#BASE DE DATOS simulada para almacenar los usuarios.
users_db = {
    "RexStar17": { #es la entidad que representa al usuario
        "username": "RexStar17",
        "full_name": "Edward Alcala",
        "email": "edwardalcala@alumno.com",
        "disabled": False, #no esta desabilitado
        "password": "12345"  #en caso real, nunca deberiamos guardar la contraseña en claro en la base de datos, debe estar encriptada.
    },
    "RexStar20": {
        "username": "RexStar20",
        "full_name": "Edward Alcala 2",
        "email": "edwardalcala2@alumno.com",
        "disabled": True, #esta desabilitado
        "password": "54321"
    }
}


#FUNCION para buscar al usuario en base de datos completa.
def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])
#**kwargs: esencial para pasar argumento de longitud variable asociados a un key-value, en una función.
#en este caso desempaqueta el diccionario y lo convierte en argumentos de palabra clave.

#FUNCION para buscar el usuario en base de datos, pero sin la contraseña.
def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])

#CREAMOS UN CRITERIO de dependencia para obtener al usuario.
async def current_user(token: str = Depends(oauth2)): #le asignamos un parametro que contenga el token de acceso, el cual depende de que esté autenticado.
    user = search_user(token) #buscamos al usuario en la base de datos.
    if not user: #si no se encuentra levantamos el error.
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                            detail="Credenciales invalidas", 
                            headers={"WWW-Authenticate": "Bearer"})#headers: son los encabezados de la respuesta HTTP, en este caso, le decimos que el tipo de autenticación es Bearer.
    if user.disabled: #en caso de que el usuario esté desabilitado:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                            detail="Usuario desabilitado",)
    return user #si el usuario esta autenticado, retornamos el usuario. 


#OPERACION DE AUTENTICACIÓN:
@router.post("/login") #ruta de url para la autenticación del usuario.
async def login(form: OAuth2PasswordRequestForm = Depends()): #le asignamos un parametro que contenga el formulario de autenticación = Depends()
    
    user_db = search_user_db(form.username) #buscamos al usuario en la base de datos por su nombre de usuario. 
    if not user_db: #si no existe el usuario en la base de datos:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado") #se levanta un error 404.
    
    if form.password != user_db.password: #si la contraseña no coincide con la contraseña del usuario en la base de datos:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="La constraseña no es correcta") #se levanta un error 400.
    
    return {"access_token": user_db.username, "token_type": "bearer"} #si el uauaio esta autenticado, retornamos el token de acceso y el tipo de token.
#el token de acceso es el nombre de usuario, y el tipo de token es bearer (al igual que la contraseña no este encriptada, no es seguro que el access token sea el username)
#el token bearer es un tipo de token que se utiliza para autenticar al usuario en la API.


#OPERACION PARA OBTENER DATOS DE USUARIO UNA VEZ AUTENTICADO:
@router.get("/users/me")
async def me(user: User = Depends(current_user)): #le asignamos un parametro que contenga el usuario el cual depende del criterio de dependencia de autenticacion.
    return user #retornamos el usuario autenticado.
#Si el current_user no es capaz de retornar un usuario es porque no esta autenticado.

