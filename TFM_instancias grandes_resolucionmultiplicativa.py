
import math
import numpy as np
import random
import copy
import time

np.random.seed(5)

n_elementos=500
pesos = np.random.uniform(0, 10, n_elementos)
valor= np.random.uniform(1, 1.1, n_elementos//2)
valor2= np.random.uniform(-1.1, -1, n_elementos//2)


valor=np.concatenate((valor, valor2))
np.random.shuffle(valor)

valores=list(zip(pesos,valor))
capacidad=200

def reordenar(dupla):
    a,b=dupla
    return -np.log(abs(b))/a

def mayor_negativo(dupla):
    a,b=dupla
    ret=0
    if b<0:
        ret=b
    return ret    

def mayor_positivo(dupla):
    a,b=dupla
    ret=0
    if b>0:
        ret=b
    return ret    

def greedy(valores,capacidad):
    inicio=time.time()
    val=valores.copy()
    ordenadas=sorted(val,key=reordenar)
    copia=ordenadas
    S_final=[]
    valor_final=1
    peso_total=0
    while peso_total<capacidad:
       nuevo=copia[0]
       valor_final=nuevo[1]*valor_final
       peso_total=peso_total+nuevo[0]
       copia.remove(copia[0])
       if nuevo[1]<0:
           ult_neg=nuevo
       S_final.append(nuevo)
       if peso_total>capacidad and valor_final<0:
          valor_final=valor_final/ult_neg[1]
          peso_total=peso_total-ult_neg[0] 
          S_final.remove(ult_neg)     
    valor_final=valor_final/nuevo[1]
    peso_total=peso_total-nuevo[0]
    S_final.remove(nuevo)  
    j=-1
    while valor_final<0:
        j-=1
        if S_final[j][1]<0:
            valor_final=valor_final/S_final[j][1]
            peso_total=peso_total-S_final[j][0]
            S_final.remove(S_final[j]) 
    
    negativos_primero=sorted(val,key=mayor_negativo)
    peso_neg=capacidad+1
    a=0
    while peso_neg>capacidad:
        b=1
        while peso_neg>capacidad and negativos_primero[b][1]<0:
            peso_neg=negativos_primero[a][0]+negativos_primero[b][0]
            b=b+1
        a=a+1
    valor_neg=negativos_primero[a-1][1]*negativos_primero[b-1][1]
    
    pos_primero=sorted(val,key=mayor_positivo)
    valor_pos=pos_primero[-1][1]
    
    
    maximo_valor=max(valor_final,valor_pos,valor_neg)
    if maximo_valor==valor_final:
        peso_final=peso_total
    elif maximo_valor==valor_pos:
        peso_final=pos_primero[-1][0]
    else:
        peso_final=peso_neg
    for el in ordenadas:
        if el[1] >0 and peso_final+el[0]<capacidad and el not in S_final:
            peso_final=peso_final+el[0]
            maximo_valor=maximo_valor*el[1]
            S_final.append(el)    
    
    fin=time.time()-inicio
    return S_final,maximo_valor,peso_final,fin


    
    
    
def un_intercambio(S,valores,capacidad,valor_inic,peso_inic):
    inicio=time.time()
    valor_mejor=valor_inic
    peso_mejor=peso_inic
    elem_mejor=0
    cambio=0
    for elem in valores:
        if elem not in S:
            for val in S:
                if peso_inic-val[0]+elem[0]<capacidad and valor_inic/val[1]*elem[1]>valor_mejor:
                    valor_mejor=valor_inic/val[1]*elem[1]
                    peso_mejor=peso_inic-val[0]+elem[0]
                    elem_mejor=elem
                    cambio=val
    S_mejor=S.copy()
    if elem_mejor!=0:
         S_mejor.remove(cambio)
         S_mejor.append(elem_mejor)   
    fin=time.time()-inicio
    return S_mejor,valor_mejor,peso_mejor,fin  
                    
        
        
     
def dos_intercambio(S,valores,capacidad,valor_inic,peso_inic):
    inicio=time.time()
    valor_mejor=valor_inic
    peso_mejor=peso_inic
    elem_mejor=0
    cambio=0
    fuera_S=[]
    for elem in valores:
        if elem not in S:
            fuera_S.append(elem)
    i=0
    for a in fuera_S:
        i=i+1
        # print(i)
        for b in fuera_S[fuera_S.index(a)+1:]:
            for c in S:
                for d in S[S.index(c)+1:]:
                  if peso_inic-c[0]-d[0]+a[0]+b[0]<capacidad and valor_inic/c[1]/d[1]*a[1]*b[1]>valor_mejor:
                      valor_mejor=valor_inic/c[1]/d[1]*a[1]*b[1]
                      peso_mejor=peso_inic-c[0]-d[0]+a[0]+b[0]
                      elem_mejor=[a,b]
                      cambio=[c,d]
    S_mejor=S.copy()
    if elem_mejor!=0:
         S_mejor.remove(cambio[0])
         S_mejor.remove(cambio[1])
         S_mejor.append(elem_mejor[0])  
         S_mejor.append(elem_mejor[1]) 
    fin=time.time()-inicio
    return S_mejor,valor_mejor,peso_mejor,fin

   
    
 
def uno_dos_intercambio(S,valores,capacidad,valor_inic,peso_inic):
    inicio=time.time()
    valor_mejor=valor_inic
    peso_mejor=peso_inic
    elem_mejor=0
    cambio=0
    fuera_S=[]
    for elem in valores:
        if elem not in S:
            fuera_S.append(elem)
    i=0
    for a in fuera_S:
        i=i+1
        # print(i)
        for b in fuera_S[fuera_S.index(a)+1:]:
            for c in S:
                  if peso_inic-c[0]+a[0]+b[0]<capacidad and valor_inic/c[1]*a[1]*b[1]>valor_mejor:
                      valor_mejor=valor_inic/c[1]*a[1]*b[1]
                      peso_mejor=peso_inic-c[0]+a[0]+b[0]
                      elem_mejor=[a,b]
                      cambio=c
    S_mejor=S.copy()
    if elem_mejor!=0:
         S_mejor.remove(cambio)
         S_mejor.append(elem_mejor[0])  
         S_mejor.append(elem_mejor[1]) 
    fin=time.time()-inicio
    return S_mejor,valor_mejor,peso_mejor,fin
 
    
 
def dos_uno_intercambio(S,valores,capacidad,valor_inic,peso_inic):
    inicio=time.time()
    valor_mejor=valor_inic
    peso_mejor=peso_inic
    elem_mejor=0
    cambio=0
    fuera_S=[]
    for elem in valores:
        if elem not in S:
            fuera_S.append(elem)
    i=0
    for a in fuera_S:
        i=i+1
        # print(i)
        for c in S:
                for d in S[S.index(c)+1:]:
                  if peso_inic-c[0]-d[0]+a[0]<capacidad and valor_inic/c[1]/d[1]*a[1]>valor_mejor:
                      valor_mejor=valor_inic/c[1]/d[1]*a[1]
                      peso_mejor=peso_inic-c[0]-d[0]+a[0]
                      elem_mejor=a
                      cambio=[c,d]
    S_mejor=S.copy()
    if elem_mejor!=0:
         S_mejor.remove(cambio[0])
         S_mejor.remove(cambio[1])
         S_mejor.append(elem_mejor)  
    fin=time.time()-inicio
    return S_mejor,valor_mejor,peso_mejor,fin
 
 

def temple_simulado(S,valores,capacidad,valor_inic,peso_inic,T=1,fact=10**-6):
    S_mejor=copy.deepcopy(S)
    v_mejor=valor_inic
    p_mejor=peso_inic
    S_actual=copy.deepcopy(S)
    v_actual=valor_inic
    p_actual=peso_inic
    inicio=time.time()
    
    sol_neg=[]
    sol_pos=[]
    for elem in S_actual:
        if elem[1]<0:
            sol_neg.append(elem)
        else:
            sol_pos.append(elem)        
    valores_neg=[]
    valores_pos=[]
    for elem in valores:
        if elem[1]<0 and elem not in S_actual:
            valores_neg.append(elem)
        else:
            valores_pos.append(elem)
               
    while T>0:
        #print(v_mejor)
        pos1=random.randint(0,1)
        pos2=random.randint(0,1)
        if pos1==0 and pos2==0:
            sol_prob=sol_pos
            valores_prob=valores_pos
        elif pos1==0 and pos2==1:
            sol_prob=sol_pos
            valores_prob=valores_neg
        elif pos1==1 and pos2==0:
            sol_prob=sol_neg
            valores_prob=valores_pos   
        else:
            sol_prob=sol_neg
            valores_prob=valores_neg
        tipo=random.randint(0,1)  
        if len(sol_prob)>=2:    
          a=random.randint(0,len(sol_prob)-1)
          b=random.randint(0,len(sol_prob)-1) 
          c=random.randint(0,len(valores_prob)-1)
          d=random.randint(0,len(valores_prob)-1) 
          if a!=b and c!=d:
            elem_sol1=sol_prob[a]
            elem_sol2=sol_prob[b]
            elem_val1=valores_prob[c]
            elem_val2=valores_prob[d]
            p_nuevo=p_actual-elem_sol1[0]-elem_sol2[0]+elem_val1[0]+elem_val2[0]
            v_nuevo=v_actual/elem_sol1[1]/elem_sol2[1]*elem_val1[1]*elem_val2[1]
            if p_nuevo<capacidad and elem_val1 not in S_actual and elem_val2 not in S_actual and elem_val1!=elem_val2:
                if v_nuevo>v_actual:
                    v_actual=v_nuevo
                    p_actual=p_nuevo
                    S_actual.remove(elem_sol1)
                    S_actual.remove(elem_sol2)
                    S_actual.append(elem_val1)
                    S_actual.append(elem_val2)
                    sol_prob.remove(elem_sol1)
                    sol_prob.remove(elem_sol2)
                    valores_prob.remove(elem_val1)
                    valores_prob.remove(elem_val2)
                    if pos1==0:
                        valores_pos.append(elem_sol1)
                        valores_pos.append(elem_sol2)
                    if pos1==1:
                        valores_neg.append(elem_sol1)
                        valores_neg.append(elem_sol2)  
                    if pos2==0:
                        sol_pos.append(elem_val1)
                        sol_pos.append(elem_val2)
                    if pos2==1:
                        sol_neg.append(elem_val1)
                        sol_neg.append(elem_val2)    
                        
                    if hay_elementos_repetidos(S_actual):
                         S_actual=sacar_elemento_repetido(S_actual)
                         p_actual=hallar_peso(S_actual)
                         v_actual=hallar_valor(S_actual)
                         
                    
                    if v_actual>v_mejor:
                        v_mejor=v_actual
                        p_mejor=p_actual
                        S_mejor=copy.deepcopy(S_actual)
                elif  v_nuevo<v_actual:
                    if random.random()<math.exp(-(v_actual-v_nuevo)/T) and elem_val1 not in S_actual and elem_val2 not in S_actual:
                        v_actual=v_nuevo
                        p_actual=p_nuevo
                        S_actual.remove(elem_sol1)
                        S_actual.remove(elem_sol2)
                        S_actual.append(elem_val1)
                        S_actual.append(elem_val2)
                        sol_prob.remove(elem_sol1)
                        sol_prob.remove(elem_sol2)
                        valores_prob.remove(elem_val1)
                        valores_prob.remove(elem_val2)
                        if pos1==0:
                            valores_pos.append(elem_sol1)
                            valores_pos.append(elem_sol2)
                        if pos1==1:
                            valores_neg.append(elem_sol1)
                            valores_neg.append(elem_sol2)  
                        if pos2==0:
                            sol_pos.append(elem_val1)
                            sol_pos.append(elem_val2)
                        if pos2==1:
                            sol_neg.append(elem_val1)
                            sol_neg.append(elem_val2)
          if tipo==0:
             if len(sol_prob)>=2 and pos1==0:
                 a=random.randint(0,len(sol_prob)-1)
                 c=random.randint(0,len(valores_prob)-1)
                 d=random.randint(0,len(valores_prob)-1) 
                 if c!=d:
                   elem_sol1=sol_prob[a]
                   elem_val1=valores_prob[c]
                   elem_val2=valores_prob[d]
                   p_nuevo=p_actual-elem_sol1[0]+elem_val1[0]+elem_val2[0]
                   v_nuevo=v_actual/elem_sol1[1]*elem_val1[1]*elem_val2[1]
                   if p_nuevo<capacidad and elem_val1 not in S_actual and elem_val2 not in S_actual and elem_val1!=elem_val2:
                       if v_nuevo>v_actual:
                           v_actual=v_nuevo
                           p_actual=p_nuevo
                           S_actual.remove(elem_sol1)
                           
                           S_actual.append(elem_val1)
                           S_actual.append(elem_val2)
                           sol_prob.remove(elem_sol1)
                           
                           valores_prob.remove(elem_val1)
                           valores_prob.remove(elem_val2)
                           if pos1==0:
                               valores_pos.append(elem_sol1) 
                           if pos2==0:
                               sol_pos.append(elem_val1)
                               sol_pos.append(elem_val2)
                           if pos2==1:
                               sol_neg.append(elem_val1)
                               sol_neg.append(elem_val2)    
                           
                           if hay_elementos_repetidos(S_actual):
                                S_actual=sacar_elemento_repetido(S_actual)
                                p_actual=hallar_peso(S_actual)
                                v_actual=hallar_valor(S_actual)
                                
                               
                           if v_actual>v_mejor:
                               v_mejor=v_actual
                               p_mejor=p_actual
                               S_mejor=copy.deepcopy(S_actual)
                       elif  v_nuevo<v_actual:
                           if random.random()<math.exp(-(v_actual-v_nuevo)/T) and elem_val1 not in S_actual and elem_val2 not in S_actual:
                               v_actual=v_nuevo
                               p_actual=p_nuevo
                               S_actual.remove(elem_sol1)
                               S_actual.append(elem_val1)
                               S_actual.append(elem_val2)
                               sol_prob.remove(elem_sol1)
                               valores_prob.remove(elem_val1)
                               valores_prob.remove(elem_val2)
                               if pos1==0:
                                   valores_pos.append(elem_sol1)
                               if pos2==0:
                                   sol_pos.append(elem_val1)
                                   sol_pos.append(elem_val2)
                               if pos2==1:
                                   sol_neg.append(elem_val1)
                                   sol_neg.append(elem_val2)
          else:
              if len(sol_prob)>=2 and pos2==0:    
                a=random.randint(0,len(sol_prob)-1)
                b=random.randint(0,len(sol_prob)-1) 
                c=random.randint(0,len(valores_prob)-1)
                if a!=b:
                  elem_sol1=sol_prob[a]
                  elem_sol2=sol_prob[b]
                  elem_val1=valores_prob[c]
                  p_nuevo=p_actual-elem_sol1[0]-elem_sol2[0]+elem_val1[0]
                  v_nuevo=v_actual/elem_sol1[1]/elem_sol2[1]*elem_val1[1]
                  if p_nuevo<capacidad and elem_val1 not in S_actual:
                      if v_nuevo>v_actual:
                          v_actual=v_nuevo
                          p_actual=p_nuevo
                          S_actual.remove(elem_sol1)
                          S_actual.remove(elem_sol2)
                          S_actual.append(elem_val1)
                          sol_prob.remove(elem_sol1)
                          sol_prob.remove(elem_sol2)
                          valores_prob.remove(elem_val1)
                          if pos1==0:
                              valores_pos.append(elem_sol1)
                              valores_pos.append(elem_sol2)
                          if pos1==1:
                              valores_neg.append(elem_sol1)
                              valores_neg.append(elem_sol2)  
                          if pos2==0:
                              sol_pos.append(elem_val1)

                              
                          if hay_elementos_repetidos(S_actual):
                               S_actual=sacar_elemento_repetido(S_actual)
                               p_actual=hallar_peso(S_actual)
                               v_actual=hallar_valor(S_actual)
                               
                            
                          if v_actual>v_mejor:
                              v_mejor=v_actual
                              p_mejor=p_actual
                              S_mejor=copy.deepcopy(S_actual)
                      elif  v_nuevo<v_actual:
                          if random.random()<math.exp(-(v_actual-v_nuevo)/T) and elem_val1 not in S_actual:
                              v_actual=v_nuevo
                              p_actual=p_nuevo
                              S_actual.remove(elem_sol1)
                              S_actual.remove(elem_sol2)
                              S_actual.append(elem_val1)
                              sol_prob.remove(elem_sol1)
                              sol_prob.remove(elem_sol2)
                              valores_prob.remove(elem_val1)
                              if pos1==0:
                                  valores_pos.append(elem_sol1)
                                  valores_pos.append(elem_sol2)
                              if pos1==1:
                                  valores_neg.append(elem_sol1)
                                  valores_neg.append(elem_sol2)  
                              if pos2==0:
                                  sol_pos.append(elem_val1)

                         
                 
        T=T-fact
        
    fin=time.time()-inicio
    return S_mejor,v_mejor,p_mejor,fin     




            
            

def seleccion(poblacion):
    tam=len(poblacion)
    while len(poblacion)>tam/2:
        i=random.randint(0,len(poblacion)-1)
        j=random.randint(0,len(poblacion)-1)
        if i!=j:
            p1=hallar_valor(poblacion[i])
            p2=hallar_valor(poblacion[j])
            if min(p1,p2)==p1:
               poblacion.remove(poblacion[i])
            else:
               poblacion.remove(poblacion[j])
    return poblacion


def cruce(S1,S2,valores,capacidad):
    hijo1=[]
    hijo2=[]
    peso1=0
    peso2=0
    valor1=1
    valor2=1
    while peso1<capacidad or peso2<capacidad:
        a=random.randint(0,len(S1)-1)
        b=random.randint(0,len(S2)-1)
        p=random.random()
        if peso1<capacidad and S1[a] not in hijo1:
            hijo1.append(S1[a])
            peso1=peso1+S1[a][0]
            valor1=valor1*S1[a][1]
        if peso2<capacidad and S2[b] not in hijo2:
            hijo2.append(S2[b]) 
            peso2=peso2+S2[b][0]
            valor2=valor2*S2[b][1]
        c=random.randint(0,len(S1)-1)
        d=random.randint(0,len(S2)-1)
        if peso1<capacidad and S2[d] not in hijo1 and p<0.2:
            hijo1.append(S2[d])
            peso1=peso1+S2[d][0]
            valor1=valor1*S2[d][1]
        if peso2<capacidad and S1[c] not in hijo2 and p<0.2:
            hijo2.append(S1[c]) 
            peso2=peso2+S1[c][0]
            valor2=valor2*S1[c][1]
    valor1=valor1/hijo1[-1][1]
    peso1=peso1-hijo1[-1][0]
    valor2=valor2/hijo2[-1][1]
    peso2=peso2-hijo2[-1][0]
    del hijo1[-1]
    del hijo2[-1]

    if valor1<0:
        el=1
        i=0
        while el>0:
            el=hijo1[i][1]
            if el<0:
                peso1=peso1-hijo1[i][0]
                valor1=valor1/hijo1[i][1]
                hijo1.remove(hijo1[i])                
            i=i+1    
    if valor2<0:
        el=1
        i=0
        while el>0:
            el=hijo2[i][1]
            if el<0:
                peso2=peso2-hijo2[i][0]
                valor2=valor2/hijo2[i][1]
                hijo2.remove(hijo2[i])
            i=i+1    
    val_mezclado=valores[:]
    random.shuffle(val_mezclado)
    for el1 in val_mezclado:
        if el1[1] >0 and peso1+el1[0]<capacidad and el1 not in hijo1:
            peso1=peso1+el1[0]
            valor1=valor1*el1[1]
            hijo1.append(el1)
    for el2 in val_mezclado:
        if el2[1] >0 and peso2+el2[0]<capacidad and el2 not in hijo2:
            peso2=peso2+el2[0]
            valor2=valor2*el2[1]
            hijo2.append(el2)            
    return hijo1,hijo2    
         
def mutacion(poblacion,valores,capacidad):
    i=random.randint(0,len(poblacion)-1)
    j=random.randint(0,len(valores)-1)
    peso=0
    for a in poblacion:
        peso=peso+a[0]
    if peso-poblacion[i][0]+valores[j][0]<capacidad and valores[j] not in poblacion:
        poblacion.remove(poblacion[i])
        poblacion.append(valores[j])
    return poblacion    
               
        
        
def hallar_valor(solucion):
    valor=1
    for el in solucion:
      valor=valor*el[1]   
    return valor  

def hallar_peso(solucion):
    peso=0
    for el in solucion:
      peso=peso+el[0]   
    return peso




def genetico(valores,capacidad,maxit=1000,N=24,prob=0.1):
    inicio=time.time()
    constr,_,_,_=greedy(valores,capacidad)
    i=1
    poblacion=[constr]
    while i < N:
        peso=0
        valor=1
        nuevo=[]
        while peso<capacidad-capacidad*160/200:
            j=random.randint(0,len(constr)-1)
            if constr[j] not in nuevo:
                nuevo.append(constr[j])
                peso=peso+constr[j][0]
                valor=valor*constr[j][1]
        
        while peso<capacidad:
            j=random.randint(0,len(valores)-1)
            if valores[j] not in nuevo:
                nuevo.append(valores[j])
                peso=peso+valores[j][0]
                valor=valor*valores[j][1]
        valor=valor/nuevo[-1][1]
        del nuevo[-1]
        if valor >0:
            i=i+1
            poblacion.append(nuevo)
    lista_valores=list(map(hallar_valor,poblacion))
    indice_mejor=lista_valores.index(max(lista_valores))
    sol_mejor=poblacion[indice_mejor]
    val_mejor=hallar_valor(sol_mejor)
    peso_mejor=hallar_peso(sol_mejor)
    sol_act=sol_mejor
    cont=0
        
    while cont<maxit:
        hijos=[]
        j=random.randint(0,N-1)
        elementos_distintos = set(poblacion[j]).symmetric_difference(set(sol_act))
        if any(elemento not in poblacion[j] for elemento in sol_act) and  any(elemento not in sol_act for elemento in poblacion[j]) and len(elementos_distintos)>3:
            hijo1,hijo2=cruce(sol_act,poblacion[j],valores,capacidad)
            hijos.append(hijo1)
            hijos.append(hijo2)
        
        while len(hijos)<N:
            i=random.randint(0,N-1)
            j=random.randint(0,N-1)
            elementos_distintos = set(poblacion[j]).symmetric_difference(set(poblacion[i]))
            if any(elemento not in poblacion[j] for elemento in poblacion[i]) and  any(elemento not in poblacion[i] for elemento in poblacion[j]) and len(elementos_distintos)>3:
                hijo1,hijo2=cruce(poblacion[i],poblacion[j],valores,capacidad)
                hijos.append(hijo1)
                hijos.append(hijo2)
        poblacion=poblacion+hijos
        lista_valores=list(map(hallar_valor,poblacion))
        print(lista_valores)
        indice_mejor=lista_valores.index(max(lista_valores))
        sol_act=poblacion[indice_mejor]
        val_act=hallar_valor(sol_act)
        if val_act>val_mejor:
            sol_mejor=sol_act
            val_mejor=val_act
            peso_mejor=hallar_peso(sol_mejor)
        
        poblacion=seleccion(poblacion)    
        if random.random()<prob:
            i=random.randint(0,len(poblacion)-1)
            if poblacion[i]!=sol_act:
              mut=mutacion(poblacion[i],valores,capacidad)
              poblacion.remove(poblacion[i])
              poblacion.append(mut)
        cont=cont+1  

    fin=time.time()-inicio
    return sol_mejor,val_mejor,peso_mejor,fin
            




def hay_elementos_repetidos(lista):
    elementos_vistos = set()    
    for elemento in lista:
        if elemento in elementos_vistos:
            return True
        elementos_vistos.add(elemento)
    
    return False
            


def sacar_elemento_repetido(lista):
    lista_unicos = []
    vistos = set()
    for elemento in lista:
        if elemento not in vistos:
            lista_unicos.append(elemento)
            vistos.add(elemento)
    return lista_unicos

     



def entorno_variable(S,valores,capacidad,v,p,maxit=5):
    S_mejor=copy.deepcopy(S)
    v_mejor=v
    p_mejor=p
    S_actual=copy.deepcopy(S)
    v_actual=v
    p_actual=p
    inicio=time.time()
    
    i=0
    j=0
    while i<maxit and j==0:
        j=1
        print(v_mejor)
        S_actual,v_actual,p_actual,_=un_intercambio(S_actual,valores,capacidad,v_actual,p_actual)
        if v_actual>v_mejor:
            S_mejor=copy.deepcopy(S_actual)
            v_mejor=v_actual
            p_mejor=p_actual
        S_actual,v_actual,p_actual,_=uno_dos_intercambio(S_actual,valores,capacidad,v_actual,p_actual)
        if v_actual>v_mejor:
            S_mejor=copy.deepcopy(S_actual)
            v_mejor=v_actual
            p_mejor=p_actual
            j=0
        if j==1:
          S_actual,v_actual,p_actual,_=dos_uno_intercambio(S_actual,valores,capacidad,v_actual,p_actual)
          if v_actual>v_mejor:
            S_mejor=copy.deepcopy(S_actual)
            v_mejor=v_actual
            p_mejor=p_actual
            j=0    
        i=i+1
        
    fin=time.time()-inicio
    return S_mejor,v_mejor,p_mejor,fin
        















    


