from fastapi import FastAPI #importamos el modulo FastAPI del paquete fastapi

#ROUTERS:
from BackendPy.routers import products, users, jwt_auth_users, users_db #importamos los routers

#IMPORTAR RECURSOS ESTATICOS:
from fastapi.staticfiles import StaticFiles

app = FastAPI() #le asignamos a una variable las funciones de FastAPI

#incluimos los routers:
app.include_router(products.router)
app.include_router(users.router)
app.include_router(jwt_auth_users.router)
app.include_router(users_db.router)

#incluimos recursos estaticos:
app.mount("/static", StaticFiles (directory="BackendPy/static"),name="static")
#le damos el path "/static" que usaremos en la url, y le asignamos el directorio donde se encuentran
#los archivos estaticos con el nombre "static" para referirnos a ellos.
#Para llamarlos el la url deberemos agregar "/static" (path) "/images" (folder dentro del directorio "static") "gato.jpg" (file de img).

@app.get("/") #creamos una ruta con el decorador @app.get y le asignamos la ruta "/" (raiz) a la función

#al crear la funcion usamos "async" que define a esta con asincronica, ya que FastAPI recomienda trabaja así.
async def root(): #definimos la función que se ejecutará cuando se acceda a la ruta "/"
    return "¡Hola FastAPI!" #Podemos retornar un str

#fastapi dev BackendPy/FastAPI/main.py #comando para ejecutar el servidor, el cual se recargará automáticamente cada vez que se realicen cambios en el código.
#podemos copiar el http que nos da para abrir el fronted de lo que se muestra en la pagina web de nuestro codigo.

#Podemos abrir otra petición, pero ahora la definicion no será la raiz principal ("/") solamente, le agregaremos algo más para diferenciarlo.
@app.get("/msj") 
async def msj(): 
    return {"message": "¡Hola FastAPI!"} #podemos trabajar en forma de dict
#para acceder al cambio en la funcion deberemos agregar a la ruta http el "/msj" al final.

@app.get("/url") 
async def url(): 
    return {"clase": "https://mouredev.com/python"} #de esta forma nos devuelve un json (key:value)

#podemos acceder a la documentacion con el programa: Swagger UI, desde el http del fronted que nos da la terminal con /docs
#podemos acceder tambien a documentacion con /redocs
