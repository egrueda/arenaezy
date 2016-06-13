# -*- coding: utf-8 -*-
#------------------------------------------------------------
# Kodi Add-on for http://arenavision.ezy.es
# Version 1.0.4
#------------------------------------------------------------
# License: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
# Based on code from youtube addon
#------------------------------------------------------------
# Changelog:
# 1.0.4
# - Mostrar agenda completa
# - Pantalla de ajustes
# - Posibilidad elegir servidor (ToDo)
# - Iconos para categorias
# 1.0.3
# - First public release
# 1.0.2
# - Minor fixes
# 1.0.1
# - Use public URL
# 1.0.0
# - First release
#---------------------------------------------------------------------------

import os
import sys
import urllib
import urllib2
import json
from datetime import date
from datetime import time
from datetime import datetime
import plugintools
import xbmcgui
import xbmcaddon
import xbmcplugin

addon         = xbmcaddon.Addon('plugin.video.arenavisionezy')
addon_id      = addon.getAddonInfo('id')
addon_name    = addon.getAddonInfo('name')
addon_version = addon.getAddonInfo('version')

# Servidor origen
if addon.getSetting('av_source_server') == "0":
  parserJsonUrl = "http://arenavision.esy.es/json.php"
#elif addon.getSetting('av_source_server') == "1":
#  parserJsonUrl = "http://arenaezy.byethost32.com/json.php"
else:
  parserJsonUrl = "http://arenavision.esy.es/json.php"

# Debug servidor seleccionado
plugintools.log("arenavisionezy Servidor: " + addon.getSetting('av_source_server'))
plugintools.log("arenavisionezy Json: " + parserJsonUrl)

# Entry point
def run():
    #plugintools.log("arenavisionezy.run")

    # Get params
    params = plugintools.get_params()
    plugintools.log("arenavisionezy.run " + repr(params))

    if params.get("action") is None:
        plugintools.log("arenavisionezy.run No hay accion")
        listado_categorias(params)
    else:
        action = params.get("action")
        plugintools.log("arenavisionezy.run Accion: " + action)
        exec action+"(params)"
    
    plugintools.close_item_list()

# Main menu
def listado_categorias(params):
  plugintools.log("arenavisionezy.listado_categorias "+repr(params))

  jsonUrl = parserJsonUrl
  plugintools.log("arenavisionezy.listado_categorias Parsing: " + jsonUrl)
  jsonSrc = urllib2.urlopen(jsonUrl)

  datos = json.load(jsonSrc)
  categorias  = datos['categories']
  last_update = datos['last_update']
  
  # Informacion del evento
  titulo01 = "                    [COLOR skyblue]ArenaVision EZY[/COLOR] Version "+addon_version+" (by Wazzu)"
  titulo02 = "                    [COLOR deepskyblue]Ultima actualizacion: "+last_update+"[/COLOR]"
  plugintools.add_item( title = titulo01 , thumbnail = generar_miniatura('default'), folder = False )
  plugintools.add_item( title = titulo02 , thumbnail = generar_miniatura('default'), folder = False )

  # Todos los eventos
  plugintools.add_item(
    action     = "mostrar_agenda" ,
    title      = "[COLOR deepskyblue][VER AGENDA COMPLETA][/COLOR]",
    plot       = '' ,
    url        = "plugin://plugin.video.arenavisionezy/?action=mostrar_agenda",
    thumbnail  = generar_miniatura('default'),
    isPlayable = True,
    folder     = True
  )

  # Listado de categorias
  for categoria in categorias:
      # Miniatura
      category_thumb = generar_miniatura(categoria['categoria'])
      plugintools.log("arenavisionezy.category_thumb "+category_thumb)
      # Items
      plugintools.add_item(
        action     = "listado_eventos" , 
        title      = categoria['categoria'] + " (" +  categoria['items'] + " eventos)", 
        plot       = '' , 
        url        = "plugin://plugin.video.arenavisionezy/?action=listado_eventos&cat="+urllib.quote(categoria['categoria']),
        thumbnail  = category_thumb,
        isPlayable = True, 
        folder     = True
      )

