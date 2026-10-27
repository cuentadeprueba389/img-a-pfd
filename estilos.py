import os
from fpdf import FPDF

# Función para convertir todas las imágenes en una carpeta a un PDF
def convertir_imagenes_a_pdf(carpeta, extension='.jpg'):
    # Crear una instancia de FPDF
    pdf = FPDF()
    
    # Lista para almacenar los nombres de los archivos de imágenes
    archivos_imagenes = []
    
    # Recorrer todos los archivos en la carpeta
    for archivo in os.listdir(carpeta):
        # Comprobar si el archivo es una imagen con la extensión dada
        if archivo.lower().endswith(extension):
            archivos_imagenes.append(archivo)
    
    # Ordenar la lista de archivos de imágenes
    archivos_imagenes.sort()
    
    # Añadir cada imagen al PDF sin bordes
    for imagen in archivos_imagenes:
        pdf.add_page()
        pdf.image(os.path.join(carpeta, imagen), x=0, y=0, w=210, h=297)
    
    # Guardar el PDF con el nombre de la carpeta
    nombre_pdf = f"{carpeta}.pdf"
    pdf.output(nombre_pdf)
    
    # Retornar el nombre del archivo PDF creado
    return nombre_pdf

# Obtener el directorio actual del script
directorio_script = os.path.dirname(os.path.realpath(__file__))

# Recorrer todas las carpetas en el directorio del script
for carpeta in os.listdir(directorio_script):
    # Comprobar si el elemento es una carpeta
    if os.path.isdir(os.path.join(directorio_script, carpeta)):
        # Llamar a la función para convertir las imágenes en PDF
        nombre_pdf_creado = convertir_imagenes_a_pdf(os.path.join(directorio_script, carpeta))
        
        # Imprimir el resultado
        print(f"Se ha creado el archivo PDF '{nombre_pdf_creado}' con las imágenes de la carpeta '{carpeta}'.")
