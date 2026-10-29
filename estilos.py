import os
from fpdf import FPDF

EXTENSIONES_IMAGENES = ('.jpg', '.jpeg', '.png', '.webp')


def _extensiones_a_comprobar(extension):
    if isinstance(extension, str):
        return (extension.lower(),)
    return tuple(ext.lower() for ext in extension)


def convertir_imagenes_a_pdf(carpeta, extension=EXTENSIONES_IMAGENES, ruta_salida=None):
    # Función para convertir las imágenes en una carpeta a un PDF
    pdf = FPDF()

    archivos_imagenes = []
    extensiones = _extensiones_a_comprobar(extension)

    # Recorrer todos los archivos en la carpeta
    for archivo in sorted(os.listdir(carpeta)):
        # Comprobar si el archivo es una imagen con una de las extensiones dadas
        if archivo.lower().endswith(extensiones):
            archivos_imagenes.append(archivo)

    # Ordenar la lista de archivos de imágenes
    archivos_imagenes.sort()

    # Añadir cada imagen al PDF sin bordes
    for imagen in archivos_imagenes:
        pdf.add_page()
        pdf.image(os.path.join(carpeta, imagen), x=0, y=0, w=210, h=297)

    # Guardar el PDF (por defecto con el nombre de la carpeta)
    if ruta_salida is None:
        ruta_salida = f"{carpeta}.pdf"
    pdf.output(ruta_salida)

    # Retornar el nombre del archivo PDF creado
    return ruta_salida


if __name__ == "__main__":
    # Obtener el directorio actual del script
    directorio_script = os.path.dirname(os.path.realpath(__file__))

    # Recorrer todas las carpetas en el directorio del script
    for carpeta in sorted(os.listdir(directorio_script)):
        ruta_carpeta = os.path.join(directorio_script, carpeta)
        if os.path.isdir(ruta_carpeta):
            nombre_pdf_creado = convertir_imagenes_a_pdf(ruta_carpeta)
            print(f"Se ha creado el archivo PDF '{nombre_pdf_creado}' con las imágenes de la carpeta '{carpeta}'.")
