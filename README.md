# rest api

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

## notas
* Para el ingreso de usuarios en la base de datos estoy utilizando el modelo ```User``` que trae implementado ```django```. Le modifiqué el campo 'email' para que este sea único.