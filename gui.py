import customtkinter as ctk
from tkcalendar import Calendar
import tkinter as tk
from datetime import datetime
from PIL import Image, ImageTk
import requests
import os
import manager_marketdata as mkd
import graph as g


# Tema dark-blue 
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

# Variables globales para guardar las selecciones
valor_seleccionado = None
fecha_inicio_seleccionada = None
fecha_fin_seleccionada = None

# Variable global para almacenar las imágenes
imagenes = {}

# Función para obtener los valores desde crypto.txt
def leer_valores_desde_archivo(filename):
    try:
        with open(filename, 'r') as file:
            valores = [line.strip() for line in file if line.strip()]
        return valores
    except FileNotFoundError:
        print(f"El archivo {filename} no se encontró.")
        return []

# Ventana principal (titulo, tamaño)
ventana = ctk.CTk()
ventana.title("KuCoin Price Retrieval")
ventana.geometry("400x850")
ventana.resizable(True, True)

def obtener_identificador_coin(symbol):
    """
    Obtiene el identificador de CoinGecko basado en el símbolo de la criptomoneda.

    Args:
        symbol (str): Símbolo de la criptomoneda.
    """
    coingecko_list_url = "https://api.coingecko.com/api/v3/coins/list"
    response = requests.get(coingecko_list_url)
    coins_list = response.json()
    
    if symbol == 'btc': # Caso especial para Bitcoin
        symbol = 'bitcoin'
        return symbol
    else:
        for coin in coins_list:
            if coin['symbol'].lower() == symbol:
                return coin['id']
            
    return None


# Función para cargar las imágenes correspondientes a las criptomonedas
def cargar_imagenes(valores):
    """
    Carga las imágenes de las criptomonedas en la carpeta 'cryptoimg'.

    Args:
        valores (list): Lista de valores de criptomonedas en formato 'symbol-currency' (ejemplo: 'btc-usd').
    """
    global imagenes  # Declarar global para evitar recolección de basura
    print("Cargando imágenes...")

    for valor in valores:
        print(f"Cargando imagen para {valor}...")
        ruta_imagen = os.path.join("cryptoimg", f"{valor.split('-')[0].upper()}.png")
        if os.path.exists(ruta_imagen):
            imagen = Image.open(ruta_imagen)
            imagen = imagen.resize((20, 20), Image.Resampling.LANCZOS)  # Redimensionar la imagen
            imagenes[valor] = ImageTk.PhotoImage(imagen, master=ventana)  # Asegurar que la imagen esté vinculada a la ventana principal
        else:
            # Obtener símbolo de la criptomoneda (solo la primera parte antes del guion)
            symbol = valor.split('-')[0].lower()
            
            # Obtener el identificador de CoinGecko
            coin_id = obtener_identificador_coin(symbol)

            print(f"Identificador de CoinGecko para {symbol}: {coin_id}")
            
            if coin_id:
                # Buscar la imagen en CoinGecko usando el identificador
                coingecko_url = f"https://api.coingecko.com/api/v3/coins/{coin_id}"
                response = requests.get(coingecko_url)
                crypto_data = response.json()
                
                if 'image' in crypto_data and 'large' in crypto_data['image']:
                    img_url = crypto_data['image']['large']
                    img_data = requests.get(img_url).content
                    
                    # Guardar la imagen en la carpeta 'cryptoimg'
                    with open(ruta_imagen, 'wb') as handler:
                        handler.write(img_data)
                    print(f"Imagen de {crypto_data['name']} guardada como {ruta_imagen}")
                    
                    # Cargar y redimensionar la imagen
                    imagen = Image.open(ruta_imagen)
                    imagen = imagen.resize((20, 20), Image.Resampling.LANCZOS)
                    imagenes[valor] = ImageTk.PhotoImage(imagen, master=ventana)
                else:
                    print(f"No se encontró la imagen para {valor}.")
            else:
                print(f"No se encontró el identificador de CoinGecko para {symbol}.")


# Leer los valores del archivo crypto.txt
valores = leer_valores_desde_archivo("crypto.txt")

# Cargar las imágenes ahora que la ventana está creada
cargar_imagenes(valores)


"""
    Elegir activo
"""

ruta_imagenes = "cryptoimg"

