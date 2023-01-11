#!/usr/bin/env python
# coding: utf-8

# In[2]:


#Esta será la malla curricular del MEFI 2014 para que yo pueda optimizarla con algoritmos genéticos

#Librerías
import random
import numpy as np
from numpy.random import randint
from numpy.random import rand
import time


# In[3]:


#TODO ESTO ES EL ALGORITMO GENÉTICO

def approx_Equal(x, y, tolerance=0.001):
    return abs(x-y) <= 0.5 * tolerance * (x + y)

def onemax(x):
    suma=0
    lisuma=[]
    hyperlist=[]
    #pl=0
    #Para cada vector que tenga
    for i in x:
        hyperp=i
        #print(i) #Este es un debug que me dice que vector es el que manejo
        #Tomo cada elemento de esa lista
        for p in range (0,14):
            #sumo todos los números de la lista para cada iteración (uno por uno)
            suma=suma+i[p]
        #print(f'para este gen, la suma total fue {suma}') # Este es un debug para vigilar los genes
        #Agrego la suma como hiperparámetro al vector
        hyperp.append(suma)
        #Agrego la suma a una lista de sumas
        lisuma.append(suma)
        #Reinicio la suma
        suma=0
        
        #print(hyperp) #Este es un debug para ver si se hiperparametriza el vector
        
        #Agrego el vector hiperparametrizado a una hiperlista
        hyperlist.append(hyperp)
        # Reinicio los vectores hiperparametrizados
        hyperp=[]
    
    # Todo esto de abajo es debug
    #print("Los scores son los siguientes")
    #print(lisuma)
    #print(hyperlist)
    
    
        #pl=pl+1 #este pedazo de código contaba si la población es correcta
    
    #Regreso una lista de sumas y una lista de vectores hiperparametrizados
    return lisuma,hyperlist

def mutacion(bitstring, r_mut):
     # creo una lista del 1 al 60
    lime= [i for i in range (1,61)]
    #La revuelvo
    random.shuffle(lime)
    
    for i in range(len(bitstring)):
        # reviso la mutación
        if rand() < r_mut:
           
            #creo una lista temporal
            result=[]
            #Añado los datos NO REPETIDOS en la lista
            [result.append(x) for x in lime if x not in bitstring]
                     
            #cambio el bitstring por un número de población, para asegurarme de que no se repite
            bitstring[i] = result.pop()
        

def crossover(p1, p2, r_cross):
    # por defecto, declaro a los niños como copias idénticas
    c1, c2 = p1.copy(), p2.copy()
    # reviso si se van a recombinar
    ##print(f'Antes de la cruza{c1,c2}')
    if rand() < r_cross:
        # selecciono al azar donde se van a cruzar en un punto que no sea el final del gen
        pt = randint(1, len(p1)-2)
        # los cruzo
        # Para cruzarlos, los parto en dos en el punto que seleccioné y luego los sumo, uno inverso del otro
        c1 = p1[:pt] + p2[pt:]
        c2 = p2[:pt] + p1[pt:]
    # regreso los hijos
    # reviso si los hijos son viables
    ##print('Este es el resultado de la cruza')
    rep1= set([x for x in c1 if c1.count(x) > 1])
    rep2= set([x for x in c2 if c2.count(x) > 1])
    if not rep1:
        pass
    else:
        #Si no son viables, los regreso a su posición original
        c1 = p1.copy()
        #print(f'Hijo inviable, reemplazo: {c1}')
        
    if not rep2:
        pass
    else:
        #Si no son viables, los regreso a su posición original
        c2 = p2.copy()
        #print(f'Hijo inviable, reemplazo: {c2}')
    
    # si no lo son, los regreso a su posición original.
    ##print('estos son los hijos finales')
    # regreso los hijos
    ##print(c1,c2)
    return [c1, c2]

#Esta función va a inicializar un vector y lo regresa cuando acaba de ejecutarse para almacenarlo en otra variable
def iniciarvector():
    #Hago una lista con valores del 1 al 60
    l= [i for i in range (1,maximo+1)]
    #La revuelvo
    random.shuffle(l)
    #Declaro una lista vacía
    lista = []
    #la inserto en un arreglo aleatoriamente hasta que haya 14 asignaturas
    for i in range (1,15):
        lista.append(l[i])
    #regreso el vector
    return lista


def iniciarpoblacion():
    #creo una lista vacía
    pop=[]
    #voy a añadir n vectores a la población
    for i in range(0,n_pop):
        #creo un vector y lo meto en una variable temporal
        tempop=iniciarvector()
        #apendizo la variable temporal a la lista vacía
        pop.append(tempop)
    # regreso la lista
    return pop
   
