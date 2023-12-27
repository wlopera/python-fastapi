from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/products", 
                   tags=["products"],
                   responses={404: {"message": "No encontrado"}})

# Entidad Producto
class Product(BaseModel):
    id:int
    value:str  
    
products_list = [Product(id= 1, value= "Producto 1"), 
                 Product(id= 2, value= "Producto 2"), 
                 Product(id= 3, value= "Producto 3"), 
                 Product(id= 4, value= "Producto 4"), 
                 Product(id= 5, value= "Producto 5")]

@router.get("/")
async def products():
    return products_list

@router.get("/{id}")
async def product(id: int):
    return search_product(id)

def search_product(id: int):
    products = filter(lambda product: product.id == id, products_list)
    try:
        return list(products)[0]
    except:
        return list(products)[0]
        #return {"error": "No se ha encontrado el producto"}
        
### Levantar Servidor
# python -m uvicorn main:app --reload