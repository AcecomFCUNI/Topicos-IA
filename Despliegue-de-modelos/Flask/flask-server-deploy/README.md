## Desplegando un modelo Pytorch usando Flask & Heroku

¡Cree e implemente su primera aplicación de aprendizaje profundo! En este tutorial de PyTorch aprenderemos a implementar nuestro modelo de PyTorch con Flask y Heroku.
Creamos una aplicación Flask simple con una API REST que devuelve el resultado como datos json y luego lo implementamos en Heroku. Como ejemplo de la aplicación PyTorch, hacemos una clasificación de dígitos, al final dibujo mis propios dígitos y muestro las predicciones. Me basé en este didáctico [video](https://youtu.be/bA7-DEtYCNM).

## Configurando Heroku
 
Una vez que ha instalado `heroku` en su máquina, comience logeándose con 
 ```console
heroku login -i 
 ```
Luego cree un nombre para su proyecto de heroku
```console
heroku create <nombre-de-su-app>
```
Después configuramos los archivos `Procfile`, `requirements.txt` y `wsgi.py`, que indican cómo se va a servir la aplicación.

Posteriormente hacemos una prueba de nuestra aplicación antes de llevarla a producción
```console
heroku local
```
Inicializamos el repositorio
```console
git init
```
Conectamos nuestro repositorio con heroku
```console
heroku git:remote -a <nombre-de-su-app>
```
Añadimos y comiteamos nuestros archivos
```console
git add .
git commit -m "primer commit del proyecto"
```
Finalmente hacemos push
```console
git push heroku master
```
Y listo! Nuestro modelo ya esta servido en la nube ☁️!