def seleccion(pop,lisuma, k=4):
    # Declaro una lista vacía donde voy a meter los índices
    pareja=[]
    #E
    for ix in randint(0, n_pop-1, k-1):
        # check if better (e.g. perform a tournament)
        pareja.append(ix)
    #Todo esto es debug
    
    #print([pareja[0]])
    #print([pareja[1]])
    #print([pareja[2]])
    
    #De aquí, obtendo el mejor score
    
    #print(f'Evaluando... 1 {lisuma[pareja[0]],pop[pareja[0]]}')
    #print(f'Evaluando... 2 {lisuma[pareja[1]],pop[pareja[1]]}')
    #print(f'Evaluando... 3 {lisuma[pareja[2]],pop[pareja[2]]}')
    
    if [lisuma[pareja[0]]] > [lisuma[pareja[1]]] and [lisuma[pareja[0]]] > [lisuma[pareja[2]]]:
        
        selected=lisuma[pareja[0]]
        selectedix=pareja[0]
        selectedvector=pop[pareja[0]]
        
        
    elif [lisuma[pareja[1]]] > [lisuma[pareja[0]]] and [lisuma[pareja[1]]] > [lisuma[pareja[2]]]:
        
        selected=lisuma[pareja[0]]
        selectedix=pareja[0]
        selectedvector=pop[pareja[0]]
        
    else:
        selected=lisuma[pareja[2]]
        selectedix=pareja[2]
        selectedvector=pop[pareja[2]]
        
        #print(lisuma[pareja[1]])
    #print(f'Evaluado! : {selected,selectedvector}')
    #Devuelvo el mejor score
    return selectedvector,selected
    
    
def genetic_algorithm(objective, n_bits, n_iter, n_pop, r_cross, r_mut):
    # primero inicio la población
    pop=iniciarpoblacion()
    poptart=[]
    maxscorp2=[]
    maxpadp2=[]
    maxscorp=0
    best=1
    count=0
    #Obtengo los hiperparámetros y el score lisuma de la funcion objetivo
    lisuma, hyperlist = objective(pop)
    #print(lisuma)
    #print(hyperlist)
    #Elimino el hiperparámetro
    for i  in pop:
        i = i[ : -1]
        poptart.append(i)
    #poptart es la población sin el hiperparámetro
    #print(poptart)
    #Ahora los obligo a concursar
    
    lisuma = []
    hyperlist = []
    
    contgen=0
    for gen in range(n_iter):
        

        
        contgen=contgen+1
#        print(maxscorp,best)
        
        error=approx_Equal(maxscorp, best, tolerance)
#        print(error)
        
        #Este es para conocer el error aproximado y cesar cuando se estabilice
        if (contgen+1>(2*n_iter/3)) and (error == True):
            count=count+1
            if (count > 3):
                print(f'El algoritmo genético acabó en la generación: {contgen}')
                break
            else:
                pass
        else:
            count=0
            pass
        
        #print(f'Esta es la generación {contgen}')
        
        
        #Obtengo los hiperparámetros y el score lisuma de la funcion objetivo
        lisuma, hyperlist = objective(pop)
        #print(lisuma)
        #print(hyperlist)
        #Elimino el hiperparámetro
        for dd  in pop:
            dd = dd[ : -1]
            poptart.append(dd)
            
        #print("lisuma")
        #print(lisuma)
        #print("hyperlist")
        #print(hyperlist)
        #print("poptart")
        #print(poptart)
        
        lispadre = []
        liscore = []
        
        #Genera n padres
        for j in range(1,n_pop+1):
            
            padre,score=seleccion(poptart,lisuma)
            lispadre.append(padre)
            liscore.append(score)
        
        poptart=[]
        
        #Vemos cual es el mejor valor
        maxscorp= max(liscore)
        #Obtengo su índice
        
        for i, j in enumerate(liscore):
            if j == maxscorp:
                indx1=i
        
        #Vemos cual es el mejor vector
        
        maxpadp=lispadre[indx1]
        
        #print(f'Antes de cruzar y mutar esta generación, el mejor score es {maxscorp}')
        #print(f'Le corresponde al vector {maxpadp}')
        
        
        
        children = []
        
        
        for i in range(0, n_pop, 2):
            # agarra padres en parejas
            p1, p2 = lispadre[i], lispadre[i+1]
            # cruza y mutación
            for c in crossover(p1, p2, r_cross):
                # mutación si tiene suerte
                mutacion(c, r_mut)
                # lo apendizamos a la nueva generación sólo si es viable
                
                children.append(c)
        # remplazamos la población
        
        
        maxscorp2.append(maxscorp)
        maxpadp2.append(maxpadp)
        #print(maxscorp2)
        #print(maxpadp2)
        
        pop = children
        #print(pop)
    
        #mutación dinámica
        
        #Reinicia la mutación si el score no se supera en la generación pasada.
        #Baja la mutación mientras más alto sea el score sólo un poquito.
        
        # este cachito me dice el mejor valor de los hijos
        best=max(maxscorp2)
        
        if best > maxscorp:           
            r_mut=r_mut
            #print(f'La tasa se ha reiniciado a{r_mut}')
        else:
            r_mut=0.99*(r_mut)
            #print(f'La tasa se ha disminuido a{r_mut}')
        
        #Este me dice cuando parar si llega a ser exactamente igual
        
        #if best == scoreT:
        #    print(f'El algoritmo genético acabó en la generación: {contgen}')
        #    break
        #else:
        #    pass
    
    maxscorp3=max(maxscorp2)
    maxid=maxscorp2.index(maxscorp3)
    maxpadp3=(maxpadp2[maxid])
    
    return [maxscorp3, maxpadp3]