# Listado de toda la agenda
def mostrar_agenda(params):
  plugintools.log("arenavisionezy.mostrar_agenda "+repr(params))

  # Parse json
  jsonUrl = parserJsonUrl + '?cat=all'
  plugintools.log("arenavisionezy.mostrar_agenda Parsing: " + jsonUrl)
  jsonSrc     = urllib2.urlopen(jsonUrl)
  datos       = json.load(jsonSrc)
  eventos     = datos['eventos']
  last_update = datos['last_update']

  # Titulo de la categoria
  titulo01 = "                [COLOR skyblue]Agenda completa[/COLOR] (actualizado: "+last_update+")"
  plugintools.add_item( title = titulo01 , thumbnail = generar_miniatura('default'), action='', url='', isPlayable = False, folder = False )

  # Para cada evento
  for evento in eventos:
    title     = "[COLOR skyblue]" + evento['fecha'] + " " + evento['hora'] + "[/COLOR] " + evento['titulo']
    plot      = ""
    thumbnail = generar_miniatura(evento['categoria'])
    url       = "plugin://plugin.video.arenavisionezy/?action=listado_canales&evento="+evento['id']
    plugintools.add_item(
      action="listado_canales" ,
      title=title ,
      plot=plot ,
      url=url ,
      thumbnail=thumbnail ,
      isPlayable=True,
      folder=True
    )

# Listado de eventos de una categoria
def listado_eventos(params):
  plugintools.log("Python Version: " + (sys.version))
  plugintools.log("arenavisionezy.listado_eventos "+repr(params))
  categoria = params['cat']
  
  # Parse json
  jsonUrl = parserJsonUrl + '?cat='+urllib.quote(categoria)
  plugintools.log("arenavisionezy.listado_eventos Parsing: " + jsonUrl)
  jsonSrc     = urllib2.urlopen(jsonUrl)
  datos       = json.load(jsonSrc)
  eventos     = datos['eventos']
  last_update = datos['last_update']

  # Titulo de la categoria
  titulo01 = "                [COLOR skyblue]"+categoria+"[/COLOR] (actualizado: "+last_update+")"
  plugintools.add_item( title = titulo01 , thumbnail = generar_miniatura('default'), action='', url='', isPlayable = False, folder = False )
  
  # Para cada evento
  for evento in eventos:
    # ToDo eventos del pasado
    #plugintools.log("Fecha: " + fecha_hora)
    #showDate = datetime.strptime(fecha_hora, "%d/%m/%y %H:%M:%S").date()
    #todayDate = datetime.today().date()
    #if(showDate < todayDate):
    #  color = 'grey'
    #else:
    #  color = 'skyblue'
    color = 'skyblue'
    title     = "[COLOR "+color+"]" + evento['fecha'] + " " + evento['hora'] + "[/COLOR] " + evento['titulo']
    plot      = ""
    thumbnail = generar_miniatura(categoria)
    url       = "plugin://plugin.video.arenavisionezy/?action=listado_canales&evento="+evento['id']
    plugintools.add_item(
      action="listado_canales" , 
      title=title , 
      plot=plot , 
      url=url ,
      thumbnail=thumbnail , 
      isPlayable=True, 
      folder=True
    )

# Listado de canales de un evento
def listado_canales(params):
  plugintools.log("arenavisionezy.listado_canales "+repr(params))
  evento = params['evento']
  
  # Parse json
  jsonUrl = parserJsonUrl + '?evento='+evento
  plugintools.log("arenavisionezy.listado_canales Parsing: " + jsonUrl)
  jsonSrc   = urllib2.urlopen(jsonUrl)
  evento    = json.load(jsonSrc)
  
  # Datos del evento
  categoria = evento['categoria']
  titulo    = evento['titulo']
  fecha     = evento['fecha']
  canales   = evento['canales']

  # Informacion del evento
  titulo01 = "[COLOR skyblue] " + categoria + " - " + fecha + "[/COLOR]"
  plugintools.add_item( title = titulo01 , thumbnail = generar_miniatura('default'), isPlayable = True, folder = True )

  # Canales del evento
  for canal in canales:
    canal_nombre = canal['canal']
    canal_enlace = canal['enlace']
    etiqueta = "[COLOR red][" + canal_nombre + "][/COLOR] " + titulo
    enlace   = "plugin://program.plexus/?url=" + canal_enlace + "&mode=1&name=" + canal_nombre + " " + titulo
    plugintools.add_item( 
      title      = etiqueta , 
      url        = enlace , 
      thumbnail  = generar_miniatura(categoria) ,
      isPlayable = True, 
      folder     = False 
    )

# Ruta de la miniatura
def generar_miniatura(categoria):
  thumb = categoria.lower().replace(" ", "_")
  thumb_path = os.path.dirname(__file__) + "/resources/media/" + thumb + ".png"
  if(os.path.isfile(thumb_path)):
    # Miniatura especifica
    category_thumb = "special://home/addons/" + addon_id + "/resources/media/" + thumb + ".png"
  else:
    # Miniatura generica
    category_thumb = "special://home/addons/" + addon_id + "/resources/media/default.png"
  return category_thumb

# Main loop
run()