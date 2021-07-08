# Propuesta API
## Resumen de la API

La propuesta que se tiene en esta ocasión es la de una API en arquitectura REST que tiene como objetivo manejar las interacciones entre usuarios y una página web dedicada a compartir videos. Esta API es desarrollada en el lenguaje de programación Python, más específicamente en su framework Flask. La información que se maneja son entre tablas que se encuentran en la parte del servidor, entre estas: usuario, canal, video, playlist, etc. Por medio de estas se aloja la información correspondiente a cada una y se retira o modifica cada vez que se necesite. Lo siguiente que a continuación se muestra es un listado de todos los endpoints de la API:

- http://127.0.0.1:5000/users 
Esta ruta es para devolver a todos los usuarios de la bd, o sea soporta únicamente GET
- http://127.0.0.1:5000/user 
Esta ruta es para crear un usuario, devolver un usuario basado en su token de seguridad, y para actualizar su información, que también exige un token de verificación. GET, POST y PUT
- http://127.0.0.1:5000/user/login 
Esta ruta genera un token de validación para autorizar al usuario a ingresante y permitir al front hacer solicitudes con cierta autorización. POST
- http://127.0.0.1:5000/user/subscription
Esta ruta genera una suscripción entre usuario y canal, también las elimina. POST y DELETE. Requiere verificación de token.
- http://127.0.0.1:5000/videos 
Esta ruta devuelve todos los canales e la bd. GET. Requiere verificación de token.
- http://127.0.0.1:5000/video GET, POST. 
Esta ruta crea el video, y devuelve los videos del usuario únicamente. Requiere verificación de token
- http://127.0.0.1:5000/video/id_del_video 
GET, PUT, DELETE. Permite devolver un video en específico, editar los de usuario y eliminarlos. Requiere verificación de token.
- http://127.0.0.1:5000/video/id_del_video/like 
PUT y DELETE. Permite actualizar la información de likes. Requiere verificación de token
- http://127.0.0.1:5000/video/id_del_video/reproduction 
PUT. Permite actualizar la información de las reproducciones. Requiere verificación de token.
- http://127.0.0.1:5000//video/download/nombre_del_archivo?channelName=nombre_del_canal 
GET. Devuelve un archivo de video.


## Desarrolladores


- Jose Vizcaya
- Bryan García
- Oscar García




## Realizar commits:
- Solo mantengan este patrón y saber qué coño hemos hecho: 
  ```MID-#DE_0000_A_9999``` + un texto muy breve detallando lo que se añada o modifique
