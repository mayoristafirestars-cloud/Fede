"""Immutable photo references and audited additions to commercial documents."""
import re
from pathlib import Path

def safe_photo(value):
    return value if isinstance(value,str) and re.fullmatch(r'/media/[0-9a-f]{32}\.jpg',value) else ''

def available_photo(value):
    from routers import preparacion
    value=safe_photo(value)
    return value if value and (Path(preparacion.MEDIA_DIR)/value.rsplit('/',1)[1]).is_file() else ''

def effective_photo(conn,origin,item_id,snapshot):
    row=conn.execute('SELECT foto FROM fotos_documento WHERE origen=? AND item_id=? ORDER BY id DESC LIMIT 1',(origin,item_id)).fetchone()
    return safe_photo(row[0]) if row else safe_photo(snapshot)
