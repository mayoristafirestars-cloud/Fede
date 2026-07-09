# Coronel Sur — Sistema de Gestión

## Instalación (una sola vez)
1. Doble click en `instalar.bat`

## Importar datos de FactuPyme
1. Exportar desde FactuPyme:
   - **Inventario** → guardar como `inventario.csv`
   - **Informe de Ventas** → guardar como `ventas.csv`
   - **Informe de Presupuestos** → guardar como `presupuestos.csv`
2. Copiar los 3 archivos a la carpeta `data/csv_originales/`
3. Doble click en `importar.bat`

## Iniciar el sistema
- Doble click en `iniciar.bat`
- El navegador se abre en `http://localhost:8000`

## Verificar que todo está bien
- Ir a `http://localhost:8000/api/estado`
- Debe mostrar los conteos de productos, clientes y ventas

## Estructura del proyecto
```
coronel-sur/
├── backend/
│   ├── db/
│   │   ├── schema.sql          ← estructura de la base de datos
│   │   └── database.py         ← conexión a SQLite
│   ├── importador/
│   │   └── importar_factupyme.py ← importa los CSVs
│   └── main.py                 ← servidor FastAPI
├── frontend/
│   └── static/                 ← CSS, JS, imágenes
├── data/
│   └── csv_originales/         ← pegar aquí los CSVs de FactuPyme
├── instalar.bat
├── importar.bat
└── iniciar.bat
```
