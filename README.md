# Restaurante_ALF:
## **link:** https://github.com/Alfonso18Feb/Restaurante_ALF
## ***¿Que es Alf?***
## Alf es un restaurante de primera clase con cinco cocineros que tiene una estrella michelin por lo menos. El Aforo del restaurante permite solo 60 personas que entren de golpe a sentarse. Por ser tan famoso muchos amigos van a celebrar varias cosas juntos. Entonces, ALF permite reservar mesa para las n personas que vayan a ir.
## ***Como trabajamos en ALF***
**ALF utiliza un programa concurente o en otrar palabras una ideologia donde varias personas son atendidos al mismo tiempo. Normalmente, hay unas cien personas esperando (reservado) para pedir nuestro gran menu de :**

**Carnes: Como pollos pavos y otros tipos de carnes muy especiales
Ensalades: Cesar, Wolskiana, Tartavia y muchas mas
Pasta: spaghetti, Fusilli, Farfalle, Penne, Rigatoni, Caracolas y Tagliatelle
Bocadilllos: Big cheese burger, ALF burger, ALF BIG sandwich
Platos especiales: Pizza y lasagna**
## **Funcion Programa**
*Los clientes son hilos que si han reservado la mesa para un grupo de personas(amigos) pues esperan a que todos esten para pedir juntos.*
*Luego si no tienes reservado tienes que esperar a que los clientes salgan del restauranete y haya espacio*
**Los cocineros iran cocinando sus pedidos el problema esque solo hay un horno(Mutex),tres fuegos( semaphoro(**Carnes y pasta*)),Un bocadillero(Mutex(bocadillos)), finalmente un ensaladarALF(donde se hacen las ensaladas)**
