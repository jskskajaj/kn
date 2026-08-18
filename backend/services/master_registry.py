"""master_registry (FASE L, diperluas FASE T) — JEMBATAN master ↔ `domain_registry`.

MASALAH YANG DITUTUP
====================
Daftar yang bisa **bertambah** (lini produk sekarang; tahapan proses & jenis
sampling pada fase berikutnya) harus hidup sebagai **master** supaya pemilik bisa
menambahnya tanpa programmer. Tetapi `domain_registry.py` tetap dibutuhkan sebagai
**bentuk + nilai benih**: ia dipakai validasi sinkron di banyak tempat dan harus
bisa diimpor tanpa basis data (skrip, gate statik, tes unit).

Kalau keduanya dibiarkan berdiri sendiri, lahirlah dua daftar — kelas bug termahal
di repo ini. Aturan yang dipakai:

    domain_registry  →  BENTUK + NILAI BENIH (seed)          [sinkron, tanpa DB]
    koleksi master   →  NILAI HIDUP (bisa ditambah pemilik)   [asinkron, per PT]
    berkas ini       →  SATU PEMBACA untuk keduanya

Urutan resolusi: baris master **efektif** untuk badan usaha itu (override PT menang
atas baris global) → bila koleksinya **kosong**, pakai nilai benih. Fallback itu
bukan kemewahan: instalasi baru & basis data uji tidak boleh mati hanya karena
migrasi seed belum dijalankan.

Cache 60 detik per (kind, badan usaha) supaya `/api/enums` dan penyaring 12 layar
tidak memukul Mongo tiap ketukan. `invalidate()` dipanggil `routers/entity_masters.py`
sesudah master diubah — pola yang sama dengan `core_utils.invalidate_entity_code`
(pelajaran FASE E-1: tanpa itu perubahan master baru terasa setelah backend restart).
"""
import time
from typing import Any, Dict, List, Optional

import domain_registry as dr

CACHE_TTL_SECONDS = 60
_cache: Dict[str, Dict[str, Any]] = {}       # key -> {"at": ts, "rows": [...]}

# kind master (URL slug) → nama enum benih di domain_registry
SEEDS: Dict[str, str] = {
    "product-lines": "product_line",
    # FASE T akan menambah: "process-stages": "process_stage", dst.
}


def invalidate(kind: str = "") -> None:
    """Buang cache. Tanpa argumen = seluruh cache."""
    if not kind:
        _cache.clear()
        return
    for key in [k for k in _cache if k.startswith(f"{kind}:")]:
        _cache.pop(key, None)


def _seed_rows(kind: str) -> List[Dict[str, Any]]:
    enum_name = SEEDS.get(kind, "")
    if not enum_name:
        return []
    return [dict(v) for v in dr.enum_items(enum_name)]


def _row_to_item(row: Dict[str, Any], key_field: str, name_field: str) -> Dict[str, Any]:
    """Baris master → bentuk item enum (`value`/`label`) + seluruh field lainnya.

    Bentuknya disamakan dengan `domain_registry` supaya layar & `useDomainEnums`
    tidak perlu tahu nilainya datang dari master atau dari benih.
    """
    out = {k: v for k, v in row.items() if k not in ("_id",)}
    out["value"] = str(row.get(key_field) or "").strip().lower()
    out["label"] = str(row.get(name_field) or out["value"] or "")
    return out


async def rows(kind: str, entity_id: str = "") -> List[Dict[str, Any]]:
    """Nilai HIDUP master `kind` untuk satu badan usaha (dengan fallback benih)."""
    key = f"{kind}:{entity_id or 'all'}"
    hit = _cache.get(key)
    now = time.time()
    if hit and (now - hit["at"]) < CACHE_TTL_SECONDS:
        return hit["rows"]
    from services import entity_master_service as ems
    try:
        spec = ems.spec(kind)
        live = await ems.effective_rows(kind, entity_id or "")
        items = [_row_to_item(r, spec.key_field, spec.name_field) for r in live]
        items = [i for i in items if i["value"]]
    except Exception:                      # noqa: BLE001 — master belum terdaftar/DB mati
        items = []
    if not items:
        items = _seed_rows(kind)
    _cache[key] = {"at": now, "rows": items}
    return items


# ─── FASE L — LINI PRODUK ────────────────────────────────────────────────────
async def product_lines(entity_id: str = "") -> List[Dict[str, Any]]:
    return await rows("product-lines", entity_id)


async def line_codes(entity_id: str = "") -> List[str]:
    return [r["value"] for r in await product_lines(entity_id)]


async def line_meta(code: str, entity_id: str = "") -> Dict[str, Any]:
    want = str(code or "").strip().lower()
    for r in await product_lines(entity_id):
        if r["value"] == want:
            return r
    return {}


async def line_options(entity_id: str = "") -> List[Dict[str, Any]]:
    """Bentuk siap-dropdown untuk `/api/enums` & komponen `<LineFilter/>`."""
    out = []
    for r in await product_lines(entity_id):
        out.append({
            "value": r["value"], "label": r["label"],
            "fabric_type_required": r.get("fabric_type_required", "") or "",
            "measure_unit_default": r.get("measure_unit_default", "") or "",
            "stage_sequence": r.get("stage_sequence") or [],
            "sample_types_default": r.get("sample_types_default") or [],
            "description": r.get("description", "") or r.get("notes", "") or "",
            "sort": r.get("sort", 0) or 0,
        })
    return out


async def live_enum_values(name: str, entity_id: str = "") -> Optional[List[Dict[str, Any]]]:
    """Nilai hidup untuk sebuah enum `domain_registry`, bila enum itu ber-master.

    Dipakai `routers/enums.py` untuk menimpa nilai benih **hanya** pada enum yang
    memang punya master — enum lain tetap apa adanya.
    """
    for kind, enum_name in SEEDS.items():
        if enum_name == name:
            return await rows(kind, entity_id)
    return None