#genetic_algorithm(onemax, n_bits, n_iter, n_pop, r_cross, r_mut)


# In[13]:


# hiperiteraciones
n_hyperiter = 4
# iteraciones
n_iter = 2000 #Las iteraciones deben aumentar para mejorar la precisión. Pero ocupan más tiempo cada vez. Lo dejo en 1000
# bits
n_bits = 14
# tamaño de población
n_pop = 230 #La población debe aumentar si el número de valores posibles aumenta, para 60, lo dejo en 200.
# tasa de crossover
r_cross = 0.9
# tasa de mutación
r_mut = 1.0 / float(n_bits)
# tasa de mutación permanente
r_mut2 = 1.0 / float(n_bits)
# tiempo estimado 
t_lap= (0.00015250715*n_hyperiter*n_pop*n_iter)/60
#maximo experimental
maximo=70
#score máximo teórico
scoreT=((maximo-n_bits+1)+maximo)*(n_bits/2) #sólo para pruebas, de momento. Cuando tenga el score real, se calcula de otra manera
#tolerancia
tolerance=0.0005 #Más o menos 0.1%


# Este algoritmo corre el algoritmo genético n veces y selecciona el mejor. Se detiene cuando alcanza el máximo,
def hypergenetics(onemax, n_hyperiter, n_bits, n_iter, n_pop, r_cross, r_mut):
    start = time.time()  
    #children = []
    maxs2=[]
    maxp2=[]
    lismaxscore=[]
    lismaxvector=[]

    print(f'Inicia el algoritmo. Tiempo estimado: {t_lap} minutos (máximo), mínimo: {t_lap/(2*n_hyperiter)} minutos')
    
    #Voy a generar los hipercandidatos
    for hgen in range(n_hyperiter):
        
        #reiniciar valores
        newscore1=[]
        newpop1=[]


        newscore1,newpop1=genetic_algorithm(onemax, n_bits, n_iter, n_pop, r_cross, r_mut)

        #Checa si no se repite algún elemento, lo descarta si lo hace
        if not set([x for x in newpop1 if newpop1.count(x) > 1]):
            print(f'Hiperiteración {hgen+1}: {newscore1,newpop1}')
            lismaxscore.append(newscore1)
            lismaxvector.append(newpop1)
        else:
            pass
        
        # Este es un hiperalgoritmo teórico, ya no lo uso. Por ahora.
        #Esto genera hijos a partir de dos padres
        #for i in range(0, int(n_pop)//2):
                # agarra padres en parejas
         #       p1, p2 = newpop1, newpop2
                # cruza y mutación
          #      for c in crossover(p1, p2, r_cross):
                    # mutación si tiene suerte
           #         mutacion(c, r_mut)
                    # lo apendizamos a la nueva generación
            #        children.append(c)
            # remplazamos la población
        # hyperpoptart = children
        
        if max(lismaxscore) == scoreT:
            print(f'El algoritmo terminó en la hiperiteración: {hgen+1}')
            print(f'La cantidad de candidatos aptos son: {len(lismaxvector)} de {hgen+1} totales.')
            break
        else:
            pass
      
        
            
    lismaxscoreT=max(lismaxscore)
    maxid=lismaxscore.index(lismaxscoreT)
    lismaxvectorT=(lismaxvector[maxid])    
    
    print(f'El score máximo teórico es: {((maximo-n_bits+1)+maximo)*(n_bits/2)}')
    print(f'El fitness máximo es: {lismaxscoreT/scoreT}')
    
    end = time.time()
    total_time = end - start
    print(f"\n Al algoritmo le tomó {total_time/60} minutos, o {total_time} segundos ejecutarse.")
    
    bb=lismaxvectorT
    return [lismaxscoreT,lismaxvectorT]
  
print(f'Este es un algoritmo genético hecho desde cero. El algoritmo tiene 14 genes. Se recomendarán valores, pero si va a usar números más altos que 60, deberá usar proporcionalmente más población y más iteraciones.\n')
maximo=int(input('Para encontrar la suma máxima, necesito un número. Dame un número máximo con el que trabajar\n'))
n_iter=int(input('Dame un número de iteraciones (se recomiendan 2000)\n'))
n_pop=int(input('Dame un número de población (se recomiendan 230)\n'))
scoreT=((maximo-n_bits+1)+maximo)*(n_bits/2)

print(f'Este algoritmo busca la suma máxima sin repetir de los números del 1 al {maximo}. Imprime el vector de dichos números y la suma máxima encontrada. \n')

    
# Corre el algoritmo genético varias veces y selecciona el mejor 
Eval,bb=hypergenetics(onemax, n_hyperiter, n_bits, n_iter, n_pop, r_cross, r_mut)
