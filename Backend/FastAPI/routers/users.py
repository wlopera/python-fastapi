from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(tags=["users"])

# Entidad Usuario
class User(BaseModel):
    id:int
    name:str
    surname: str
    url: str
    age: int
    
# Lista DUMMY de usuarios
users_list = [User(id=1, name="Leonel", surname= "Messi", url= "https://leonel.com", age= 35),
              User(id=2, name="Cristiano", surname= "Ronaldo", url= "https://cr7.com", age= 37),
              User(id=3, name="Neymar", surname= "Junior", url= "https://ney.com", age= 32)]
    
@router.get("/usersjson")
async def usersjson():
    return [{"name":"Leonel", "surname":"Messi", "url":"https://leonel.com", "age": 35},
            {"name":"Cristiano", "surname":"Ronaldo", "url":"https://cr7.com", "age": 37},
            {"name":"Neymar", "surname":"Junior", "url":"https://ney.com", "age": 32},
    ]

@router.get("/usersclass")
async def usersclass():
    return User(name="Leonel", surname="Messi", url="https://leonel.com", age= 36)

@router.get("/users")
async def users():
    return users_list

# Con Path
@router.get("/user/{id}")
async def users(id: int):
   return search_user(id)
    
# Con Query
@router.get("/userquery")
async def users(id: int):
    return search_user(id)

# POST
@router.post("/user",response_model=User, status_code=201)
async def user(user: User):
    if type(search_user(user.id)) == User:
        raise HTTPException(status_code=404, detail="usuario ya existe")
    
    users_list.append(user)
    return user
     
# PUT   
@router.put("/user",response_model=User, status_code=202)
async def user(user: User):
    found = False
    for index, save_user in enumerate(users_list):
        if save_user.id == user.id:
            users_list[index] = user
            found = True
            
    if not found:
        raise HTTPException(status_code=406, detail="No se ha actualizado el usuario")
    
    return user

# DELETE
@router.delete("/user/{id}")
async def user(id: int):
    found = False
    for index, save_user in enumerate(users_list):
        if save_user.id == id:
            del users_list[index]
            found = True
            
    if not found:
        return {"error": "No se ha eliminado el usuario"}
    
    
def search_user(id: int):
    users = filter(lambda user: user.id == id, users_list)
    try:
        return list(users)[0]
    except:
        return {"error": "No se ha encontrado el usuario"}
    
### Iniciar servidor: python -m uvicorn users:router --reload