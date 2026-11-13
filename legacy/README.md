# legacy/ — versión anterior (no se usa)

Esta carpeta guarda la primera versión del sistema, que quedó reemplazada por `backend/`:

- `database/schema.py`: esquema viejo (tablas `facturas`, `factura_items`, `movimientos_stock`, `log_importacion`).
- `importador/importar.py` y `importador/verificar.py`: importador y verificador viejos, que escriben en `data/coronel_sur.db`.

**Nada de esto se ejecuta.** Los `.bat`, el servidor y el importador vigente usan `backend/`.

La base de datos vieja (`data/coronel_sur.db`, con 5 productos de prueba) no se sube al repositorio porque las bases de datos están excluidas por `.gitignore`. Sigue disponible dentro de `coronel-sur-render_1.zip`, que es el respaldo original del proyecto.