# Función para actualizar el valor seleccionado y la imagen correspondiente
def actualizar_seleccion(valor):
    """
    Actualiza el valor seleccionado (activo) y la imagen correspondiente en el Canvas.

    Args:
        valor (str): Valor seleccionado (activo) en el menú desplegable.
    """
    global valor_seleccionado
    valor_seleccionado = valor

    ruta_imagen = os.path.join(ruta_imagenes, f"{valor.split('-')[0].upper()}.png")
    print(f"Ruta de la imagen: {ruta_imagen}") # Imprimir la ruta de la imagen

    if os.path.exists(ruta_imagen):
        print(f"Cargando imagen para {valor}...")
        imagen = Image.open(ruta_imagen)
        imagen = imagen.resize((100, 100), Image.Resampling.LANCZOS)  # Redimensionar a 100x100 píxeles
        
        # Crear una referencia separada para la imagen grande
        imagen_grande = ImageTk.PhotoImage(imagen, master=ventana)
        
        # Actualizar el Canvas con la nueva imagen
        canvas_imagen.create_image(0, 0, anchor='nw', image=imagen_grande)
        canvas_imagen.image = imagen_grande  # Mantener una referencia a la imagen grande

    print(f"Valor seleccionado: {valor_seleccionado}")

# Crear un Canvas para mostrar la imagen
canvas_imagen = tk.Canvas(ventana, width=100, height=100)
canvas_imagen.pack(side='top', padx=10, pady=30)  # Colocar el Canvas a la izquierda

# Menú desplegable personalizado con imágenes
etiqueta_valores = ctk.CTkLabel(ventana, text="Seleccione un activo:")
etiqueta_valores.pack(pady=10)

# Variable para almacenar la opción seleccionada
opcion_seleccionada = tk.StringVar(ventana)
opcion_seleccionada.set(valores[0])  # Establecer un valor predeterminado

variable_activo = tk.StringVar(ventana)
variable_activo.set(valores[0])

# Menú desplegable con imágenes para los activos disponibles de crypto.txt
menu_desplegable = tk.OptionMenu(ventana, opcion_seleccionada, *valores, command=actualizar_seleccion)
menu_desplegable.config(bg="#2b2b2b", fg="white", activebackground="#3e3e3e", activeforeground="white")
menu_desplegable["menu"].config(bg="#2b2b2b", fg="white", activebackground="#3e3e3e", activeforeground="white")

for i, valor in enumerate(valores):
    if valor in imagenes:
        menu_desplegable["menu"].entryconfig(i, image=imagenes[valor], compound="left")

menu_desplegable.pack(pady=10)

"""
    Funciones para la validacion y seleccion de fechas
"""

# Función para validar que la fecha seleccionada no sea posterior a la fecha actual
def validar_fecha(fecha, tipo_fecha):
    """
    Verifica que la fecha seleccionada no sea posterior a la fecha actual.

    Args:
        fecha (str): Fecha en formato "dd/mm/yyyy HH:MM".
        tipo_fecha (str): Tipo de fecha ("inicio" o "fin").

    Returns:
        bool: True si la fecha es válida, False si no lo es.
    """
    fecha_actual = datetime.now()
    fecha_seleccionada = datetime.strptime(fecha, "%d/%m/%Y %H:%M")
    
    if fecha_seleccionada > fecha_actual:
        tk.messagebox.showerror("Fecha no válida", f"La fecha de {tipo_fecha} no puede ser posterior a la fecha actual.")
        return False
    return True

# Función para seleccionar la fecha y la hora
def seleccionar_fecha(etiqueta_fecha, tipo_fecha):
    """
    Abre una ventana para seleccionar la fecha y la hora

    Args:
        etiqueta_fecha (tk.Label): Etiqueta para mostrar la fecha seleccionada.
        tipo_fecha (str): Tipo de fecha ("inicio" o "fin").
    """
    def obtener_fecha():
        """
        Obtiene la fecha seleccionada y la hora, y la muestra en la etiqueta correspondiente.
        """
        fecha_seleccionada = calendario.get_date()
        hora_seleccionada = f"{spin_horas.get()}:{spin_minutos.get()}"
        fecha_y_hora = f"{fecha_seleccionada} {hora_seleccionada}"

        if validar_fecha(fecha_y_hora, tipo_fecha):
            etiqueta_fecha.configure(text=f"Fecha seleccionada: {fecha_y_hora}")
            
            # Guardar la fecha en la variable correspondiente
            global fecha_inicio_seleccionada, fecha_fin_seleccionada
            if tipo_fecha == 'inicio':
                fecha_inicio_seleccionada = fecha_y_hora
            else:
                fecha_fin_seleccionada = fecha_y_hora
            
            calendario_window.destroy()

    calendario_window = tk.Toplevel(ventana)
    calendario_window.title("Seleccionar Fecha")

    calendario = Calendar(calendario_window, selectmode='day', date_pattern='dd/mm/y')
    calendario.pack(pady=20)

    # Spinboxes para seleccionar la hora y los minutos
    spin_horas = tk.Spinbox(calendario_window, from_=0, to=23, wrap=True, width=5, format="%02.0f")
    spin_horas.pack(side="left", padx=(10, 0))
    spin_minutos = tk.Spinbox(calendario_window, from_=0, to=59, wrap=True, width=5, format="%02.0f")
    spin_minutos.pack(side="left", padx=(0, 10))

    boton_obtener_fecha = ctk.CTkButton(calendario_window, text="Obtener Fecha", command=obtener_fecha)
    boton_obtener_fecha.pack(pady=10)

