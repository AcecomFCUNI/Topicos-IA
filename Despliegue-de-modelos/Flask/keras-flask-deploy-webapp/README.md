# Despliegue de modelo Keras con Flask

[![](https://img.shields.io/badge/python-3.5%2B-green.svg)]()

Una linda y customizable aplicación web para desplegar tus modelos DL con facilidad. El código fuente es propiedad de [este](https://github.com/mtobeiyf/keras-flask-deploy-webapp) repositorio.

## Configuración inicial

- Clona este repositorio 
- Instala los requerimientos
- Ejecuta `app.py`
- Desde tu navegador, abre http://localhost:5000
- Hecho! ✨

⏬ Screenshot:

<p align="center">
  <img src="https://user-images.githubusercontent.com/5097752/71063354-8caa1d00-213a-11ea-86eb-879238887c1f.png" height="420px" alt="">
</p>

## Nuevas Características 🆕

- IU mejorada y optimizada para dispositivos móviles
- Admite arrastrar y soltar imágenes
- Actualizado a JavaScript vanilla, HTML y CSS
- Switch para TensorFlow 2.0 y [tf.keras](https://www.tensorflow.org/guide/keras) por defecto
- Actualización Docker con python 3

<p float="left">
  <img src="https://user-images.githubusercontent.com/5097752/71065048-61c1c800-213e-11ea-92f1-274cbe4734ba.png" height="330px" alt="">
  <img src="https://user-images.githubusercontent.com/5097752/71062921-aeef6b00-2139-11ea-8b23-6b9eb1e326ca.png" height="330px" alt="">
</p>


------------------

## Ejecutando con Docker

Con **[Docker](https://www.docker.com)**, puede crear y ejecutar rápidamente toda la aplicación en minutos :whale:

```shell
# 1. Primero, clonamos la repo
$ git clone https://github.com/AcecomFCUNI/Topicos-IA.git
$ cd Despliegue-de-modelos/Flask/keras-flask-deploy-webapp/

# 2. Construimos la imagen Docker
$ docker build -t keras_flask_app .

# 3. Ejecutamos!
$ docker run -it --rm -p 5000:5000 keras_flask_app
```

Abrimos http://localhost:5000 y esperamos a que la página web termine de cargarse.

## Instalación local

Es fácil instalar y ejecutar en tu computadora.

```shell
# 1. Primero, clonamos la repo
$ git clone https://github.com/AcecomFCUNI/Topicos-IA.git
$ cd Despliegue-de-modelos/Flask/keras-flask-deploy-webapp/

# 2. Instale las dependencias
$ pip install -r requirements.txt

# 3. Ejecuta!
$ python app.py
```

Abre http://localhost:5000 y diviértete. 😄

<p align="center">
  <img src="https://user-images.githubusercontent.com/5097752/71064959-3c34be80-213e-11ea-8e13-91800ca2d345.gif" height="480px" alt="">
</p>

------------------

## Customización

Esto es además fácil de customizar e incluir tus modelos en esta aplicación.

<details>
 <summary>Detalles</summary>

### Usa tu propio modelo

Coloca tu modelo entrenado `.h5` en la carpeta [models](models/).

Verifica [app.py](app.py).

### Usa otros modelos preentrenados

Hay muchos modelos en [Keras applications](https://keras.io/applications/) tales como DenseNet, MobilNet, NASNet, etc.

Verifica [app.py](app.py).

### Modificación de la UI

Modifica los archivos en las carpertas `templates` y `static`.

`index.html` para la UI y `main.js` para todo lo demás.

</details>


## Despliegue

Para desplegar el modelo necesita una máquina pública **linux**.

<details>
 <summary>Detalles</summary>
  
### Ejecutando la app

Ejecute el script
```
$ python app.py
```

También puedes usar gunicorn en lugar de gevent
```
$ gunicorn -b 127.0.0.1:5000 app:app
```

Para más opciones de despliegue, visitar este [sitio](https://flask.palletsprojects.com/en/1.1.x/deploying/wsgi-standalone/)

### Configurando Nginx

Para redirigir el tráfico a su aplicación local, configura tu archivo Nginx `.conf`.

```
server {
  listen  80;

  client_max_body_size 20M;

  location / {
      proxy_pass http://127.0.0.1:5000;
  }
}
```

</details>

## Características futuras

- ⬜️ Soporte para modelos de detección y segmentación

## Más recursos

[Construyendo un simple REST API: Keras + deep learning](https://blog.keras.io/building-a-simple-keras-deep-learning-rest-api.html)
