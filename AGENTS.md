# AGENTS.md

## Proyecto

`img-a-pfd` — pequeño utilitario de Python ("convertidor de imagen a PDF") que convierte todas las imágenes dentro de cada subdirectorio en un único PDF con el nombre de esa carpeta.

## Comandos

- Instalar dependencias: `pip install fpdf2 pillow tkinterdnd2`
- Interfaz gráfica (Tkinter + tkinterdnd2): `python interfaz.py`
- Ejecutar CLI: `python estilos.py`
- Generar ejecutable: `pyinstaller estilos.spec` (artefactos en `build/` y `dist/`, ambos en `.gitignore`)

## Funcionalidad / GUI

- `interfaz.py`: GUI con Tkinter + `tkinterdnd2`. Arrastrar/soltar carpeta (`DND_FILES`, usar `root.tk.splitlist(event.data)`) o selector de carpeta.
- Formatos aceptados: `.jpg`, `.jpeg`, `.png`, `.webp` (definidos en `EXTENSIONES_IMAGENES` de `estilos.py`).
- Un PDF por subcarpeta detectada con imágenes compatibles.
- Guardado: misma carpeta que la subcarpeta origen, o carpeta de destino elegida manualmente.

## Particularidades

- `estilos.py` es el core reutilizable: `convertir_imagenes_a_pdf(carpeta, extension=..., ruta_salida=...)`; el loop automático está bajo `if __name__ == "__main__":`.
- `estilos.spec` es un spec de PyInstaller, no un archivo de tests.

## Verificación

- No hay suite de tests, linter, type checker ni CI configurado.

## Notas

- Rama actual: `dev_cuenta` (también existe `main`).
- `build/` y `dist/` son artefactos de PyInstaller y están en `.gitignore`.
