from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import psycopg

app = FastAPI()

# Modelos

class Editorial(BaseModel):
    nombre: str
    pais: str

class Libro(BaseModel):
    titulo: str
    paginas: int
    editorial: Editorial
    disponible: bool = True

class Autor(BaseModel):
    nombre: str
    nacionalidad: str

# Datos en memoria

libros = [
    {"titulo": "Dune", "paginas": 412, "editorial": {"nombre": "Chilton Books", "pais": "Estados Unidos"}, "disponible": True},
    {"titulo": "1984", "paginas": 328, "editorial": {"nombre": "Secker & Warburg", "pais": "Reino Unido"}, "disponible": True},
    {"titulo": "El Aleph", "paginas": 150, "editorial": {"nombre": "Losada", "pais": "Argentina"}, "disponible": False},
]

autores = [
    {"nombre": "Gabriel García Márquez", "nacionalidad": "Colombia"},
    {"nombre": "Jorge Luis Borges", "nacionalidad": "Argentina"},
]

# Endpoints

@app.get("/")
def leer_raiz():
    return {"mensaje": "hola"}

@app.get("/autores")
def listar_autores():
    return autores

@app.post("/autores")
def crear_autor(autor: Autor):
    autores.append(autor.dict())
    return autor

@app.post("/libros")
def crear_libro(libro: Libro):
    if libro.paginas <= 0:
        raise HTTPException(status_code=422, detail="paginas debe ser mayor a 0")
    with conectar() as conexion:
        preparar_tabla(conexion)
        conexion.execute(
            "INSERT INTO libros (titulo, paginas, editorial_nombre, editorial_pais, disponible) "
            "VALUES (%s, %s, %s, %s, %s)",
            (libro.titulo, libro.paginas, libro.editorial.nombre,
             libro.editorial.pais, libro.disponible),
        )
    return libro

@app.get("/libros")
def listar_libros(paginas_min: int = 0):
    with conectar() as conexion:
        preparar_tabla(conexion)
        filas = conexion.execute(
            "SELECT titulo, paginas, editorial_nombre, editorial_pais, disponible "
            "FROM libros WHERE paginas >= %s ORDER BY id",
            (paginas_min,),
        ).fetchall()
    return [
        {"titulo": f[0], "paginas": f[1],
         "editorial": {"nombre": f[2], "pais": f[3]}, "disponible": f[4]}
        for f in filas
    ]

@app.get("/libros/{titulo}")
def buscar_libro(titulo: str):
    for libro in libros:
        if libro["titulo"] == titulo:
            return libro
    raise HTTPException(status_code=404, detail="Libro no encontrado")

@app.put("/libros/{titulo}")
def actualizar_libro(titulo: str, libro_nuevo: Libro):
    for indice, libro in enumerate(libros):
        if libro["titulo"] == titulo:
            libros[indice] = libro_nuevo.dict()
            return libro_nuevo
    raise HTTPException(status_code=404, detail="Libro no encontrado")

@app.delete("/libros/{titulo}", status_code=204)
def borrar_libro(titulo: str):
    for indice, libro in enumerate(libros):
        if libro["titulo"] == titulo:
            libros.pop(indice)
            return
    raise HTTPException(status_code=404, detail="Libro no encontrado")

@app.get("/salud")
def salud():
    try:
        conexion = psycopg.connect(
            host=os.environ["DB_HOST"],
            user=os.environ["DB_USER"],
            password=os.environ["DB_PASSWORD"],
            dbname="postgres",
            connect_timeout=3,
        )
        conexion.close()
        return {"base": "ok"}
    except Exception as e:
        return {"base": "error", "motivo": str(e)}

def conectar():
    return psycopg.connect(
        host=os.environ["DB_HOST"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        dbname="postgres",
        connect_timeout=3,
    )

def preparar_tabla(conexion):
    conexion.execute("""
        CREATE TABLE IF NOT EXISTS libros (
            id serial PRIMARY KEY,
            titulo text NOT NULL,
            paginas int NOT NULL,
            editorial_nombre text NOT NULL,
            editorial_pais text NOT NULL,
            disponible boolean NOT NULL DEFAULT true
        )
    """)