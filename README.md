# Using Poetry to Install and Run a Python Program

## 1. Install Poetry

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

Add Poetry to your PATH if necessary:

```bash
export PATH="$HOME/.local/bin:$PATH"
```

Verify installation:

```bash
poetry --version
```

---

## 2. Create or Enter a Project

### Enter an existing project:

```bash
cd project_name
```

### Create a new project:

```bash
poetry new my_project
cd my_project
```

---

## 3. Install Project Dependencies

```bash
poetry install
```

Poetry will automatically create an isolated virtual environment.

---

## 4. Activate the Virtual Environment

```bash
poetry shell
```

Exit the shell with:

```bash
exit
```

---

## 5. Add Dependencies

### Regular dependencies:
```bash
poetry add requests
```

### Multiple packages:
```bash
poetry add numpy pandas
```

### Development dependencies:
```bash
poetry add --dev pytest black
```

---

## 6. Run Your Program

### Method 1: Activate the virtual environment

```bash
poetry shell
python main.py
```

### Method 2: Run without activating the environment

```bash
poetry run python main.py
```

---

## 7. Run Scripts Defined in `pyproject.toml`

Example:

```toml
[tool.poetry.scripts]
start = "my_package.main:run"
```

Run the script:

```bash
poetry run start
```

---

## 8. Update Dependencies

```bash
poetry update
```

---

## Quick Example to Run Your App

If you have an `app.py` file:

```bash
poetry install
poetry run python app.py
```

---

