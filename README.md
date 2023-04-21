# rest api:  peliculas

## autenticacion
Para registrar un usuario en la aplicacion hay que realizar una peticion **POST** al endpoint ```/api/signup/``` enviando un json con los siguientes campos obligatorios:  
```
{
    "email" : "email@email.com",
    "username" : "usuario",
    "password" : "contraseña"
}
```
*Tambien se pueden enviar los campos ```'first_name'``` y ```'last_name'```, pero estos no son obligatorios.*  

Si el registro fue exitoso se enviará un email el correo ingresado.  
Con el **usuario y contraseña** se podrá obtener un token de acceso y de refresco realizando una petición **POST** al endpoint ```/api/token/```.  
Ya con el token de acceso, se tendrá autorización para realizar las consultas del CRUD de peliculas.

## autorizacion
Los métodos **POST, PUT, PATCH, DELETE** para las rutas del CRUD verifican si el usuario que realiza la petición tiene permisos de *super usuario*.

## rutas accesibles
Las siguientes rutas son accesibles utilizando el token obtenido en la ruta ```/api/token``` en la cabecera *Authorization*, usando el esquema Bearer 
 ```Authorization: Bearer <token>```:  
 > **POST** ```/api/signup/```  
 > **GET** ```/api/character/```    
 > **GET** ```/api/movie/```  
 > **GET** ```/api/genre/```  
 > **GET** ```/api/charactermovie/```  

Todas las rutas pueden acceder por id a un elemento especifico, por ejemplo ```/api/movie/3```.  
Las rutas de *movie* y *character* pueden recibir los siguientes query params:
* character -> name=str, age=int, movie=movieid
* movie -> name=str, genre=str, order=ASC || DESC
## notas
* Para el ingreso de usuarios en la base de datos estoy utilizando el modelo ```User``` que trae implementado ```django```. Le modifiqué el campo 'email' para que este sea único.
## mejoras
1. Implementar documentación en swagger
2. Mejorar la estructura de carpetas del proyecto
3. Cambiar la base de datos a postgresql
4. Implementar el campo 'imagenes' para las tablas