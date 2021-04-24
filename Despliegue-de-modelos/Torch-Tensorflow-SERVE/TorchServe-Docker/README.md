<h2 align="center">
<p>TorchServe‎️‍ 🔥🌐</p>
</h2>

TorchServe es una fácil y flexible herramienta para servir modelos PyTorch.

## Arquitectura de TorchServe

<p align="center">
    <br>
    <img src="https://user-images.githubusercontent.com/880376/83180095-c44cc600-a0d7-11ea-97c1-23abb4cdbe4d.jpg"/>
    <br>
    <img src="./docs/images/pipeline.png"/>
</p>

### Terminología:
* **Frontend**: El componente de manejo de requests/responses de TorchServe. Esta parte del componente de servicio maneja tanto la request/response proveniente de los clientes y administra los ciclos de vida de los modelos.
* **Model Workers**: Estos trabajadores son responsables de ejecutar la inferencia real en los modelos. Estas son instancias reales en ejecución de los modelos.
* **Model**: Los modelos pueden ser un `script_module` (modelos guardados JIT) o` eager_mode_models`. Estos modelos pueden proporcionar procesamiento previo y posterior personalizado de datos junto con cualquier otro artefacto de modelo, como state_dicts. Los modelos se pueden cargar desde el almacenamiento en la nube o desde hosts locales.
* **Plugins**: Estos son puntos finales personalizados o algoritmos de procesamiento por lotes que se pueden colocar en TorchServe en el momento del inicio..
* **Model Store**: Este es un directorio en el que existen todos los modelos que van a ser cargados.

## Contenido de este documento

* [Prerequisitos](#Prerequisitos)
* [Creando un .mar](#Creando-un-.mar)
* [Configurando los modelos servidos](#configurando-los-modelos-servidos)
* [Obteniendo predicciones](#Obteniendo-predicciones)

# Prerequisitos
Necesitamos tener instaldo Docker y Git. Luego necesitamos descargar la imagen de TorchServe desde Docker Hub

```console
docker pull toretak/torchserve
```
La imagen pesa aproximadamente ~1.35GB

# Creando un .mar

Para crear un archivo mar [archivo de modelo] para la implementación de TorchServe, puede seguir los siguientes pasos

1. Comience el contenedor compartiendo su directorio `model-store` local/cualquier directorio que contenga contenido de mar personalizado (si no existe se debe crear), así como el directorio `examples`.

```bash
docker run --rm -it -p 8080:8080 -p 8081:8081 --name mar -v $(pwd)/model-store:/home/model-server/model-store -v $(pwd)/examples:/home/model-server/examples toretak/torchserve:latest
```

2. Desde otro terminal, liste su contenedor u omita esto si conoce el nombre del contenedor

```bash
docker ps
```

3. Enlazar e ingresar al bash del contenedor en ejecución (al que llamé `mar`)

```bash
docker exec -it mar /bin/bash
```

Estarás _aterrizando_ en `/home/model-server/`, donde encontraremos 4 carpetas (`examples`, `model-store`, `tmp` y `logs`).

4. Descargue los pesos del modelo si aún no lo ha hecho (no forman parte del repositorio)

```bash
curl -o /home/model-server/examples/image_classifier/densenet_161/densenet161-8d451a50.pth https://download.pytorch.org/models/densenet161-8d451a50.pth
```

5. Ahora ejecute el comando torch-model-archiver, p. Ej.

```bash
torch-model-archiver --model-name densenet161 --version 1.0 --model-file examples/image_classifier/densenet_161/model.py --serialized-file densenet161-8d451a50.pth --handler image_classifier --extra-files examples/image_classifier/index_to_name.json
```

6. El archivo desnet161.mar debe estar presente en `/home/model-server/model-store`


# Configurando los modelos servidos

Desde otro terminal ubicada en la misma carpeta:

1. Configuramos los _workers iniciales_ y también enlazamos el archivo `.mar`
```console
curl -v -X POST "http://localhost:8081/models?initial_workers=1&synchronous=true&url=densenet161.mar"
```
2. Versionamos nuestro modelo
```console
curl -v -X PUT http://localhost:8081/models/densenet161/1.0/set-default
```

3. En caso deseemos eliminar un modelo de nuestra lista
```console
curl -X DELETE http://localhost:8081/models/densenet161/1.0
```

Podemos obtener una lista de nuestros modelos disponibles en `http://localhost:8081/models`.

Se puede acceder a las API de inferencia y administración de TorchServe en localhost a través de los puertos 8080 y 8081, respectivamente. Ejemplo :

```bash
curl http://localhost:8080/ping
```

Y listo! Ya tenemos nuestra API de inferencia configurada 😉


# Obteniendo predicciones

Para probar el servidor modelo, envíe una solicitud a la API de predicciones del servidor. TorchServe admite todas las api de inferencia y administración a través de gRPC y HTTP/REST.

### Usando REST APIs

Complete los siguientes pasos:

* Abra una nueva ventana de terminal (que no sea la que ejecuta TorchServe).
* Usa `curl` para descargar una de estas [lindas imágenes de un gatito](https://www.google.com/search?q=cute+kitten&tbm=isch&hl=en&cr=&safe=images)
   y use la bandera `-o` para nombrarlo como `kitten.jpg`.
* Utilice `curl` para enviar `POST` al end-point `predict` de TorchServe con la imagen del gatito.

<p align="center">
    <br>
    <img src="docs/images/kitten_small.jpg"/>
    </a>
    <br>
</p>

El siguiente código completa los tres pasos:

```bash
curl -O https://raw.githubusercontent.com/pytorch/serve/master/docs/images/kitten_small.jpg
curl http://127.0.0.1:8080/predictions/densenet161 -T kitten_small.jpg
```
O también podemos usar el siguiente comando (desde la carpeta actual) 
```bash
curl http://127.0.0.1:8080/predictions/densenet161 -T examples/image_classifier/kitten.jpg
```

El end-point de predicción devuelve una respuesta de predicción en JSON. Se verá como el siguiente resultado:

```json
[
  {
    "tiger_cat": 0.46933549642562866
  },
  {
    "tabby": 0.4633878469467163
  },
  {
    "Egyptian_cat": 0.06456148624420166
  },
  {
    "lynx": 0.0012828214094042778
  },
  {
    "plastic_bag": 0.00023323034110944718
  }
]
```
### Probando otros modelos

Del mismo modo, si deseamos configurar más modelos para poder servirlos, podemos explorar los ejemplos en [`examples`](examples/) (hay modelos de NLP, segmentación, etc).

A continuación se muestran los para configurar `fast-rcnn`:
```console
torch-model-archiver --model-name fastrcnn --version 1.0 --model-file examples/object_detector/fast-rcnn/model.py --serialized-file fasterrcnn_resnet50_fpn_coco-258fb6c6.pth --handler object_detector --extra-files examples/object_detector/index_to_name.json
```
```console
curl -v -X POST "http://localhost:8081/models?initial_workers=1&synchronous=true&url=fastrcnn.mar"

curl -v -X PUT http://localhost:8081/models/fastrcnn/1.0/set-default

curl http://127.0.0.1:8080/predictions/fastrcnn -T examples/object_detector/persons.jpg

curl -X DELETE http://localhost:8081/models/fastrcnn/1.0
```

Vemos que solo cambia el nombre de referencia y la ubicación de los archivos (*.py* y *.json*).