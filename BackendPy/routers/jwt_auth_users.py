#AUTENTICACIÓN DE TIPO JWT(JSON WEB TOKEN): es una autenticación más segura que usa un token JWT, a diferencia del basico, este si usa la ecriptación de datos.
#Token JWT: necesita diferentes dependencias (pip install python-jose[cryptography]) para poder trabajar con autenticación de tipo JWT. 
#(pip install "passlib[bcrypt]") para poder trabajar con encriptación de contraseñas.

from fastapi import FastAPI, HTTPException, Depends, status, APIRouter
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

#Importamos fechas que nos servira para trabajar con el tiempo de expiración del access token.
from datetime import datetime, timedelta
#timedelta: para trabjar con calculos de fechas y horas.

#Importamos jwt de jose
from jose import jwt, JWTError #JWError: se utiliza para manejar errores relacionados con la firma y verificación de tokens JWT.

#Importamos la libreria de passlib para encriptar contraseñas
from passlib.context import CryptContext

#ALGORITMO DE ENCRIPTACIÓN: Usamos la constante ALGORITHM
ALGORITHM = "HS256" #le asignamos el algoritmo de encriptación que se utiliza para firmar el token JWT.

#TOKEN DE ACCESO TEMPORAL: Usamos la constante ACCESS_TOKEN_DURATION
ACCESS_TOKEN_DURATION = 1 #1 minuto. Este token se generará al autenticar al usuario y se usará para acceder a recursos protegidos.

#SECRET: semilla que solo conoce nuestro backend y hace que nuestra encriptacion y desencriptación solo use la clave que nostros conocemos.
SECRET = "221jkgfdtd214h5qweu4677oiaud832ak875jklnxc45nv5892nk3b5kn65gk3jkh2g34"

#CONTEXTO DE ENCRIPTACIÓN:
crypt = CryptContext(schemes=["bcrypt"]) #se utiliza para encriptar y verificar contraseñas.
#schemes: definen el algoritmo de encriptación que se va a utilizar. En este caso, usamos bcrypt de passlib.

#INSTANCIA FastAPI o APIRouter
router = APIRouter()

#iNSTANCIA OAuth2
oauth2 = OAuth2PasswordBearer("/login")

#CLASES
class User(BaseModel):
    username: str
    full_name: str
    email: str
    disabled: bool

class UserDB(User):
    password: str


#DB: la contraseña será encriptada bajo las reglas de bcrypt, en este caso usaremos una pagina web que encripta la contraseña https://jwt.io/?wtime&utm_campaign=french-predictions-2024&utm_source=Snowflake&utm_medium=Website&utm_cta=native-app-hub-page?wtime
users_db = {
    "RexStar17": { 
        "username": "RexStar17",
        "full_name": "Edward Alcala",
        "email": "edwardalcala@alumno.com",
        "disabled": False, 
        "password": "$2a$12$wIZidGTTRc.aW7jEYXMEYORcW.vrqYOqpIvaj8h.balY1HmCUxime" #contraseña:12345
    },
    "RexStar20": {
        "username": "RexStar20",
        "full_name": "Edward Alcala 2",
        "email": "edwardalcala2@alumno.com",
        "disabled": True, 
        "password": "$2a$12$q03vc57JMj5HRzJNu1snB.Bj7w82YPPi7mwpmpCBOSCMteVbTA1Ji" #contraseña:54321
    }
}

#FUNCIONES de busqueda de usuarios:
def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])

def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])


#CRITERIOS:
#auth_user: se encarga de comprobar si funciona el token de acceso y verificar si el usuario existe en la base de datos.
async def auth_user(token: str = Depends(oauth2)):
    exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, #creamos una variable con la excepcion
                              detail="Credenciales invalidas", 
                              headers={"WWW-Authenticate": "Bearer"})
    
    try: #decodifica el token de acceso y comprueba si el "sub"(surname) existe.
        username = jwt.decode(token, SECRET, algorithms=[ALGORITHM]).get("sub") 
        if username is None: ##si el token no tiene el "sub" lanzamos una excepción.
            raise exception

    except JWTError: #En el caso de que el token ya no sea válido.
        raise exception

    return search_user(username)

#El current_user, ya no busca un token, tiene dependencia en auth_user. Comprueba si el usuario esta habilitado, lo retornara.
async def current_user(user: User = Depends(auth_user)): 
    if user.disabled: 
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                            detail="Usuario deshabilitado",)
    return user


#OPERACION DE AUTENTICACIÓN: 
#En este caso cambiaremos varios aspectos ya que ahora debe verificar la contraseña que se ingreso con la contraseña ¡Encriptada! del db.
#Crearemos un token de acceso seguro también debido 
@router.post("/login") 
async def login(form: OAuth2PasswordRequestForm = Depends()):
    
    user_db = search_user_db(form.username) 
    if not user_db: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")

    if not crypt.verify(form.password, user_db.password): #verificamos la contraseña ingresada con la contraseña encriptada del db. 
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="La constraseña no es correcta") 

    access_token = {"sub": user_db.username, #el token de acceso devolvera el username
                    "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_DURATION)}#se establece el tiempo de expiración del codigo de acceso

    return {"access_token": jwt.encode(access_token, SECRET, algorithm=ALGORITHM), "token_type": "bearer"}
    #se retorna el codigo de acceso codificado con los parametros de la expiracion, semilla unica y el algoritmo.

#OPERACION PARA OBTENER DATOS DE USUARIO UNA VEZ AUTENTICADO: accederemos a traves del token de acceso.
@router.get("/user/me")
async def me(user: User = Depends(current_user)):
    return user