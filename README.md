# 💹 Obtención de precios históricos de Criptomonedas con Interfaz Gráfica

Este programa te permite obtener, consultar y visualizar precios de criptomonedas utilizando una interfaz intuitiva. A partir de un archivo de texto (`crypto.txt`) con una lista de criptomonedas, podrás elegir la que desees, seleccionar su temporalidad, añadir medias móviles exponenciales (EMAs) y ver todo representado en una **gráfica interactiva**, incluyendo la imagen oficial del activo.

---

## 📦 Funcionalidades

- 📂 **Carga automática de criptomonedas** desde el archivo `crypto.txt`.
- 🧠 **Interfaz gráfica amigable** para seleccionar criptomoneda y temporalidad.
- 🖼️ **Descarga y visualización de la imagen** del logo de la criptomoneda.
- 🕒 **Soporte para múltiples temporalidades** (por ejemplo: 1m, 5m, 15m, 1h, 1d...).
- 📈 **Gráfica de precios** con opción de añadir **EMAs personalizadas**.
- 🔍 Visualización clara del precio y comportamiento del activo a lo largo del tiempo.

---

## 🗃️ Estructura esperada del archivo `crypto.txt`

El archivo `crypto.txt` debe contener un listado de criptomonedas con su **símbolo reconocido por la API o fuente de datos**. Ejemplo:

BTC-USDT
ETH-USDT
XRP-USDT
SOL-USDT
ADA-USDT
LTC-USDT

---

## ⚙️ Requisitos e instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/alejandrorodm/Crypto-Price-Retrieval
cd Crypto-Price-Retrieval
```

2. Instalar dependencias
```bash
pip install -r requirements.txt
```

---

## 🚀 Cómo ejecutar

1. Asegúrate de tener **Python 3.8+** y los siguientes paquetes instalados:

   ```bash
   python gui.py
   ```
   
Se abrirá una ventana gráfica donde podrás:
- Seleccionar una criptomoneda.
- Elegir una temporalidad.
- Añadir EMAs personalizadas (como 20, 50, 200).
- Visualizar precios y logos de las criptomonedas.
- Exportar datos a un archivo Excel.
  
## 📦 Tecnologías utilizadas

- `tkinter` — Interfaz gráfica.
- `kucoin-python` — API oficial para datos de mercado.
- `openpyxl` — Gestión y edición de archivos Excel.
- `pandas` — Manipulación de datos.
- `threading`, `math`, `datetime` — Utilidades para ejecución eficiente y manipulación de datos.

---

## 👨‍💻 Autor

**Alejandro Rodríguez Moreno**

---

## 🪪 Licencia

Este proyecto está bajo la licencia MIT. Puedes usarlo, modificarlo y distribuirlo libremente.




