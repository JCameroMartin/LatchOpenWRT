#!/usr/bin/env python
# -*- coding: utf-8 -*
import latch
import Latch_OpenWRT_Auxiliar as Aux
import sys
import sqlite3
import commands
import time

class OpenwrtLatch():

    def __init__(self):
        #Lleno variables de configuraci√≥n
	self.latchAux = Aux.OpenwrtLatchAux()
        self.APPID, self.SECRETKEY,self.TComprobacion = self.latchAux.cargar_config()
        #self.SECRETKEY = self.latchAux.cargar_config("secretkey")
        self.api = latch.Latch(self.APPID, self.SECRETKEY)
        self.accountid = self.latchAux.cargar_accountid()  
        
    def parear(self, usuario, codigo):
        #Se realiza el pareado con el servidor Latch
        response = self.api.pair(codigo)
	#print response
        if response.get_data():
            accountid = response.get_data()['accountId']
        else:
            print 'Error pareando: ', response.get_error()
            sys.exit(1)

        self.latchAux.guardar_accountid(usuario, accountid)
        
    def desparear(self, usuario):
        #Se realiza el despareado del servidor Latch
        response = self.api.unpair(self.latchAux.cargar_accountid())
        
        if response.get_error():
            print 'Error despareando: ', response.get_error()
        else:
            self.latchAux.eliminar_accountid()

    def cambiarEstado(self, mac, estado):
	if estado == 1:
            #print "Operation Blocked"
            self.latchAux.actualizar_dispositivo(mac, 1)
            commands.getstatusoutput('ubus call hostapd.wlan0 del_client '+"'"+'{"addr":"'+mac+'", "reason":1, "deauth":true, "ban_time":5000}'+"'")
        else:
            #print "Operation Allowed"
            self.latchAux.actualizar_dispositivo(mac, 0)

    def purgarInstancias(self, ListaMac):
	ListaInstancias = self.latchAux.purgarInstancias(ListaMac)
	
	for instancia in ListaInstancias:
	    try:
                #raise SystemExit(0)
	        eliminaInstanceResponse= self.api.deleteInstance(instancia[0], self.accountid, None)
	        if eliminaInstanceResponse.get_error():
            	    print 'Error eliminando instancia: ', eliminaInstanceResponse.get_error()
	    except (RuntimeError, TypeError, NameError):
	        pass

    def creaInstancia(self, mac, asocia=0):
        instanceIdResponse=self.api.createInstance(mac, self.accountid)
	if instanceIdResponse.get_error():
            print 'Error creando instancia: ', instanceIdResponse.get_error()
        else:
	    instanceId =  instanceIdResponse.get_data()['instances'].keys()[0]
	    permanente = 0
	    self.latchAux.guardar_dispositivo(mac, instanceId, asocia)
	    self.api.lock(self.accountid, None, instanceId)
	    return instanceId, permanente

    def proteger(self):
        #Comprueba los estados y act√∫a en consecuencia

        #Haciendo uso de una funcion externa obtiene la lista de MAC conectadas al router
        ComandoMac = commands.getstatusoutput('/root/Latch/Lista_mac.sh')
        ListaMac = self.latchAux.limpiaLista(ComandoMac[1].split('\n'))
	
	####Check if exists any obsolete operationid and delete it
        #print "Deleting obsolete operations"
	self.purgarInstancias(ListaMac)
        #raise SystemExit(0)
	if ListaMac:
            for mac in ListaMac:
                #print "MAC: "+mac
                ####Compruebo si existe un InstanceId para la MAC actual
                instanceId, permanente, alias = self.latchAux.cargar_dispositivo(mac)
                ####Si la MAC no tiene InstanceId asignada, creo una (bloqueada) y la guardo
                if not instanceId:
                    ####Crea y guarda la operaci√≥n
		    instanceId, permanente =  self.creaInstancia(mac)
		else:
		    ####En caso de que exista en la base de datos pero no tenga instancia asociada lo creo
		    ####Esto es para el caso de que fuese mac permanente y dejase de serlo, por lo tanto ya tendria instancia pero no estaria en Latch
		    response=self.api.instanceStatus(instanceId, self.accountid)
		    if (not response.get_data()) and (permanente == "0"):
			    instanceId, permanente =  self.creaInstancia(mac, 1)

		####Update alias of Instance (If necessary)
		if alias != mac:
		    actualizaInstanceResponse= self.api.updateInstance(instanceId, self.accountid, None, alias, "DISABLED", "DISABLED")
		    if actualizaInstanceResponse.get_error():
            		print 'Error actualizando instancia: ', actualizaInstanceResponse.get_error()

                ####Check status
		try:
                    if permanente == "0":
                        response=self.api.instanceStatus(instanceId, self.accountid)
                        if response.get_data():
                            status = response.get_data()['operations'][instanceId]['status']
                            ####If the MAC is blocked, kill the connection for this MAC
                            if status == "off":
                                self.cambiarEstado(mac, 1)
                            else:
                                self.cambiarEstado(mac, 0)
                        else:
                            print 'Error obteniendo el estado de una instancia: ', response.get_error()
                            sys.exit(1)
		    else:
		        self.cambiarEstado(mac, 0)
                except (RuntimeError, TypeError, NameError):
		    pass
		####Reload Firewall
                #print "Fin de ciclo"

if __name__ == '__main__':
    latch = OpenwrtLatch()
    if len(sys.argv) == 1:
	if (latch.SECRETKEY) and (latch.APPID):
            if latch.accountid:
                while True:
       	            latch.proteger()
		    time.sleep( float(latch.TComprobacion) )
            else:
                print "No hay dispositivos pareados"
	else:
	    print "El plugin no est· configurado"
    elif len(sys.argv) == 2:
        #Si tiene 2 argumentos significa que quiere desparear un dispositivo
        if (latch.SECRETKEY) and (latch.APPID):
	    latch.desparear(sys.argv[1])
	else:
	    print "El plugin no est· configurado"
    elif len(sys.argv) == 3:
        #Si tiene 3 argumentos significa que quiere parear un nuevo dispositivo
	if (latch.SECRETKEY) and (latch.APPID):
            latch.parear(sys.argv[1],sys.argv[2])
	else:
	    print "El plugin no est· configurado"
    else:
        print "Cantidad de par√°metros incorrecta";
