#MODELS: se encarga de representar las entidades de modelo con la que se trabaja como clase en este caso (puede ser atributo o metodo también)
#models es una carpeta que contiene los modelos de datos, en este caso el modelo de usuario.
from pydantic import BaseModel
from typing import Optional #para que el id sea opcional

class User(BaseModel):
    id: Optional[str] = None#hacemos que el id sea opcional, ya que no lo vamos a usar en la base de datos y le damos el valor None
    username: str
    email: str

