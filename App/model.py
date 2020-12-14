"""
 * Copyright 2020, Departamento de sistemas y Computación
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 * Contribución de:
 *
 * Dario Correal
 *
 """
import config
from DISClib.ADT.graph import gr
from DISClib.ADT import map as m
from DISClib.ADT import list as lt
from DISClib.ADT import stack as st
from DISClib.DataStructures import listiterator as it
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.Utils import error as error
from DISClib.ADT import orderedmap as om
from datetime import datetime
assert config
from DISClib.DataStructures import mapentry as me 
"""
En este archivo definimos los TADs que vamos a usar y las operaciones
de creacion y consulta sobre las estructuras de datos.
"""

# -----------------------------------------------------
#                       API
# -----------------------------------------------------
def newAnalyzer():
    """ Inicializa el analizador

   stops: Tabla de hash para guardar los vertices del grafo
   connections: Grafo para representar las rutas entre estaciones
   components: Almacena la informacion de los componentes conectados
   paths: Estructura que almancena los caminos de costo minimo desde un
           vertice determinado a todos los otros vértices del grafo
    """
    try:
        analyzer = {
                    'stops': None,
                    'connections': None,
                    'nameverteces': None,
                    'dates_paths':None,
                    'paths': None,
                    'company':None
                    }

        analyzer['stops'] = m.newMap(numelements=14000,
                                     maptype='PROBING',
                                     comparefunction=compareStopIds)
        analyzer['connections'] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=True,
                                              size=14000,
                                              comparefunction=compareStopIds)
        analyzer['nameverteces'] = m.newMap(numelements=2000,
                                     maptype='PROBING',
                                     comparefunction=compareStopIds) 
        analyzer['dates_paths'] = m.newMap(numelements=1000,
                                     maptype='PROBING',
                                     comparefunction=compareStopIds)
        analyzer['dates_paths'] = m.newMap(numelements=1000,
                                     maptype='PROBING',
                                     comparefunction=compareStopIds)
        analyzer['company'] = m.newMap(numelements=1000,
                                     maptype='PROBING',
                                     comparefunction=compareStopIds)                             
                                                     
        return analyzer
    except Exception as exp:
        error.reraise(exp, 'model:newAnalyzer')



# Funciones para agregar informacion al grafo
def addTrip(analyzer, trip):
    try:
        weight = trip['trip_seconds']
        if weight != '' and weight != '0.0':
            origin= trip['pickup_community_area']
            destination= trip['dropoff_community_area']
            weight= float(weight)       
            name= trip['trip_id']
            start= getDateTimeTaxiTrip(trip['trip_start_timestamp'])[1]
            end= getDateTimeTaxiTrip(trip['trip_end_timestamp'])[1]
            if not (origin==destination) and not(origin=='' or destination==''):
                addStation(analyzer, origin)
                addStation(analyzer, destination)
                addConnection(analyzer, origin, destination, weight)
                addDatesbypath(analyzer,origin,destination,weight,start,end,name)
                addCompany(analyzer,trip)
            
    except Exception as exp:
        error.reraise(exp, 'model:addTrip')

def addStation(analyzer, stationid):
    """
    Adiciona una estación como un vertice del grafo
    """
    if not gr.containsVertex(analyzer['connections'], stationid):
            gr.insertVertex(analyzer['connections'], stationid)
    return analyzer

def addConnection(analyzer,origin,destination,weight):
    """
    Adiciona un arco entre dos estaciones
    """
    edge = gr.getEdge(analyzer['connections'], origin, destination)
    if edge is None:
        gr.addEdge(analyzer['connections'], origin, destination, weight)
    return analyzer

def addDatesbypath(analyzer,v1,v2,weight,start,end,trip_id):
    edge= {'vertexA':v1,'vertexB':v2,'weight':weight,'end':end}
    value= {}
    value[trip_id]= edge
    key= start
    if not m.contains(analyzer['dates_paths'],key):
        m.put(analyzer['dates_paths'],key,value)
    else: 
        x = m.get(analyzer['dates_paths'],key)
        x['value'][trip_id]= edge
    return analyzer