"""
    Fechas    
"""

# Etiquetas para mostrar las fechas seleccionadas
etiqueta_fecha_inicio = ctk.CTkLabel(ventana, text="Fecha de inicio: Ninguna")
etiqueta_fecha_inicio.pack(pady=10)

etiqueta_fecha_fin = ctk.CTkLabel(ventana, text="Fecha de fin: Ninguna")
etiqueta_fecha_fin.pack(pady=10)

# Botones para elegir fechas
boton_fecha_inicio = ctk.CTkButton(ventana, text="Seleccionar Fecha Inicio", command=lambda: seleccionar_fecha(etiqueta_fecha_inicio, 'inicio'))
boton_fecha_inicio.pack(pady=10)

boton_fecha_fin = ctk.CTkButton(ventana, text="Seleccionar Fecha Fin", command=lambda: seleccionar_fecha(etiqueta_fecha_fin, 'fin'))
boton_fecha_fin.pack(pady=10)


"""
    Temporalidades 
"""

# Array de temporalidades
temporalidades = ['1min', '5min', '15min', '1hour', '4hour', '8hour', '1day', '1week', '1month']

# Función para actualizar la temporalidad seleccionada
def actualizar_temporalidad(temporalidad):
    """
    Actualiza la temporalidad seleccionada.

    Args:
        temporalidad (str): Temporalidad seleccionada.
    """
    global temporalidad_seleccionada
    temporalidad_seleccionada = temporalidad
    print(f"Temporalidad seleccionada: {temporalidad_seleccionada}")

# Menú desplegable temporalidad
etiqueta_temporalidad = ctk.CTkLabel(ventana, text="Seleccione la temporalidad:")
etiqueta_temporalidad.pack(pady=10)

# Variable para almacenar la temporalidad seleccionada
opcion_temporalidad = tk.StringVar(ventana)
opcion_temporalidad.set(temporalidades[0])  # Valor predeterminado

menu_temporalidad = tk.OptionMenu(ventana, opcion_temporalidad, *temporalidades, command=actualizar_temporalidad)
menu_temporalidad.config(bg="#2b2b2b", fg="white", activebackground="#3e3e3e", activeforeground="white")
menu_temporalidad["menu"].config(bg="#2b2b2b", fg="white", activebackground="#3e3e3e", activeforeground="white")

menu_temporalidad.pack(pady=10)



"""
    Botones para mostrar y obtener selecciones
"""

# Función para obtener y mostrar las selecciones
def obtener_seleccion():
    """
    Obtiene y muestra las selecciones realizadas por el usuario (consola).
    """
    global valor_seleccionado
    valor_seleccionado = opcion_seleccionada.get()

    # Imprimir los valores seleccionados
    try:
        print(f"Valor seleccionado: {valor_seleccionado}")
    except NameError:
        print("No se ha seleccionado un valor.")

    try:
        print(f"Temporalidad seleccionada: {temporalidad_seleccionada}")
    except NameError:
        print("No se ha seleccionado una temporalidad.")

    try:
        print(f"Fecha de inicio seleccionada: {fecha_inicio_seleccionada}")
    except NameError:
        print("No se ha seleccionado una fecha de inicio.")

    try:
        print(f"Fecha de fin seleccionada: {fecha_fin_seleccionada}")
    except NameError:
        print("No se ha seleccionado una fecha de fin.")

# Botón para imprimir las selecciones
boton_mostrar_seleccion = ctk.CTkButton(ventana, text="Mostrar Selección", command=obtener_seleccion)
boton_mostrar_seleccion.pack(pady=20)


"""
    Si se desea añadir medias moviles exponenciales (EMAs) a los precios
"""

