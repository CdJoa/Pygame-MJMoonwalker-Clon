import pygame as py


W,H = 1200, 700
FPS = 30 
PANTALLA = py.display.set_mode((W,H)) # En pixeles



def reescalar_imagenes(diccionario, ancho, alto):
    for clave in diccionario:
        for i in range(len(diccionario[clave])):
            img = diccionario[clave][i]
            diccionario[clave][i] = py.transform.scale(img, (ancho,alto))

def rotar_imagen(imagenes:list):
    lista_imagenes = []
    for i in range(len(imagenes)):
        imagen_rotada = py.transform.flip(imagenes[i],True,False)
        lista_imagenes.append(imagen_rotada)
    
    return lista_imagenes



personaje_quieto = [py.image.load(r"Recursos/0.png")]
personaje_camina_derecha = [
    py.image.load(r"Recursos/1.png"),py.image.load(r"Recursos/2.png"),py.image.load(r"Recursos/2.png"),
                            py.image.load(r"Recursos/1.png")]
personaje_camina_izquierda = rotar_imagen(personaje_camina_derecha)

personaje_salta = [py.image.load(r"Recursos/3.png")]
personaje_golpeado = [py.image.load(r"Recursos/4.png")]
personaje_dispara = [py.image.load(r"Recursos/6.png")]
personaje_muerto = [py.image.load(r"Recursos/7.png")]


acciones = {}
acciones["Quieto"] = personaje_quieto
acciones["Derecha"] = personaje_camina_derecha
acciones["Izquierda"] = personaje_camina_izquierda
acciones["salta"] = personaje_salta
acciones["dispara"] = personaje_dispara
acciones["golpeado"] = personaje_golpeado
acciones["muerte"] = personaje_muerto


personaje_quieto2 = [py.image.load(r"Recursos/sm0.png")]
personaje_camina_derecha2 = [py.image.load(r"Recursos/sm1.png"),py.image.load(r"Recursos/sm1.png"),py.image.load(r"Recursos/sm2.png"),
                            py.image.load(r"Recursos/sm2.png")]
personaje_camina_izquierda2 = rotar_imagen(personaje_camina_derecha2)

personaje_salta2 = [py.image.load(r"Recursos/smSalta.png")]
personaje_dispara = [py.image.load(r"Recursos/sm4.png")]


acciones_power_up = {}
acciones_power_up["Quieto"] = personaje_quieto2
acciones_power_up["Derecha"] = personaje_camina_derecha2
acciones_power_up["Izquierda"] = personaje_camina_izquierda2
acciones_power_up["salta"] = personaje_salta2
acciones_power_up["dispara"] = personaje_dispara
acciones_power_up["golpeado"] = personaje_golpeado




enemigo_camina = [py.image.load(r"Recursos/ene1.png"),py.image.load(r"Recursos/ene1.png"),py.image.load(r"Recursos/ene2.png"),py.image.load(r"Recursos/ene2.png")]
enemigo_aplastado = [py.image.load(r"Recursos/ene4.png")]

enemigo_camina_derecha = [py.image.load(r"Recursos/ene1-derecha.png"),py.image.load(r"Recursos/ene1-derecha.png"),py.image.load(r"Recursos/ene2 - derecha.png"),py.image.load(r"Recursos/ene2 - derecha.png")]

diccionario_enemigo = {"izquierda":enemigo_camina,"derecha":enemigo_camina_derecha, "aplastado":enemigo_aplastado}

enemigo_quieto = [py.image.load(r"Recursos/Equieto0.png")]
enemigo_quietoiZQ = [py.image.load(r"Recursos/Equieto0IZQ.png")]

enemigoQ_dispara = [py.image.load(r"Recursos/Equieto2.png"),py.image.load(r"Recursos/Equieto2.png")]
enemigoQ_disparaIZQ = [py.image.load(r"Recursos/Equieto1IZQ.png"),py.image.load(r"Recursos/Equieto2IZQ.png")]


enemigo_QMuerto = [py.image.load(r"Recursos/Equieto3.png")]


enemigo_camina_derecha = [py.image.load(r"Recursos/ene1-derecha.png"),py.image.load(r"Recursos/ene1-derecha.png"),py.image.load(r"Recursos/ene2 - derecha.png"),py.image.load(r"Recursos/ene2 - derecha.png")]

diccionario_enemigoQuieto = {"izquierda":enemigo_quietoiZQ,"derecha":enemigo_quieto, "aplastado":enemigo_QMuerto, "dispara":enemigoQ_dispara,"disparaIZQ":enemigoQ_disparaIZQ }

drHuevo = [py.image.load(r"Recursos/Dr.Huevo1.png"),py.image.load(r"Recursos/Dr.Huevo2.png"),py.image.load(r"Recursos/Dr.Huevo3.png")]
drHuevoD = [py.image.load(r"Recursos/Dr.Huevo1D.png"),py.image.load(r"Recursos/Dr.Huevo2D.png"),py.image.load(r"Recursos/Dr.Huevo3D.png")]
BombaHuevo = [py.image.load(r"Recursos/Dr.Huevo5.png"),py.image.load(r"Recursos/Dr.Huevo5.png"),py.image.load(r"Recursos/explosion1.png"),py.image.load(r"Recursos/explosion2.png"),py.image.load(r"Recursos/explosion3.png"),py.image.load(r"Recursos/explosion4.png"),py.image.load(r"Recursos/explosion3.png"),py.image.load(r"Recursos/explosion2.png"),py.image.load(r"Recursos/explosion1.png")]
drHuevo_golpeado = [py.image.load(r"Recursos/Dr.Huevo5.png")]
diccionario_drHuevo = {"izquierda":drHuevoD,"derecha":drHuevo, "aplastado":drHuevo_golpeado,"bomba":BombaHuevo}


moneda_camina = [py.image.load(r"Recursos/moneda0.png"),py.image.load(r"Recursos/moneda2.png")]
moneda_aplastado = [py.image.load(r"Recursos/moneda1.png")]

diccionario_moneda = {"izquierda":moneda_camina, "aplastado":moneda_aplastado}


estrella = [py.image.load(r"Recursos/flor.png")]
estrella_tocada = [py.image.load(r"Recursos/flor.png")]

diccionario_estrella = {"izquierda": estrella, "aplastado": estrella_tocada}

vida = [py.image.load(r"Recursos/vidaExtra.png")]
vida_tocada = [py.image.load(r"Recursos/vidaExtra.png")]

diccionario_vida = {"izquierda": vida, "aplastado": vida_tocada}

botiquin = [py.image.load(r"Recursos/botiquin.png")]
botiquin_tocado = [py.image.load(r"Recursos/botiquin.png")]

diccionario_botiquin = {"izquierda": botiquin, "aplastado": botiquin_tocado}

flecha = [py.image.load(r"Recursos/flecha2.png"),py.image.load(r"Recursos/flecha.png")]
flecha_aplastado = [py.image.load(r"Recursos/flecha.png")]
diccionario_flecha= {"izquierda":flecha, "aplastado":flecha_aplastado}




llave = [py.image.load(r"Recursos/LLave.png"),py.image.load(r"Recursos/LLave.png")]
llave_aplastado = [py.image.load(r"Recursos/LLave.png")]
diccionario_llave= {"izquierda":llave, "aplastado":llave_aplastado}



