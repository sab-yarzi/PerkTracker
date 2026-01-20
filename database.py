import hashlib
import sqlite3
from contextlib import contextmanager
from typing import List

from models import SingularPerk, PerkList

DB_PATH = 'perks.db'
def get_perk_hash(perk: SingularPerk) -> str:
    key_str = f"{perk.company_name.lower()}|{perk.offer_text}"
    return hashlib.md5(key_str.encode()).hexdigest()

@contextmanager
def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

def init_db():
    """Create tables if they don't exist."""
    with get_db_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS perks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                hash TEXT UNIQUE NOT NULL,
                company_name TEXT NOT NULL,
                offer_text TEXT NOT NULL,
                expiry_text TEXT,
                conditions_text TEXT,
                percentage_value REAL,
                minimum_spend REAL,
                money_back REAL,
                cap_amount REAL,
                confidence REAL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_company ON perks(company_name)
        """)
        conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_hash ON perks(hash)
        """)


def save_perks(perk_list: PerkList) -> dict:
    """
    Save perks to database, skip duplicates.
    """
    inserted = 0
    skipped = 0

    with get_db_connection() as conn:
        for perk in perk_list.perks:
            perk_hash = get_perk_hash(perk)

            try:
                conn.execute("""
                             INSERT INTO perks (hash, company_name, offer_text, expiry_text, conditions_text,
                                                percentage_value, minimum_spend, money_back, cap_amount, confidence)
                             VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                             """, (
                                 perk_hash,
                                 perk.company_name,
                                 perk.offer_text,
                                 perk.expiry_text,
                                 perk.conditions_text,
                                 perk.percentage_value,
                                 perk.minimum_spend,
                                 perk.money_back,
                                 perk.cap_amount,
                                 perk.confidence
                             ))
                inserted += 1
            except sqlite3.IntegrityError:
                # Duplicate hash, update instead
                conn.execute("""
                             UPDATE perks
                             SET expiry_text      = ?,
                                 conditions_text  = ?,
                                 percentage_value = ?,
                                 minimum_spend    = ?,
                                 money_back       = ?,
                                 cap_amount       = ?,
                                 confidence       = ?,
                                 updated_at       = CURRENT_TIMESTAMP
                             WHERE hash = ?
                             """, (
                                 perk.expiry_text,
                                 perk.conditions_text,
                                 perk.percentage_value,
                                 perk.minimum_spend,
                                 perk.money_back,
                                 perk.cap_amount,
                                 perk.confidence,
                                 perk_hash
                             ))
                skipped += 1

    return {'inserted': inserted, 'skipped': skipped}


def get_all_perks() -> List[dict]:
    """Retrieve all perks from database."""
    with get_db_connection() as conn:
        cursor = conn.execute("""
                              SELECT *
                              FROM perks
                              ORDER BY created_at DESC
                              """)
        return [dict(row) for row in cursor.fetchall()]