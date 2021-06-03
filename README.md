# Aplicación que ayuda a visualizar videos en youtube por canales de un usuario

By [@alejanadrohdo](https://www.facebook.com/alejandrohdo)
Nota: Este proyecto es  un experimento para  probar el algoritmo de youtube en cuanto al posicionamiento de videos(YouTube SEO).

### Requisitos generales:
- git
- pip3 
- Virtualenv 
- Python3.6.x
- selenium==3.141.0 

### PASOS O ACCIONES QUE REALIZA EL SCRIPT:
- 1: Visitar al canal, a la seccion de videos
- 2: Realizar click en reproducir todo
- 2: Aumentar la reproduccion de videos a 2x, si es la primera iteración autenticarse o reutilizar la sesión de firefox y verificar los likes de todos los videos.
- 4: Esperar entre 15 a 30min en una iteración
- 5: repetir las acciones anteriores

## PASOS PARA EJECUTAR EN MODO DESARROLLO
- Antes tener aguegrado su llave ssh en su perfil de gitlab, 
[generación de id_rsa.pub](https://www.ssh.com/ssh/keygen/)

- Descarga de driver para seleninum geckodriver, 
[geckodriver](https://github.com/mozilla/geckodriver/releases)

- Descarga de python3.6.x , 
[python3](https://www.python.org/downloads/)

Clonar el repositorio
```
git clone git@github.com:alejandrohdo/youtube-viewer-selenium.git
```
creación y activación de un entorno virtual
```
virtualenv -p python3 env_youtube_viewer && source env_youtube_viewer/bin/activate
```
Creación de archivo de configuración, provisionamiento de configuraciones de un usuario
```
cp youtube-viewer-selenium/example_config.json youtube-viewer-selenium/config.json && cd youtube-viewer-selenium

```
### Instalacion de dependencias del proyecto
```
pip install -r install requeriments.txt
```

### Ejecuación del script
```
 python youtubeViewerRobot.py
```
