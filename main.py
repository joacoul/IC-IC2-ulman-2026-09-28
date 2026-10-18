from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

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

@app.get("/libros")
def listar_libros(paginas_min: int = 0):
    resultado = []
    for libro in libros:
        if libro["paginas"] >= paginas_min:
            resultado.append(libro)
    return resultado

@app.post("/libros")
def crear_libro(libro: Libro):
    if libro.paginas <= 0:
        raise HTTPException(status_code=422, detail="Paginas debe ser mayor a 0")
    libros.append(libro.dict())
    return libro

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