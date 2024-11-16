# Introducción 👋

...

## Backend

...

### API

Para la API se utilizó [fastAPI](https://fastapi.tiangolo.com).

#### Requisitos:

1. Instalar [Python](https://www.python.org/downloads/) para poder ejecutar los comandos de pip.
2. Entorno virtual y dependencias:

   - Crear un entorno virtual:
      ```bash
      python -m venv venv
      ```
   - Activar el entorno virtual:

      En Windows:

      ```bash
      .\venv\Scripts\activate
      ```
      
      En Linux/Mac:
      ```bash
      . venv/bin/activate
      ```
   - Instalar las dependencias:
      ```bash
      pip install -r requirements.txt
      ```
3. Iniciar la API desde la carpeta src:

      ```bash
      uvicorn API.main:app --reload
      ```


## App Móvil

La aplicación movil se creó con [React Native](https://reactnative.dev/docs/environment-setup) con el siguiente comando:
```
npx create-expo-app@latest
```

### Pre-requisitos:
1. Instalar [Node.js](https://nodejs.org/en)  para poder ejecutar los comandos de npm.
2. Instalar [Android Studio](https://developer.android.com/studio) para poder emular la aplicación en un dispositivo virtual.


### Comenzando

1. Instalar dependencias

   ```bash
   npm install
   ```

2. Iniciar la aplicación

   ```bash
    npx expo start
   ```

Luego se debe iniciar el emulador de Android Studio para poder visualizar la aplicación. con la tecla "a" se abrirá la aplicación en el emulador.
Tambien se puede escanear el código QR con la aplicación de Expo Go en un dispositivo móvil.
