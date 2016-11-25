module("luci.controller.Latch.latch", package.seeall)
 function index()
     entry({"admin", "Latch"}, firstchild(), "Latch", 40).dependent=false
     entry({"admin", "Latch", "Configuracion"}, call("accion_configuracion"), "Configuration", 1) 
     entry({"admin", "Latch", "Pareado"}, call("accion_pareado"), "Pair / Unpair", 2)  
     entry({"admin", "Latch", "Dispositivos"}, call("accion_dispositivos"), "Devices", 3) 
     entry({"admin", "Latch", "Ayuda"}, call("accion_ayuda"), "Help", 4) 
     entry({"admin", "Latch", "editarDispositivos"}, call("accion_editarDispositivos"), nil) 
 end

function accion_configuracion()
        if luci.http.formvalue("secretkey") then
                local driver = require "luasql.sqlite3"
		env = assert (driver.sqlite3())
		con = assert (env:connect("/root/Latch/Latch.db"))
		res = assert (con:execute(string.format([[UPDATE Configuracion SET applicationId='%s', secretkey='%s', tiempoComprobacion='%s']], luci.http.formvalue("applicationId"), luci.http.formvalue("secretkey"), luci.http.formvalue("tiempoComprobacion"))))
		con:close()
		env:close()
		luci.http.redirect(
                    luci.dispatcher.build_url("admin", "Latch", "Configuracion")
                )
        else
                luci.template.render("Latch/configuracion")
        end
end

function accion_pareado()
        if luci.http.formvalue("parear") then
               if nixio.fork() == 0 then
    			nixio.exec("/root/Latch/Latch-OpenWRT.py", luci.http.formvalue("usuario"), luci.http.formvalue("parear"))
    			io.stderr:write("Can't exec Reg\n")
		end
		sleep(30)
    		luci.http.redirect(
                    luci.dispatcher.build_url("admin", "Latch", "Pareado")
                )
        elseif luci.http.formvalue("desparear") then
		if nixio.fork() == 0 then
                        nixio.exec("/root/Latch/Latch-OpenWRT.py", luci.http.formvalue("desparear"))
		end
		sleep(30)
                luci.http.redirect(
                        luci.dispatcher.build_url("admin", "Latch", "Pareado")

                )
        else
                luci.template.render("Latch/pareado")		
        end
end

function accion_dispositivos()
	if luci.http.formvalue("alias") and luci.http.formvalue("mac") then
		if string.len(luci.http.formvalue("alias")) > 0 and string.len(luci.http.formvalue("mac")) > 0 then
                	local driver = require "luasql.sqlite3"
			env = assert (driver.sqlite3())
			con = assert (env:connect("/root/Latch/Latch.db"))
			res = assert (con:execute(string.format([[INSERT INTO Dispositivos (alias, dispositivo, estado, claveDispositivo, permanente, ultimaConexion) VALUES ('%s', '%s', 'Unlocked', '0', 1, "Unknown")]], luci.http.formvalue("alias"), luci.http.formvalue("mac"))))
			con:close()
			env:close()
		end
		luci.http.redirect(
                    luci.dispatcher.build_url("admin", "Latch", "Dispositivos")
                )
	else
		luci.template.render("Latch/dispositivos")
	end
end

function accion_ayuda()

	luci.template.render("Latch/ayuda")

end

function accion_editarDispositivos()

	if luci.http.formvalue("alias") then
                local driver = require "luasql.sqlite3"
		env = assert (driver.sqlite3())
		con = assert (env:connect("/root/Latch/Latch.db"))
		if luci.http.formvalue("permanente") then
			res = assert (con:execute(string.format([[UPDATE Dispositivos SET alias='%s', permanente='1' WHERE dispositivo='%s']], luci.http.formvalue("alias"), luci.http.formvalue("mac"))))
		else
			res = assert (con:execute(string.format([[UPDATE Dispositivos SET alias='%s', permanente='0' WHERE dispositivo='%s']], luci.http.formvalue("alias"), luci.http.formvalue("mac"))))
		end
		con:close()
		env:close()
		luci.http.redirect(
                    luci.dispatcher.build_url("admin", "Latch", "Dispositivos")
                ) 
        else
                luci.template.render("Latch/editarDispositivos")
        end
end

function sleep(s)
        local ntime = os.time() + s
        repeat until os.time() > ntime
end