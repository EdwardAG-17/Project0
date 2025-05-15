from fastapi import APIRouter #importamos el modulo APIRouter de fastapi para crear un router.
from fastapi import HTTPException #importamos la clase HTTPException de fastapi para manejar los errores.
router = APIRouter(prefix="/products" #creamos un router con el prefijo "/products" para agrupar las rutas relacionadas a productos.
                   ,tags=["Products"] #le asignamos una etiqueta "Products" al router para organizar la documentacion.
                   ,responses={404: {"description": "Not Found"}}) #asignamos una respuesta por defecto para el status code 404 (no encontrado).

products_list = ["Product 1", "Product 2", "Product 3", "Product 4", "Product 5"]

@router.get("")
async def products():
    return products_list

@router.get("/{id}")
async def products(id: int):
    return products_list[id]


