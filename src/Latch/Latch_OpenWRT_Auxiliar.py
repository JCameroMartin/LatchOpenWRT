#!/usr/bin/env python
# -*- coding: utf-8 -*
import sqlite3 as lite
import os
import sys
import time

class OpenwrtLatchAux():

    def __init__(self):
        self.db = os.path.dirname(sys.argv[0])+"/Latch.db"
        
    def guardar_accountid(self, usuario, accountid):
        con = lite.connect(self.db)
        if not self.cargar_accountid():
            with con:
                cur = con.cursor()    
                cur.execute("INSERT INTO Usuarios (nombre, clave) VALUES ('"+usuario+"','"+accountid+"')")
        else:
            print "Ya hay un dispositivo pareado"
                
    def cargar_accountid(self):
        con = lite.connect(self.db)
        with con:
            cur = con.cursor()
            cur.execute('SELECT clave FROM Usuarios')
            accountid = cur.fetchone()
            if str(accountid) == "None":
                return ""
            return str(accountid[0])
                
    def eliminar_accountid(self):
        con = lite.connect(self.db)
        with con:
            cur = con.cursor()    
            cur.execute("DELETE FROM Usuarios WHERE clave='"+self.cargar_accountid()+"'")
            cur.execute("DELETE FROM Dispositivos")


    def cargar_config(self):
        con = lite.connect(self.db)
	with con:
            cur = con.cursor()
            cur.execute("SELECT applicationId,secretkey,tiempoComprobacion FROM Configuracion")
            res = cur.fetchone()
            if str(res) == "None":
                return ""
            return str(res[0]),str(res[1]),str(res[2])

			
    def guardar_dispositivo(self, mac, instanceId, asocia = 0):
        con = lite.connect(self.db)
        if (not self.cargar_dispositivo(mac)[0]) or (asocia == 1):
            with con:
                cur = con.cursor()
		if asocia == 1:
                    cur.execute("UPDATE Dispositivos SET claveDispositivo='"+instanceId+"' WHERE dispositivo='"+mac+"'")
		else:
                    cur.execute("INSERT INTO Dispositivos (alias, dispositivo, estado, claveDispositivo, permanente, ultimaConexion) VALUES ('"+mac+"', '"+mac+"', 'Unlocked', '"+instanceId+"', 0, '"+time.strftime("%c")+"')")
        else:
            print "Ya hay un dispositivo pareado"
                    
    def cargar_dispositivo(self, mac):
        con = lite.connect(self.db)
        with con:
            cur = con.cursor()
            cur.execute("SELECT claveDispositivo, permanente FROM Dispositivos WHERE dispositivo='"+mac+"'")
            valores = cur.fetchone()
            if str(valores) == "None":
                return "",0,mac
	    else:
		cur = con.cursor()    
                cur.execute("UPDATE Dispositivos SET ultimaConexion='"+time.strftime("%c")+"' WHERE dispositivo='"+mac+"'")
		cur = con.cursor()    
                cur.execute("SELECT alias FROM Dispositivos WHERE dispositivo='"+mac+"'")
		alias = cur.fetchone()
			
            return str(valores[0]), str(valores[1]), str(alias[0])
                    
    def eliminar_dispositivo(self, mac):
        con = lite.connect(self.db)
        with con:
            cur = con.cursor()    
            cur.execute("DELETE FROM Dispositivos WHERE claveDispositivo='"+self.cargar_dispositivo(mac)+"'")

    def actualizar_dispositivo(self, mac, estado):
	con = lite.connect(self.db)
        with con:
	    cur = con.cursor()
	    if estado == 1:
                cur.execute("UPDATE Dispositivos SET estado='Locked' WHERE dispositivo='"+mac+"'")
	    else:
                cur.execute("UPDATE Dispositivos SET estado='Unlocked' WHERE dispositivo='"+mac+"'")

    def limpiaLista(self, lista):
	for i in range(len(lista)-1, -1, -1):
    	    if lista[i] == "":
                del lista[i]
	return lista

    def purgarInstancias(self, ListaMac):
	con = lite.connect(self.db)
        with con:
            cur = con.cursor()
	    ListaMacString = "".join(str("'"+x+"',") for x in ListaMac)
	    ListaMacString  = ListaMacString.strip(',')
	    cur.execute("SELECT claveDispositivo FROM Dispositivos WHERE dispositivo not in ("+ListaMacString+") OR (dispositivo in ("+ListaMacString+") AND permanente=1)")
	    ListaInstancias = cur.fetchall()
	    cur.execute("DELETE FROM Dispositivos WHERE dispositivo not in ("+ListaMacString+") AND permanente=0")
	    return ListaInstancias
	
