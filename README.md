# AdimistracionProyectosE3

<<<<<<< HEAD
Los comandos del codigo en la misma rama del proyecto bajo el nombre de "ComandosDocker.txt"
=======
#Iniciar docoker
(que no se te olvide arrancar su aplicacion)
(si tienes fallas intenta reiniciar el doker)
-> cd //dirijete al proyecto
-> docker-compose down -v //solo usar en caso de que no abra los servicios
-> docker-compose down //cierra el proyecto
-> docker-compose up -d --build //crea todo
-> docker-compose exec web bash //arranca doker

# Ya estando arrancado ejecutar lo siguiente segun sea necesario
-> python manage.py runserver 0.0.0.0:8080 //corre el proyecto
-> python3 manage.py startapp nombre
-> python3 manage.py makemigrations //para ver las migraciones
-> python3 manage.py migrate //para crear las migraciones
-> python3 manage.py createsuperuser //es para crear un super usuario
>>>>>>> d8d7cdcea63562b36562e37daa0f7b63f8d710b8
