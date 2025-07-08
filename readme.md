
# Info QR

## Desarrollo

### Entorno virtual
```bash
python3 -m venv env
```

### Dependencias
```bash
pip install -r requirements.txt
```

### Archivo de configuración (.env)

#### Generar "secret_key"

```bash
python -c 'import secrets; print(secrets.token_hex())'
```

#### Archivo ".env"

```bash
# base
environment = "development"
secret_key = ""
base_url = "http://localhost:5000"

# development
database_sqlite_file="database.db"
```

### Ejecutar
```bash
flask --app app run --debug
```