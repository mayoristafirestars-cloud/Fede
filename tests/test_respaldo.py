import importlib.util
from pathlib import Path
import sqlite3
import tarfile
import tempfile
import unittest

spec = importlib.util.spec_from_file_location('respaldo', Path(__file__).resolve().parents[1] / 'scripts/respaldo.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class BackupTests(unittest.TestCase):
    def test_live_wal_and_photos_restore(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            media = root / 'photos'
            media.mkdir()
            (media / 'product.jpg').write_bytes(b'image fixture')
            db = root / 'source.db'
            with sqlite3.connect(db) as conn:
                conn.execute('PRAGMA journal_mode=WAL')
                conn.execute('CREATE TABLE data(value TEXT)')
                conn.execute('INSERT INTO data VALUES(?)', ('Nativa',))
                conn.commit()
                output = module.backup(db, media, root / 'backup.tar.gz')
                self.assertEqual(output.stat().st_mode & 0o777, 0o600)
                restored = root / 'restore'
                with tarfile.open(output) as archive:
                    archive.extractall(restored, filter='data')
                with sqlite3.connect(restored / 'nativa.db') as target:
                    self.assertEqual(target.execute('SELECT value FROM data').fetchone()[0], 'Nativa')
                self.assertEqual((restored / 'uploads/product.jpg').read_bytes(), b'image fixture')
                with self.assertRaises(FileExistsError):
                    module.backup(db, media, output)
                with self.assertRaises(ValueError):
                    module.backup(db, media, media / 'recursive.tar.gz')
