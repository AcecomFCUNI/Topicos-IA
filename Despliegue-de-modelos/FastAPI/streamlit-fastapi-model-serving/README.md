<h2 align="center">
<p>Sirviendo un modelo con FastAPI, Streamlit y Docker 馃悑</p>
</h2>

Ejemplo simple de uso de streamlit y FastAPI para el modelo de ML que se describe en [este](https://davidefiocco.github.io/streamlit-fastapi-ml-serving) art铆culo y este video del [PyCon ESPA脩A 2020](https://www.youtube.com/watch?v=IvHCxycjeR0).

Al desarrollar API simples que sirven modelos de aprendizaje autom谩tico, puede ser 煤til tener _ambos_, un backend (con documentaci贸n de API) para que otras aplicaciones llamen y un frontend para que los usuarios experimenten con la funcionalidad.

En este ejemplo vamosa servir un modelo de [segmentaci贸n sem谩ntica](https://pytorch.org/hub/pytorch_vision_deeplabv3_resnet101/) usando `FastAPI` para el backend y `streamlit` para el frontend. `docker-compose` orquestar谩 los dos servicios y permite la comunicaci贸n entre ellos.

Para ejecutar el ejemplo en una m谩quina que ejecuta Docker y docker-compose, ejecute:

    docker-compose build
    docker-compose up

Para visitar la documentaci贸n de FastAPI del servicio resultante, visite http://localhost:8000 con un navegador web.
Para visitar la interfaz de usuario de Streamlit, visite http://localhost:8501.

Los registros se pueden inspeccionar a trav茅s de:

    docker-compose logs

### Despliegue 馃殌

Para implementar la aplicaci贸n, una opci贸n es la implementaci贸n en Heroku (con [Dockhero](https://elements.heroku.com/addons/dockhero)). Para hacer esto:

- renombramos `docker-compose.yml` a `dockhero-compose.yml`
- creamos una app (`<my-app>`) en una cuenta de Heroku
- instalamos localmente Heroku CLI, y habilitamos el plugin de Dockhero `heroku plugins:install dockhero`
- a帽adimos la app a DockHero (y con un plan que permita suficiente RAM para ejecutar el modelo!)
- en el terminal ingresamos `heroku dh:compose up -d --app <my-app>` para desplegar la aplicaci贸n
- para encontrar la direcci贸n de la app en la web, ingresamos `heroku dh:open --app <my-app>`
- para visualizar la api, visitamos la direcci贸n a帽adiendo el puerto `:8000/docs`, por ejemplo, `http://dockhero-<named-assigned-to-my-app>-12345.dockhero.io:8000/docs` (sin `https`)
- visitamos la direcci贸n a帽adiendo `:8501` para visualizar la interfaz de streamlit
- nos logeamos via `heroku logs -p dockhero --app <my-app>`

### Debugeando 馃悶

Para debugear y modificar la aplicaci贸n, revise este [art铆culo](https://davidefiocco.github.io/debugging-containers-with-vs-code).
