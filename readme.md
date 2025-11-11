
# InfoQR

InfoQR es una aplicación web accesible que permite compartir información personal relevante mediante códigos QR o un ID único, facilitando la comunicación y el acceso a datos esenciales, especialmente para personas con dificultades en la comunicación o el habla.

## Descripción del Proyecto

**InfoQR** es una aplicación web diseñada para mejorar la comunicación y el acceso a información personal relevante mediante el uso de **códigos QR** o un **ID único de usuario**. Su propósito es facilitar el intercambio de datos esenciales —como información de contacto, médica o de preferencias personales— de forma rápida, segura y accesible.

La aplicación está especialmente orientada a **personas con discapacidad intelectual o dificultades en la comunicación**, brindándoles una herramienta digital que promueve la **autonomía, inclusión y seguridad**. A través de una interfaz simple e intuitiva, terceros (como acompañantes, profesionales o personal de salud) pueden acceder fácilmente a la información necesaria para ofrecer asistencia adecuada o entablar una interacción respetuosa.

En síntesis, InfoQR busca **reducir barreras comunicativas y favorecer la comprensión mutua**, combinando accesibilidad, usabilidad y control sobre la información compartida.

## Puesta en Producción

El sistema está preparado para desplegarse fácilmente mediante Docker Compose, garantizando un entorno reproducible y aislado.

### Despliegue

Para levantar el sistema, simplemente ejecutar en el directorio raíz del proyecto:

```
docker compose up -d
```

Esto iniciará dos servicios:
- `database` → Servicio PostgreSQL.
- `app` → Aplicación web InfoQR.

### Configuración requerida antes del despliegue

Antes de poner el sistema en producción, es **imprescindible** modificar las siguientes variables de entorno en el archivo `compose.yml`:

- `POSTGRES_PASSWORD`: Contraseña del usuario de la base de datos. Debe reemplazarse por una contraseña segura. También debe modificarse la variable de entorno `database_password` para coincidir con este valor.

- `secret_key`: Clave secreta utilizada por Flask para sesiones y cifrado interno. Cambiar por un valor aleatorio seguro. Puede ser generado con `python -c 'import secrets; print(secrets.token_hex())'`.

- `base_url`: URL base del dominio donde se alojará el sistema. Es utilizado para la generación de URLs que serán codificadas en los códigos QR (por ejemplo: https://infoqr.mi-dominio.com.ar).

### Persistencia

El volumen `./instance/postgres` almacena los datos de PostgreSQL de forma persistente.

### Consideraciones de seguridad

- El contenedor de la aplicación se ejecuta con un usuario sin privilegios (`nobody:nogroup`) y en modo de solo lectura (`read_only: true`), siguiendo el principio de mínimo privilegio.

## Desarrollo

Esta sección describe cómo preparar el entorno de desarrollo y ejecutar la aplicación **InfoQR** localmente.

### 1. Crear entorno virtual

Se recomienda utilizar un entorno virtual para aislar las dependencias del proyecto.

```bash
python -m venv env
source env/bin/activate  # En Linux/Mac
env\Scripts\activate     # En Windows
```

### 2. Instalar dependencias

Con el entorno activado, instalar las dependencias requeridas desde el archivo `requirements.txt`:

```bash
pip install -r requirements.txt
```

### 3. Configurar variables de entorno

#### Generar una clave secreta (`secret_key`)

```bash
python -c 'import secrets; print(secrets.token_hex())'
```

#### Crear archivo `.env`

Se puede crear un archivo `.env` para definir las variables de entorno.

```bash
# base
environment="development"
secret_key="<clave_generada>"
base_url="http://localhost:5000"

# development
database_sqlite_file="database.db"
```

### 4. Ejecutar la aplicación

Iniciar el servidor Flask en modo desarrollo con recarga automática:

```bash
flask --app app run --debug
```

La aplicación estará disponible en: http://localhost:5000

## Equipo de desarrollo
- Maturo Agustín
- Pereyra Iyael Lihue

## Institución

Proyecto desarrollado en el marco de la materia **Diseño de Experiencia de Usuario**, perteneciente a la **Facultad de Informática** de la **Universidad Nacional de La Plata (UNLP)**.
