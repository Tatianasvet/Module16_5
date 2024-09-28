from fastapi import FastAPI, Path, HTTPException, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Annotated
from typing import List

app = FastAPI()
templates = Jinja2Templates(directory="templates")
users = []


class User(BaseModel):
    id: int = None
    username: str
    age: int

    def __eq__(self, other):
        return self.id == other.id


@app.get('/')
def get_all_users(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("users.html", {"request": request, "Users": users})


@app.get('/users/{user_id}')
def get_users(request: Request, user_id: int) -> HTMLResponse:
    try:
        index = users.index(User(id=user_id, username='no_name', age=100))
        user = users[index]
        return templates.TemplateResponse("users.html", {"request": request, "user": user})
    except ValueError:
        raise HTTPException(status_code=404, detail="user not found")


@app.post('/user/{username}/{age}')
def add_user(username: Annotated[str, Path(min_length=5, max_length=20,
                                           description='Enter username',
                                           example='IUrban')],
             age: Annotated[int, Path(ge=18, le=120,
                                      description='Enter age',
                                      example='25')]) -> User:
    next_id = len(users) + 1
    user = User(id=next_id, username=username, age=age)
    users.append(user)
    return user


@app.put('/user/{user_id}/{username}/{age}')
def update_user(user_id: int,
                username: Annotated[str, Path(min_length=5, max_length=20,
                                              description='Enter username',
                                              example='IUrban')],
                age: Annotated[int, Path(ge=18, le=120,
                                         description='Enter age',
                                         example='25')]) -> User:
    try:
        index = users.index(User(id=user_id, username='no_name', age=100))
        users[index].username = username
        users[index].age = age
        return users[index]
    except ValueError:
        raise HTTPException(status_code=404, detail="user not found")


@app.delete('/user/{user_id}')
def del_user(user_id: int) -> User:
    try:
        index = users.index(User(id=user_id, username='no_name', age=100))
        return users.pop(index)
    except ValueError:
        raise HTTPException(status_code=404, detail="user not found")
