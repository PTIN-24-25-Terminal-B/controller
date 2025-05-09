## Documentacion para la creacion de Dashboard con Grafana

# Pasos a seguir 

1- Instalar Prometheus
```
sudo apt update
sudo apt install -y prometheus
```
2- Verificar la instalacion 
```
prometheus --version
```
3- Agregar el repositorio de Grafana
```
sudo apt install -y software-properties-common
sudo add-apt-repository "deb https://packages.grafana.com/oss/deb stable main"
sudo apt update
```
4- Añadir la clave GPG de Grafana
    Este comando añade la clave publica de Grafana 
```
sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 963FA27710458545
```
5- Instalar Grafana
```
sudo apt install grafana
```
6- Iniciar y habilitar Grafana
````
sudo systemctl enable grafana-server
sudo systemctl start grafana-server
```
7- Entrar
    Ya deberia estar intalado todo correctamente aqui que podemos acceder a http://<ip_de_tu_servidor>:3000
    Si todo va bien deberias ver un inicio de sesion para Grafana, ahora hay dos opciones:
        1- Es la primera vez que alguien entra por tanto el nombre de usuario es "admin" y la contraseña tambien (si este es el caso cuando entres te pedira una contraseña nueva).
        2- Si no eres el primer@ en entrar deberas poner de nombre de usuario "admin" y de contraseña la que se escogiese cuando se entro por primera vez
