#SCHEMAS: Guarda operaciones que nos ayuda a trabajar entre loq ue son los modelos y como se trabajan los datos en la base de datos.
#schemas es una carpeta que contiene los esquemas de datos, en este caso el esquema de usuario.

#Creamos una funcion de esquema para el usario que nos va a ayudar a transformar los datos que nos llegan por el body en un objeto de tipo User.
def user_schema(user) -> dict: #user es el parametro que recibe la funcion, que es el objeto que se va a transformar.
    
    return {#el return, hara que se transformen los datos del usuario que se va a guardar en la base de datos.
        #buscará cada campo (id, username y email) en la base de datos y se le asignara el valor corrependiente.

        "id": str(user["_id"]), #se convierte el id a string porque mongodb lo guarda como un objeto.
        "username": user["username"], 
        "email": user["email"] 
    
    } #retornamos un diccionario con los datos del usuario que se va a guardar en la base de datos.

#Esta función trabaja como la anterior, pero devuelve varios objetos, no solo uno.
def user_schema_list(users) -> list:
    return [user_schema(user) for user in users] #retornamos una lista con los objetos que se van a guardar en la base de datos.