# Función para añadir EMAs
def añadir_emas():
    """
    Abre una ventana emergente para añadir EMAs.
    """
    def agregar_ema():
        """
        Agrega una EMA a la lista de EMAs.
        """
        ema_valor = entry_ema.get()
        if ema_valor:
            emas.append(int(ema_valor))
            entry_ema.delete(0, tk.END)
            print(f"EMA añadida: {ema_valor}")

    def validar_emas():
        """
        Valida las EMAs ingresadas y cierra la ventana emergente.
        """
        if emas:
            emas_window.destroy()
            print("EMAs validadas")
        else:
            tk.messagebox.showerror("Error", "Debe agregar al menos una EMA")

    emas_window = tk.Toplevel(ventana)
    emas_window.title("Añadir EMAs")

    # Etiqueta y campo de entrada para agregar EMAs
    etiqueta_ema = ctk.CTkLabel(emas_window, text="Añadir EMA:")
    etiqueta_ema.pack(pady=10)

    entry_ema = ctk.CTkEntry(emas_window)
    entry_ema.pack(pady=10)

    # Botón para agregar EMA
    boton_agregar_ema = ctk.CTkButton(emas_window, text="Agregar EMA", command=agregar_ema)
    boton_agregar_ema.pack(pady=10)

    # Botón para validar EMAs
    boton_validar_emas = ctk.CTkButton(emas_window, text="Validar EMAs", command=validar_emas)
    boton_validar_emas.pack(pady=10)

# Array para almacenar las EMAs
emas = []

# Botón para añadir EMAs
boton_emas = ctk.CTkButton(ventana, text="Añadir EMAs", command=añadir_emas)
boton_emas.pack(pady=10)

"""
    Casilla por si se quiere graficar los precios

"""

# Variable para almacenar si se desea graficar los precios
global graficar_precios
graficar_precios = tk.BooleanVar(ventana)
graficar_precios.set(True)

# Casilla para graficar precios
casilla_graficar = ctk.CTkCheckBox(ventana, text="Graficar precios", variable=graficar_precios)
casilla_graficar.pack(pady=10)

"""
# Función para imprimir el estado actual de graficar_precios
def imprimir_estado_graficar_precios():
    print(f"Graficar precios: {graficar_precios.get()}")

# Botón para imprimir el estado actual de graficar_precios
boton_imprimir_estado = tk.Button(ventana, text="Imprimir estado", command=imprimir_estado_graficar_precios)
boton_imprimir_estado.pack(pady=10)
"""

# Arreglar problema con imagenes del menu desplegable ¿sera por el png vacio que hemos creado?

"""

    Obtener Precios
"""

# Función para "Obtener Precios"
def obtener_precios():
    """
    Obtiene los precios para el valor seleccionado, la temporalidad, y las fechas seleccionadas,
    guardandolas en un excel
    """
    print("Obteniendo precios para:")
    print(f"Valor seleccionado: {valor_seleccionado}")
    print(f"Temporalidad seleccionada: {temporalidad_seleccionada}")
    print(f"Fecha de inicio: {fecha_inicio_seleccionada}")
    print(f"Fecha de fin: {fecha_fin_seleccionada}")
    # Aquí puedes añadir el código para obtener los precios

    coin = valor_seleccionado

    fecha_hora = datetime.strptime(fecha_inicio_seleccionada, "%d/%m/%Y %H:%M")
    startDate = [fecha_hora.year, fecha_hora.month, fecha_hora.day, fecha_hora.hour, fecha_hora.minute, 0]
    
    fecha_hora = datetime.strptime(fecha_fin_seleccionada, "%d/%m/%Y %H:%M")
    endDate = [fecha_hora.year, fecha_hora.month, fecha_hora.day, fecha_hora.hour, fecha_hora.minute, 0]

    data, excelFile = mkd.obtainData(coin, temporalidad_seleccionada, startDate, endDate, mav=emas)

    if excelFile:
        tk.messagebox.showinfo("Guardado exitoso", f"Se han guardado correctamente los precios de la moneda {coin} con temporalidad {temporalidad_seleccionada} desde {fecha_inicio_seleccionada} a {fecha_fin_seleccionada} en el archivo {excelFile}")
    
        if graficar_precios.get():
            g.represent_graphic_excel(excelFile, mav=emas)
    else:
        tk.messagebox.showerror("Error", "No se pudo guardar el archivo de precios")

# Botón para obtener precios
boton_obtener_precios = ctk.CTkButton(ventana, text="Obtener Precios", command=obtener_precios)
boton_obtener_precios.pack(pady=20)

# Iniciar la aplicación
ventana.mainloop()


# Arreglar problema con imagenes del menu desplegable ¿sera por el png vacio que hemos creado?
# Comprobar que existen las imagenes de las criptomonedas en la carpeta cryptoimg y manejar el error
# Dejar seleccionada una temporalidad por defecto en el menu desplegable