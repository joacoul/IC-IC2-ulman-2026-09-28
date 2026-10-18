# Clase 3, Parte A

## A5: Imagen vs contenedor

1. Diferencia entre imagen y contenedor:
Una imagen es como el molde estatico que empaqueta el programa con sus dependencias, mientras que un contenedor es la instancia viva de ese molde en ejecucion. Por ejemplo, hoy a partir de una unica imagen python:3.12-slim pude tener dos contenedores distintos corriendo al mismo tiempo.

2. Por que Docker resuelve el "en mi maquina anda y en la tuya no":
Docker soluciona el tipico problema de "en mi maquina anda y en la tuya no" porque mete absolutamente todo el entorno en una caja sellada. Por ejemplo, hoy mi maquina tiene Python 3.14 y el contenedor corrio Python 3.12, y el programa no se entero de la diferencia porque la version correcta viajaba adentro de la caja.

3. Que aislaba Docker que el venv no:
A diferencia del `venv` de la primera clase, que solo aislaba las librerias de Python, Docker aisla todo el entorno del programa: la version exacta de Python, otros programas externos (como el broker MQTT) y el sistema base con sus archivos, procesos y red. Y lo logra siendo mas liviano que una maquina virtual, porque el contenedor comparte el kernel de la maquina anfitriona en vez de arrancar uno propio.