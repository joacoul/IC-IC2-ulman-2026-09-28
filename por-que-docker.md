# Por que Docker

## Un problema de las clases 1 y 2

En la clase 2, cuando corri `uvicorn main:app --reload`, me tiro `bash: uvicorn: command not found`. Pense que no se habia instalado bien la libreria o que me faltaba instalar FastAPI. Despues me di cuenta de que me habia olvidado de activar el entorno virtual (`venv`) en esa terminal nueva antes de ejecutarlo.

Con Docker eso no habria pasado porque empaqueta el programa junto con todo lo que necesita para correr (como las dependencias y la version de Python) directamente adentro de la imagen. Al levantar el contenedor, el entorno aislado ya viene listo y funcionando, asi que no hay que acordarse de activar nada a mano.

## Un error de Docker de hoy

Al levantar el compose, la base se murio con este mensaje:

    Error: Database is uninitialized and superuser password is not specified.

Esto pasaba porque la imagen oficial de Postgres exige que se configure una contrasenia para el superusuario para poder arrancar por cuestiones de seguridad. Lo encontre mirando los registros de la base de datos con el comando `docker compose logs base`, y lo arregle agregando la variable `POSTGRES_PASSWORD` en la seccion de `environment:` en el `compose.yaml`.