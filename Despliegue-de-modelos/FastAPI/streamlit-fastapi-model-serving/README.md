<h2 align="center">
<p>Sirviendo un modelo con FastAPI, Streamlit y Docker 🐋</p>
</h2>

Ejemplo simple de uso de streamlit y FastAPI para el modelo de ML que se describe en [este](https://davidefiocco.github.io/streamlit-fastapi-ml-serving) artículo y este video del [PyCon ESPAÑA 2020](https://www.youtube.com/watch?v=IvHCxycjeR0).

Al desarrollar API simples que sirven modelos de aprendizaje automático, puede ser útil tener _ambos_, un backend (con documentación de API) para que otras aplicaciones llamen y un frontend para que los usuarios experimenten con la funcionalidad.

En este ejemplo vamosa servir un modelo de [segmentación semántica](https://pytorch.org/hub/pytorch_vision_deeplabv3_resnet101/) usando `FastAPI` para el backend y `streamlit` para el frontend. `docker-compose` orquestará los dos servicios y permite la comunicación entre ellos.

Para ejecutar el ejemplo en una máquina que ejecuta Docker y docker-compose, ejecute:

    docker-compose build
    docker-compose up

Para visitar la documentación de FastAPI del servicio resultante, visite http://localhost:8000 con un navegador web.
Para visitar la interfaz de usuario de Streamlit, visite http://localhost:8501.

Los registros se pueden inspeccionar a través de:

    docker-compose logs

### Despliegue 🚀

Para implementar la aplicación, una opción es la implementación en Heroku (con [Dockhero](https://elements.heroku.com/addons/dockhero)). Para hacer esto:

- renombramos `docker-compose.yml` a `dockhero-compose.yml`
- creamos una app (`<my-app>`) en una cuenta de Heroku
- instalamos localmente Heroku CLI, y habilitamos el plugin de Dockhero `heroku plugins:install dockhero`
- añadimos la app a DockHero (y con un plan que permita suficiente RAM para ejecutar el modelo!)
- en el terminal ingresamos `heroku dh:compose up -d --app <my-app>` para desplegar la aplicación
- para encontrar la dirección de la app en la web, ingresamos `heroku dh:open --app <my-app>`
- para visualizar la api, visitamos la dirección añadiendo el puerto `:8000/docs`, por ejemplo, `http://dockhero-<named-assigned-to-my-app>-12345.dockhero.io:8000/docs` (sin `https`)
- visitamos la dirección añadiendo `:8501` para visualizar la interfaz de streamlit
- nos logeamos via `heroku logs -p dockhero --app <my-app>`

### Debugeando 🐞

Para debugear y modificar la aplicación, revise este [artículo](https://davidefiocco.github.io/debugging-containers-with-vs-code).
