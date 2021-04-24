# Modelo de reconocimiento de dígitos con conjunto de datos MNIST

En este ejemplo, mostramos cómo utilizar un modelo MNIST personalizado previamente entrenado para realizar el reconocimiento de dígitos en tiempo real con TorchServe.

El servicio de inferencia devolvería el dígito inferido por el modelo en la imagen de entrada.

Usamos el siguiente ejemplo de pytorch para entrenar el modelo básico de MNIST para el reconocimiento de dígitos:

https://github.com/pytorch/examples/tree/master/mnist

# Objetivo
1. Demuestre cómo empaquetar un modelo entrenado personalizado con un controlador (handler) personalizado en un archivo de modelo de Pytorch (.mar)
2. Demuestre cómo crear código de controlador de modelo
3. Demuestre cómo cargar un archivo de modelo (.mar) en TorchServe y ejecutar la inferencia.

# Serve a custom model on TorchServe

Ejecute los comandos dados en los siguientes pasos desde el directorio principal de la raíz del repositorio. Por ejemplo, si clonó el repositorio en /home/my_path/serve, ejecute los pasos desde /home/my_path/serve

  * Paso - 1: Cree un nuevo archivo de arquitectura de modelo que contenga la clase de modelo extendida desde torch.nn.modules. En este ejemplo, hemos creado un [archivo de modelo mnist](mnist.py).
  * Paso - 2: Entrene un modelo de reconocimiento de dígitos MNIST usando https://github.com/pytorch/examples/blob/master/mnist/main.py y guarde el diccionario de estado del modelo. Hemos agregado el [state dict](mnist_cnn.pt) creado previamente de este modelo.
  * Paso - 3: escriba un controlador personalizado para ejecutar la inferencia en su modelo. En este ejemplo, hemos agregado un [custom_handler](mnist_handler.py) que ejecuta la inferencia en las imágenes de entrada en escala de grises usando el modelo anterior y reconoce el dígito en la imagen.
  * Paso - 4: Cree un archivo del modelo de Pytorch utilizando la utilidad torch-model-archiver para archivar los archivos anteriores.
 
    ```bash
    torch-model-archiver --model-name mnist --version 1.0 --model-file examples/image_classifier/mnist/mnist.py --serialized-file examples/image_classifier/mnist/mnist_cnn.pt --handler  examples/image_classifier/mnist/mnist_handler.py
    ```
   
 * Paso - 5: Registre el modelo en TorchServe utilizando el archivo de archivo del modelo anterior y ejecute la inferencia de reconocimiento de dígitos
   
    ```bash
    mkdir model_store
    mv mnist.mar model_store/
    torchserve --start --model-store model_store --models mnist=mnist.mar
    curl http://127.0.0.1:8080/predictions/mnist -T examples/image_classifier/mnist/test_data/0.png
    ```

Para las Explicaciones de Captum en el lado de Torchserve, use el siguiente request de curl:
```bash
curl http://127.0.0.1:8080/explanations/mnist -T examples/image_classifier/mnist/test_data/0.png
```

Para ejecutar Explicaciones de Captum con la entrada del request en un archivo json, siga los pasos a continuación:

En config.properties, especifique `service_envelope = body` y realice la solicitud curl como se muestra a continuación:
```bash
curl -H "Content-Type: application/json" --data @examples/image_classifier/mnist/mnist_ts.json http://127.0.0.1:8080/explanations/mnist_explain
```
When a json file is passed as a request format to the curl, Torchserve unwraps the json file from the request body. This is the reason for specifying service_envelope=body in the config.properties file

### Explicaciones de Captum

La explicación se llama con la siguiente API de solicitud http://127.0.0.1:8080/explanations/mnist_explain

Torchserve admite Captum Explanations solo para modelos Eager.

Captum/Explain no admite el procesamiento por lotes.

#### Los cambios del controlador:

1. Los controladores deben inicializarse.
```python
self.ig = IntegratedGradients(self.model)
```
en la función de inicialización para que funcione el captum (se inicializa en la clase base-vision_handler)

2. El identificador del manejador de Base usa el método expla_handle para realizar captum insights en función de si el usuario desea predicciones o explicaciones. Estos métodos se pueden anular para realizar cambios en el controlador.

3. El método get_insights en el controlador es llamado por el método explain_handle para calcular información utilizando captum.

4. Si el manejador personalizado anula la función de manejador del manejador base, se debe llamar a la función explain_handle para obtener información sobre captum.

### Ejecutando KFServing

Consulte el [Readme de MNIST para KFServing](https://github.com/pytorch/serve/blob/master/kubernetes/kfserving/mnist_readme.md) para ejecutarlo localmente.

Consulte el [documento de KFServing de extremo a extremo](https://github.com/pytorch/serve/blob/master/kubernetes/kfserving/README.md) para ejecutarlo en el clúster.