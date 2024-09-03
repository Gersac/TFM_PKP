
import math
import numpy as np
import random
import copy
import time

np.random.seed(5)

pesos = np.random.uniform(0, 10, 500)
valor= np.random.uniform(1, 1.1, 250)
valor2= np.random.uniform(-1.1, -1, 250)

valor=np.concatenate((valor, valor2))
np.random.shuffle(valor)

valores=list(zip(pesos,valor))
capacidad=200

def leer_archivo(nombre_archivo):
    with open(nombre_archivo) as f:
            V=f.readlines()
            V_pri=V[0]
            V_pri=V_pri.split()
            capacidad=int(V_pri[1])
            
            V=V[1:]
            V=[a.strip("\n") for a in V]
            V=[a.split("\t") for a in V]
            
            V=[[int(e) for e in a] for a in V]
            valores=[]
            for x in V:
                valores.append((x[1],x[0]))
            np.random.shuffle(valores)    
    return valores, capacidad



def hacer_pruebas(nombre_archivo):
    valores,capacidad=leer_archivo(nombre_archivo)
    valores=transformar_logaritmo(valores)
    v_final=[]
    S,v,p,t=greedy(valores,capacidad)
    v_final.append([v,t])
    S2,v2,p2,t2=entorno_variable(S,valores,capacidad,v,p)
    v_final.append([v2,t2])
    S3,v3,p3,t3=temple_simulado(S,valores,capacidad,v,p,np.sqrt(v)/500,np.sqrt(v)/500*(10**-6))
    S4,v4,p4,t4=temple_simulado(S,valores,capacidad,v,p,np.sqrt(v)/500,np.sqrt(v)/500*(10**-6))
    S5,v5,p5,t5=temple_simulado(S,valores,capacidad,v,p,np.sqrt(v)/500,np.sqrt(v)/500*(10**-6))
    v_final.append([[v3,t3],[v4,t4],[v5,t5]])
    return v_final
    
def transformar_logaritmo(lista_de_duplas):
    def logaritmo_con_signo(valor):
        if valor > 0:
            return math.log(valor)
        elif valor < 0:
            return -math.log(abs(valor))

    return [(x, logaritmo_con_signo(y)) for x, y in lista_de_duplas]



def reordenar(dupla):
    a,b=dupla
    return -np.log(abs(np.exp(abs(b))))/a

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
    valor_final=0
    peso_total=0
    n_neg=0
    while peso_total<capacidad:
       nuevo=copia[0]
       valor_final=abs(nuevo[1])+valor_final
       peso_total=peso_total+nuevo[0]
       copia.remove(copia[0])
       if nuevo[1]<0:
           n_neg=n_neg+1
           ult_neg=nuevo
       S_final.append(nuevo)
       if peso_total>capacidad and n_neg%2==1:
          valor_final=valor_final-abs(ult_neg[1])
          n_neg=n_neg-1
          peso_total=peso_total-ult_neg[0] 
          S_final.remove(ult_neg)     
    valor_final=valor_final-abs(nuevo[1])
    peso_total=peso_total-nuevo[0]
    if nuevo[1]<0:
        n_neg=n_neg-1
    S_final.remove(nuevo)  
    j=-1
    while n_neg%2==1:
        j-=1
        if S_final[j][1]<0:
            valor_final=valor_final-abs(S_final[j][1])
            peso_total=peso_total-S_final[j][0]
            S_final.remove(S_final[j])
            n_neg=n_neg-1
    
    negativos_primero=sorted(val,key=mayor_negativo)
    peso_neg=capacidad+1
    a=0
    while peso_neg>capacidad:
        b=1
        while peso_neg>capacidad and negativos_primero[b][1]<0:
            peso_neg=negativos_primero[a][0]+negativos_primero[b][0]
            b=b+1
        a=a+1
    valor_neg=negativos_primero[a-1][1]+negativos_primero[b-1][1]
    
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
            maximo_valor=maximo_valor+el[1]
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
                if peso_inic-val[0]+elem[0]<capacidad and valor_inic-abs(val[1])+abs(elem[1])>valor_mejor and val[1]*elem[1]>0:
                    valor_mejor=valor_inic-abs(val[1])+abs(elem[1])
                    peso_mejor=peso_inic-val[0]+elem[0]
                    elem_mejor=elem
                    cambio=val
    S_mejor=S.copy()
    if elem_mejor!=0:
         S_mejor.remove(cambio)
         S_mejor.append(elem_mejor)   
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
                  if peso_inic-c[0]+a[0]+b[0]<capacidad and valor_inic-abs(c[1])+abs(a[1])+abs(b[1])>valor_mejor and c[1]*a[1]*b[1]>0:
                      valor_mejor=valor_inic-abs(c[1])+abs(a[1])+abs(b[1])
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
                  if peso_inic-c[0]-d[0]+a[0]<capacidad and valor_inic-abs(c[1])-abs(d[1])+abs(a[1])>valor_mejor and c[1]*a[1]*d[1]>0:
                      valor_mejor=valor_inic-abs(c[1])-abs(d[1])+abs(a[1])
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
            v_nuevo=v_actual-abs(elem_sol1[1])-abs(elem_sol2[1])+abs(elem_val1[1])+abs(elem_val2[1])
            if p_nuevo<capacidad and elem_val1 not in S_actual and elem_val2 not in S_actual and elem_val1!=elem_val2 and elem_sol1!=elem_sol2:
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
                    if random.random()<math.exp(-(v_actual-v_nuevo)/T) and elem_val1 not in S_actual and elem_val2 not in S_actual and elem_sol1!=elem_sol2:
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
                   v_nuevo=v_actual-abs(elem_sol1[1])+abs(elem_val1[1])+abs(elem_val2[1])
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
                  v_nuevo=v_actual-abs(elem_sol1[1])-abs(elem_sol2[1])+abs(elem_val1[1])
                  if p_nuevo<capacidad and elem_val1 not in S_actual and elem_sol1!=elem_sol2:
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
                          if random.random()<math.exp(-(v_actual-v_nuevo)/T) and elem_val1 not in S_actual and elem_sol1!=elem_sol2:
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



def hallar_valor(solucion):
    valor=0
    for el in solucion:
      valor=valor+abs(el[1])   
    return valor  

def hallar_peso(solucion):
    peso=0
    for el in solucion:
      peso=peso+el[0]   
    return peso



