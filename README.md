# img-a-pfd

Convertidor de imágenes a PDF. Crea un PDF por carpeta con el nombre de la misma.

## Requisitos

- Python 3
- `fpdf2` y `pillow` (para formatos como `.webp`): `pip install fpdf2 pillow`
- `tkinterdnd2` (interfaz gráfica): `pip install tkinterdnd2`

## Uso con interfaz gráfica (Tkinter)

```
python interfaz.py
```

- Arrastrá una carpeta con imágenes y soltéala, o usá "Seleccionar carpeta".
- Se detectan subcarpetas con imágenes (`.jpg`, `.jpeg`, `.png`, `.webp`) y se genera un PDF por subcarpeta.
- Opciones de guardado:
  - "En la misma carpeta que la subcarpeta origen" (PDF junto a las subcarpetas).
  - "Elegir carpeta de destino" manualmente.

## Uso desde terminal

```
python estilos.py
```
