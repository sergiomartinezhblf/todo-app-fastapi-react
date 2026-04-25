from fastapi import FastAPI, Request, Form 
from fastapi.responses import HTMLResponse, RedirectResponse, Response
from fastapi.templating import Jinja2Templates
from database import get_connection, init_db
from fastapi import Body
from fastapi.middleware.cors import CORSMiddleware 

app = FastAPI()


origins = [
    "http//localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=[*],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory = "templates")

init_db()

#HOME (READ)
@app.get("/",response_class=HTMLResponse)
def read_task(request:Request):
    conn = get_connection()
    tasks = conn.execute("SELECT * FROM tasks").fetchall()
    conn.close()
    return templates.TemplateResponse(name="index.html",request=request,context={"tasks":tasks})

# CREATE
@app.get("/create",response_class=HTMLResponse)
def create_page(request:Request):
    return templates.TemplateResponse(name="create.html" ,request=request)

@app.post("/create")
def create_task(title: str =Form(...),description: str=Form(...),date: str=Form(...)):
    conn = get_connection()
    conn.execute(
        "INSERT INTO tasks (title,description,date) VALUES (?,?,?)", (title,description,date)
    )
    conn.commit()
    conn.close()
    return RedirectResponse("/", status_code=303)

#UPDATE
@app.get("/edit/{task_id}",response_class=HTMLResponse)
def edit_page(request:Request,task_id: int):
    conn = get_connection()
    task = conn.execute("SELECT * FROM tasks WHERE id = ?",(task_id,)).fetchone()
    conn.close()

    if not task:
        return {"error":"Task not found"}

    return templates.TemplateResponse(name="edit.html",request=request,context={"task":task})

@app.post("/edit/{task_id}")
def update_task(task_id:int,title: str =Form(...),description: str=Form(...),date: str=Form(...)):
    conn = get_connection()
    conn.execute("UPDATE tasks SET title=?,description=?,date=? WHERE id = ?", (title,description,date,task_id))
    conn.commit()
    conn.close()
    return RedirectResponse("/",status_code=303)

#DELETE
@app.get("/delete/{task_id}")
def delete_task(task_id:int):
    conn = get_connection()
    conn.execute("DELETE FROM tasks WHERE id=?",(task_id,))
    conn.commit()
    conn.close()
    return RedirectResponse("/",status_code=303)

#GET TAREAS ENDPOINT API
@app.get("/api/tasks")
def get_tasks():
    conn = get_connection()
    tasks = conn.execute("SELECT * FROM tasks").fetchall()
    conn.close()

    return [dict(task) for task in tasks]

#CREATE ENDPOINT API
@app.post("/api/tasks")
def create_task(task: dict= Body(...)):
    conn = get_connection()
    conn.execute("INSERT INTO tasks (title,description,date) VALUES (?,?,?)",(task["title"],task["description"],task["date"]))
    conn.commit()
    conn.close()

    return {"message":"Task created"}

#UPDATE ENDPOINT API
@app.put("/api/tasks/{task_id}")
def update_task(task_id: int,task: dict=Body(...)):
    conn = get_connection()
    conn.execute("UPDATE tasks SET title=?, description=?, date=? WHERE id=?",(task["title"],task["description"],task["date"],task_id))
    conn.commit()
    conn.close()

    return {"message":"Task updated"}


#DELETE ENDPOIN API
@app.delete("/api/tasks/{task_id}")
def delete_task(task_id: int):
    conn = get_connection()
    conn.execute("DELETE FROM tasks WHERE id=?",(task_id,))
    conn.commit()
    conn.close()

    return {"message":"Task deleted"}


@app.options("/{full_path:path}")
def options_handler(full_path:str):
    return Response()