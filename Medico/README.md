# Médico — Sistema de Gestión de Profesionales de la Salud

Sistema simple para registrar médicos y nutricionistas, sus pacientes y consultas.

## Instalación
```
pip install -r requirements.txt
```

## Iniciar el sistema
```
cd backend
python main.py
```
El navegador se abre en `http://localhost:8001`

## Estructura
```
Medico/
├── backend/
│   ├── db/
│   │   ├── schema.sql          ← estructura de la base de datos
│   │   └── database.py         ← conexión SQLite
│   ├── routers/
│   │   └── profesionales.py    ← endpoints médicos/nutricionistas
│   └── main.py                 ← servidor FastAPI
├── frontend/
│   ├── templates/index.html
│   └── static/
├── data/                       ← SQLite DB
└── requirements.txt
```

## Endpoints principales
- `GET  /`                       → interfaz web
- `GET  /api/estado`             → conteos
- `GET  /api/profesionales`      → listar (filtros: `tipo`, `buscar`)
- `POST /api/profesionales`      → crear médico o nutricionista
- `GET  /api/profesionales/{id}` → detalle
- `PUT  /api/profesionales/{id}` → actualizar
- `DELETE /api/profesionales/{id}` → baja lógica
