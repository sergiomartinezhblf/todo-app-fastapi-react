import React, { useState,useEffect } from 'react'

type Task = {
  id: number;
  title: string;
  description: string;
  date: string;
};

  

function App() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [title,setTitle] = useState ("");
  const [description,setDescription] = useState("")
  const [date,setDate] = useState("")
  const [editingId,setEditingId] = useState<number | null>(null);

  const fetchTask = async () =>{
  const res = await fetch("http://todo-backend-0oc6.onrender.com/api/tasks");
  const data = await res.json();
  console.log(data)
  setTasks(data);
  }

  const handleSubmit = async (e: any)=> {
    e.preventDefault();

    if (editingId){
      await fetch(`http://todo-backend-0oc6.onrender.com/api/tasks/${editingId}`,{
        method:"PUT",
        headers: {"Content-Type":"application/json"},
        body: JSON.stringify({title,description,date})
      });

      setEditingId(null)
    } else {
      await createTask(e)
    }
    setTitle("");
    setDescription("");
    setDate("")

    await fetchTask()
  };

  const handleEdit = (task: Task) =>{
     setEditingId(task.id)
     setTitle(task.title)
     setDescription(task.description)
     setDate(task.date)
  };

  const createTask = async (e: any) =>{
    e.preventDefault();
    console.log("click detectado")

    await fetch("http://todo-backend-0oc6.onrender.com/api/tasks",{
      method:"POST",
      headers: {
        "Content-Type":"application/json",
      },
      body: JSON.stringify({title,description,date}),
    });

    setTitle("");
    setDescription("");
    setTasks([]);

    await fetchTask(); 
  }

  const deleteTask = async (id: number) =>{
    const url = "http://todo-backend-0oc6.onrender.com/api/tasks/" + id

    console.log("DELETE URL",url)

    const res = await fetch(url,{
      method:"DELETE",
    });

    console.log("status",res.status)
    await fetchTask()
  
  }

  const updateTask = async (id: number) => {
    await fetch(`http://todo-backend-0oc6.onrender.com/api/tasks/${id}`,{
      method:"PUT",
      headers:{
        "Content-Type": "application/json",
      },
      body: JSON.stringify({title,description,date})
    });

    await fetchTask()
  }


useEffect(()=>{
     fetchTask();
},[]);

console.log("task state:",tasks)
  return (
    <div className="container py-4">
        <h1 className='text-center mb-4'>Todo List</h1>

      <form onSubmit={handleSubmit} className='card p-3 mb-4 shadow-sm'>
        <h5>{editingId? "Editar Tarea": "Nueva Tarea"}</h5>

        <input type="text" placeholder='Title' className="form-control mb-2" value={title} onChange={e=>setTitle(e.target.value)}/>
        <input type="text" placeholder='Description' className="form-control mb-2" value={description} onChange={e=>setDescription(e.target.value)}/>
        <input type="date" className="form-control mb-3" value={date} onChange={e=>setDate(e.target.value)} />
        <button type='submit' className='btn btn-primary'>{editingId? "Actualizar":"Agregar"}</button>
      </form>

        {
          tasks?.map(task=>(
            <div key={task.id} className='card mb-3 shadow-sm'>
              <div className='card-body'>
                <h5 className='card-title'>{task.title}</h5>
                <p className='card-text'>{task.description}</p>
                <p className='text-muted'>{task.date}</p>

                <div className='mt-3 d-flex gap-2'>
                  <button className='btn btn-warning btn-sm' onClick={()=>
                    handleEdit(task)                     
                    }>Editar</button>
                  <button className="btn btn-danger btn-sm" onClick={()=>deleteTask(task.id)}>Eliminar </button>
                
                </div>
              </div>
            </div>
          ))
        }
    </div>
     
  );
}

export default App
