### Instalación de Docker 🐳

- Comenzamos desinstalando versiones antiguas

```console
 sudo apt-get remove docker docker-engine docker.io containerd runc
```

- Actualice el índice de paquetes de apt e instale paquetes para permitir que apt use un repositorio a través de HTTPS 
```console
 sudo apt-get update
 sudo apt-get install \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg \
    lsb-release
```

- Agregue la clave GPG oficial de Docker:
```console
 curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
```

- Utilice el siguiente comando para configurar el repositorio estable
```console
 echo \
  "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```

- Actualice el índice del paquete apt e instale la última versión de Docker Engine y containerd
```console
 sudo apt-get update
 sudo apt-get install docker-ce docker-ce-cli containerd.io
```

- Verifique que Docker Engine esté instalado correctamente ejecutando la imagen hello-world
```console
sudo docker run hello-world
```