def addCompany(analyzer,trip):
    company= trip["company"]
    taxi= trip["taxi_id"]
    if company=="":
        company="Independent Owner"
    existcompany= m.contains(analyzer["company"], company)
    if existcompany:
        entry= m.get(analyzer["company"], company)["value"]
        if  not taxi in entry:
            entry[1].append(taxi)    
            entry[0]+=1
            m.put(analyzer["company"],company, entry)
    else:
        m.put(analyzer["company"],company,[1,[taxi]])
    
def topCompanies(analyzer,quantity):
    llaves=m.keySet(analyzer["company"])
    iterador=it.newIterator(llaves)
    orderedmap=om.newMap(omaptype="RBT",comparefunction=CompaniesComparer)
    while it.hasNext(iterador):
        llave=it.next(iterador)
        clave=m.get(analyzer['company'],llave)['value'][0]
        compañia={'quantity':clave,'company':llave}
        om.put(orderedmap,clave,llave)
    llaves=om.keySet(orderedmap)
    iterador=it.newIterator(llaves)
    retorno=[]
    for x in range(lt.size(llaves)-quantity,lt.size(llaves)):
        llave=lt.getElement(llaves,x)
        retorno.append([om.get(orderedmap,llave)['value'],om.get(orderedmap,llave)['key']])
    return retorno

def topCompaniesbyTaxi(analyzer,quantity):
    llaves=m.keySet(analyzer["company"])
    iterador=it.newIterator(llaves)
    orderedmap=om.newMap(omaptype="RBT",comparefunction=CompaniesComparer)
    while it.hasNext(iterador):
        llave=it.next(iterador)
        clave=m.get(analyzer['company'],llave)['value']
        clave=len(clave[1])
        print(clave)
        compañia={'quantity':clave,'company':llave}
        om.put(orderedmap,clave,llave)
    llaves=om.keySet(orderedmap)
    iterador=it.newIterator(llaves)
    retorno=[]
    for x in range(lt.size(llaves)-quantity,lt.size(llaves)):
        llave=lt.getElement(llaves,x)
        retorno.append([om.get(orderedmap,llave)['value'],om.get(orderedmap,llave)['key']])
    return retorno


def CompaniesComparer(company1,company2):
    if isinstance(company1, dict):
        company1=company1['quantity']
    if isinstance(company2, dict):
        company2=company2['quantity']
    
    if company1==company2:
        return 0
    elif company1>company2:
        return 1
    else:
        return -1






# ==============================
# Funciones de consulta
# ==============================


def requerimiento_3(analyzer,com1,com2,inicio,final):
    try:
        inicio= convert_to_datetime(inicio)
        final= convert_to_datetime(final)
        if final >= inicio :
            
            minimumCostPaths(analyzer,com1)
            path= minimumCostPath(analyzer,com2)
            if path is not None :
                print('HAY CAMINO MI HERMANO')
                organized_path= []
                size= st.size(path)
                add= {}
                for i in range(0,size):
                    arco= st.pop(path)
                    organized_path.append(poner_bonita_la_ruta(arco))
                    possible_routes= get_dates_range(analyzer,inicio,final,arco)
                    add[i]= possible_routes
                first= add[0]
                minor= 0
                date= None
                for i in first.keys():
                    x= get_logical_route(add,i,final,first[i],size)
                    wei= get_time_route(x,i)
                    if minor== 0:
                        minor= wei[0]
                        date= wei[1]
                    elif minor > wei[0]:
                        minor= wei[0]
                        date= wei[1]
                return (organized_path,date,minor)
            else:
                print('NO HAY CAMINO MI HERMANO')
        else:
            print('COMO RAYOS ES MENOR EL LIMITE SUPERIOR CRACKKK')
    except Exception as exp:
        error.reraise(exp, 'model;Fallo en requerimiento 3')

def get_dates_range(analyzer,inf,sup,arco):
    mape= analyzer['dates_paths']
    keys= m.keySet(mape)
    results= {}
    for i in range(0,lt.size(keys)):
        date= lt.getElement(keys,i)
        if date >= inf and date <= sup :
            arcos= m.get(mape,date)['value']
            for j in arcos.values():
                if j['vertexA']== arco['vertexA'] and j['vertexB'] == arco['vertexB']:
                    results[date]= j['weight']
    return results

