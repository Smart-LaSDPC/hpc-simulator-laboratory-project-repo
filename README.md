# Uso de Poetry para Instalar y Ejecutar un Programa en Python

## 1. Instalar Poetry

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

Agregar Poetry al PATH si es necesario:

```bash
export PATH="$HOME/.local/bin:$PATH"
```

Verificar la instalación:

```bash
poetry --version
```

---

## 2. Crear o ingresar a un proyecto

### Entrar a un proyecto existente:

```bash
cd nombre_del_proyecto
```

### Crear un nuevo proyecto:

```bash
poetry new mi_proyecto
cd mi_proyecto
```

---

## 3. Instalar dependencias del proyecto

```bash
poetry install
```

Esto crea automáticamente un entorno virtual aislado.

---

## 4. Activar el entorno virtual

```bash
poetry shell
```

Salir:

```bash
exit
```

---

## 5. Agregar dependencias

### Dependencias normales:
```bash
poetry add requests
```

### Múltiples paquetes:
```bash
poetry add numpy pandas
```

### Dependencias de desarrollo:
```bash
poetry add --dev pytest black
```

---

## 6. Ejecutar tu programa

### Forma 1: Activando el entorno virtual

```bash
poetry shell
python main.py
```

### Forma 2: Sin activar el entorno

```bash
poetry run python main.py
```

---

## 7. Ejecutar scripts definidos en `pyproject.toml`

Ejemplo:

```toml
[tool.poetry.scripts]
start = "mi_paquete.main:run"
```

Ejecutar:

```bash
poetry run start
```

---

## 8. Actualizar dependencias

```bash
poetry update
```

---

## Ejemplo rápido para correr tu aplicación

Si tienes `app.py`:

```bash
poetry install
poetry run python app.py
```

---

