from typing import List
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

import crud.models as Models
from crud import create_engine, Crud

import api.api_types as ApiTypes

resources = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    """start the character device reader"""
    print('lifespan started')
    engine = create_engine('sqlite:///database.db')
    resources['crud'] = Crud(engine)
    yield
    engine.dispose()
    resources.clear()
    print('lifespan finished')


app = FastAPI(lifespan=lifespan,
              swagger_ui_parameters={
                    'persistAuthorization': True,
                    'docExpansion': 'none',
                    'defaultModelsExpandDepth': -1,
                    'displayRequestDuration': True,
                    'filter': True,
                    'showExtensions': True,
                    'tagsSorter': 'alpha',
                    'operationsSorter': 'alpha',
                    'deepLinking': True,
                    'displayOperationId': False,
                    'defaultModelRendering': 'schema',
                    'showCommonExtensions': True,
                })

origins = [
    "http://localhost",
    "http://localhost:5001",
    "http://localhost:5001/",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/')
async def read_main():
    return "This is the base endpoint of the ball king points API v1."


@app.get('/students')
async def read_students(sort_by: str = None,
                        search: str = None) -> List[ApiTypes.Student]:
    if search:
        return resources['crud'].search(Models.Student, search)
    else:
        return resources['crud'].get(Models.Student, sort_by)


@app.get('/students/{student_id}')
async def read_student(student_id: int) -> ApiTypes.Student:
    return resources['crud'].get_single(Models.Student, student_id)


@app.get('/students/gender/{gender}')
async def get_students(gender: str) -> List[ApiTypes.Student]:
    students = resources['crud'].get(Models.Student)
    return [student for student in students if student.gender == gender]


@app.post('/students')
async def create_student(student: ApiTypes.Student) -> ApiTypes.Student:
    return resources['crud'].create(Models.Student, student)


@app.put('/students/{student_id}')
async def update_student(student_id: int,
                         student: ApiTypes.StudentNoID) -> ApiTypes.Student:
    return resources['crud'].update(Models.Student,
                                    student_id,
                                    student.model_dump())


@app.delete('/students/{student_id}')
async def delete_student(student_id: int) -> None:
    return resources['crud'].delete(Models.Student, student_id)


if __name__ == '__main__':
    import uvicorn
    uvicorn.run("main:app", host='0.0.0.0', port=5000, reload=True)