def get_logical_route(routes,start,end,weight,size):
    temp= start
    lt= []
    lt.append({start:weight})
    for i in routes.keys():
        if i != 0:
            step= routes[i]
            k= 0
            for date in step.keys():
                wei= step[date]
                if date >= temp and k== 0:
                    lt.append({date:wei})
                    temp= date
                elif date >= temp and i < (size-1) and date < end:
                    temp= date
                    lt[i][date]=wei
                elif date >= temp and i == size :
                    temp= date
                    lt[i][date]= wei

    return lt
                
def get_time_route(routes,start):
    weight= routes[0][start]
    for i in range(1,len(routes)):
        step= routes[i]
        minor= 0
        for date in step.keys():
            wei= step[date]
            if minor== 0:
                minor= wei
            elif wei < minor:
                minor= wei
        weight+= minor               
    return (weight,start)

def poner_bonita_la_ruta(arco):
    vertexA= arco['vertexA']
    vertexB= arco['vertexB']
    hola= {'vertexA':vertexA,'vertexB':vertexB}
    return hola



def companys(analyzer):
    cantcompanies = m.keySet(analyzer["company"])
    return lt.size(cantcompanies)


def taxis(analyzer):
    lsttaxis= m.valueSet(analyzer["company"])
    iterator=it.newIterator(lsttaxis)
    canttaxis= 0
    while (it.hasNext(iterator)):
        nextvalue= it.next(iterator)
        size= len(nextvalue)
        canttaxis += size
    return canttaxis





































def minimumCostPaths(analyzer, initialStation):
    """
    Calcula los caminos de costo mínimo desde la estacion initialStation
    a todos los demas vertices del grafo
    """
    analyzer['paths'] = djk.Dijkstra(analyzer['connections'], initialStation)
    return analyzer


def hasPath(analyzer, destStation):
    """
    Indica si existe un camino desde la estacion inicial a la estación destino
    Se debe ejecutar primero la funcion minimumCostPaths
    """
    return djk.hasPathTo(analyzer['paths'], destStation)


def minimumCostPath(analyzer, destStation):
    """
    Retorna el camino de costo minimo entre la estacion de inicio
    y la estacion destino
    Se debe ejecutar primero la funcion minimumCostPaths
    """
    path = djk.pathTo(analyzer['paths'], destStation)
    return path


def totalStops(analyzer):
    """
    Retorna el total de estaciones (vertices) del grafo
    """
    return gr.numVertices(analyzer['connections'])


def totalConnections(analyzer):
    """
    Retorna el total arcos del grafo
    """
    return gr.numEdges(analyzer['connections'])


# ==============================
# Funciones Helper
# ==============================


def getDateTimeTaxiTrip(taxitrip):

    """

    Recibe la informacion de un servicio de taxi leido del archivo de datos (parametro).

    Retorna de forma separada la fecha (date) y el tiempo (time) del dato 'trip_start_timestamp'

    Los datos date se pueden comparar con <, >, <=, >=, ==, !=

    Los datos time se pueden comparar con <, >, <=, >=, ==, !=

    """

    taxitripdatetime = datetime.strptime(taxitrip, '%Y-%m-%dT%H:%M:%S.%f')
    return taxitripdatetime.date(), taxitripdatetime.time()

def convert_to_datetime(date):
    comp= '09/19/18 '
    fecha= comp + date
    fecha= datetime.strptime(fecha,'%m/%d/%y %H:%M:%S')
    time= fecha.time()
    return time
# ==============================
# Funciones de Comparacion
# ==============================

def compareStopIds(stop, keyvaluestop):
    """
    Compara dos estaciones
    """
    stopcode = keyvaluestop['key']
    stop= (stop)
    stopcode= (stopcode)
    if (stop == stopcode):
        return 0
    elif (stop > stopcode):
        return 1
    else:
        return -1

