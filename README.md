# Restaurante_ALF:
## **link:** https://github.com/Alfonso18Feb/Restaurante_ALF
# ***¿Que es Alf?***
## Alf es un restaurante de primera clase con cinco cocineros que tiene una estrella michelin por lo menos. El Aforo del restaurante permite solo 60 personas que entren de golpe a sentarse. Por ser tan famoso muchos amigos van a celebrar varias cosas juntos. Entonces, ALF permite reservar mesa para las n personas que vayan a ir.
## ***Como trabajamos en ALF***
## **ALF utiliza un programa concurente o en otrar palabras una ideologia donde varias personas son atendidos al mismo tiempo. Normalmente, hay unas cien personas esperando (reservado) para pedir nuestro gran menu de :**

## **Carnes: Como pollos pavos y otros tipos de carnes muy especiales
## Ensalades: Cesar, Wolskiana, Tartavia y muchas mas
## Pasta: spaghetti, Fusilli, Farfalle, Penne, Rigatoni, Caracolas y Tagliatelle
## Bocadilllos: Big cheese burger, ALF burger, ALF BIG sandwich
## Platos especiales: Pizza y lasagna**
# **Funcion Programa**
## *Los clientes son hilos que si han reservado la mesa para un grupo de personas(amigos) pues esperan a que todos esten para pedir juntos.*

## *Luego si no tienes reservado tienes que esperar a que los clientes salgan del restauranete y haya espacio*

## *Los cocineros iran cocinando sus pedidos el problema esque solo hay un horno(Mutex),tres fuegos( semaphoro(**Carnes y pasta*)),Un bocadillero(Mutex(bocadillos)), finalmente un ensaladarALF(donde se hacen las ensaladas)**

## **Cuando llagan los platos las personas suelen tardar 5 minutos antes de salir del restaurante dejando a otras personas entrar**

# **Como se corre el programas**
## *En el programa sin que haya condiciones de carrera aparecen todas las personas que entran piden y se van para dejar otras mas pasar*
# **Programacion distribuida**
## **Utilizamos Product-Consumer para que las personas que hayan reservado puedan pedir su comida favorita y ser servida por nuestros grandes cocineros**
## *Es muy util para ver que estemos cuidando a cada consumidor como si fuese un consumidor especial para nuestro restaurante*
# **Tips:**
## *Hay consumidores que solo van para hablar con sus compis y pueden compartir el mismo plato. Tambien hay veces que unas personas pidan mucha comida porque tienen hambre*
## *Por eso en el histograma de los pedidos puede que no te salgan el mismo numero de clientes esperados*
## *Tambien veras a personas con mismo nombre debido a que estos nombres son comunes asi que es muy probable que se repitan*
