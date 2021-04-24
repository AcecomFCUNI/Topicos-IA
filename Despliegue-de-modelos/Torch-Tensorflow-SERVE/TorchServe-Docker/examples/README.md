# Ejemplos TorchServe

Los siguientes son ejemplos sobre cómo crear y servir archivos de modelos con TorchServe.

## Creando un archivo mar para el modelo de modo ansioso

Los siguientes son los pasos para crear un archivo de modelo de Pytorch (.mar) para ejecutar un modelo de Pytorch en modo ansioso en TorchServe: 

* Requisitos previos para crear un archivador de modelos de Pytorch(.mar):
    * serialized-file (.pt) : Este archivo representa el state_dict en el caso del modelo de modo ansioso.
    * model-file (.py) : Este archivo contiene la clase de modelo ampliada desde los nn.módulos de Pytorch que representan la arquitectura del modelo. Este parámetro es obligatorio para los modelos en modo ansioso. Este archivo debe contener solo una definición de clase extendida desde torch.nn.modules
    * index_to_name.json : Este archivo contiene la asignación del índice predicho a la clase. El controlador predeterminado de TorchServe devuelve el índice y la probabilidad predichos. Este archivo se puede pasar al archivador de modelos usando el parámetro --extra-files.
    * version : Versiones del modelo.
    * handler : Nombre del controlador predeterminado o ruta al controlador de inferencia personalizado (.py)
* Sintáxis

    ```bash
    torch-model-archiver --model-name <model_name> --version <model_version_number> --model-file <path_to_model_architecture_file> --serialized-file <path_to_state_dict_file> --handler <path_to_custom_handler_or_default_handler_name> --extra-files <path_to_index_to_name_json_file>
    ```

## Creando de un archivo mar para el modelo en modo torchscript

Los siguientes son los pasos para crear un archivo de modelo de Pytorch (.mar) para ejecutar un modelo de Pytorch en modo ansioso en TorchServe:

* Requisitos previos para crear un archivador de modelos de Pytorch(.mar):
    * serialized-file (.pt) : Este archivo representa el state_dict en el caso de un modelo en modo ansioso o un ScriptModule ejecutable en el caso de TorchScript.
    * index_to_name.json : Este archivo contiene la asignación del índice predicho a la clase. El controlador predeterminado de TorchServe devuelve el índice y la probabilidad predichos. Este archivo se puede pasar al archivador de modelos usando el parámetro --extra-files.
    * version : Versiones del modelo.
    * handler : Nombre del controlador predeterminado o ruta al controlador de inferencia personalizado (.py)

* Sintáxis

    ```bash
    torch-model-archiver --model-name <model_name> --version <model_version_number> --serialized-file <path_to_executable_script_module> --extra-files <path_to_index_to_name_json_file> --handler <path_to_custom_handler_or_default_handler_name>
    ```  

## Sirviendo modelos de clasificación de imágenes
El siguiente ejemplo demuestra cómo crear un archivo de modelo de clasificador de imágenes, servirlo en TorchServe y ejecutar la predicción de imágenes utilizando el controlador image_classifier predeterminado de TorchServe:

* [Modelos de clasificación de imágenes](image_classifier)

## Sirviendo un modelo con controlador personalizado

El siguiente ejemplo demuestra cómo crear y servir un modelo NN personalizado con archivos de controladores personalizados en TorchServe: 

* [Reconocimiento de dígitos con MNIST](image_classifier/mnist)

## Sirviendo modelo de clasificación de texto
El siguiente ejemplo demuestra cómo crear y servir un modelo NN de clasificación de texto personalizado con el controlador de clasificación de texto predeterminado proporcionado por TorchServe:

* [Ejemplo de clasificación de texto](text_classification)

## Serviendo modelos de detección de objetos

El siguiente ejemplo demuestra cómo crear y servir un modelo NN fast-rcnn previamente entrenado con el controlador object_detector predeterminado proporcionado por TorchServe:

* [Ejemplo de detección de objetos](object_detector)

## Sirviendo modelos de segmentación de imágenes

El siguiente ejemplo demuestra cómo crear y servir un modelo fcn NN previamente entrenado con el controlador image_segmenter predeterminado proporcionado por TorchServe:

* [Image segmentation example](image_segmenter)


## Serving Huggingface Transformers

El siguiente ejemplo demuestra cómo crear y servir modelos de transformes previamente entrenados de Huggingface como BERT, RoBERTA, XLM: 

* [Hugging Face Transformers](Huggingface_Transformers)

## Sirviendo Wavegolw: texto-2-speech

* [Texto Waveglow a sintetizador de voz](text_to_speech_synthesizer)
