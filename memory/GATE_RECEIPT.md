# 🧾 GATE RECEIPT — Kain Nusantara

> Bukti verifikasi otomatis. Dihasilkan `scripts/gate.sh`. JANGAN edit manual.

- **Waktu:** 2026-08-18 19:19:31
- **Mode:** `quick`  ·  **Durasi total:** 11s  ·  **Pekerja statik:** 2
- **Backend:** DOWN / tidak diperiksa (mode quick atau Phase 0)

| Gate | Hasil |
|------|-------|
| guard:auth_coverage (INV-AUTH-01) | PASS (1s) |
| guard:auth_coverage SELF-TEST (bukti-merah penjaga auth) | PASS (0s) |
| validate_compliance (file/naming/docs/api/env) | PASS (1s) |
| check_nav_map (navigasi vs SSOT) | PASS (0s) |
| guard:modal_dismiss (INV-UI-01, modal auto-close) | PASS (0s) |
| guard:create_modal SELF-TEST (bukti-merah penjaga create pop-up) | PASS (0s) |
| guard:create_modal (INV-UI-05, tombol Buat = pop-up konsisten) | PASS (0s) |
| guard:blocking_dialogs SELF-TEST (bukti-merah + anti tuduh palsu) | PASS (1s) |
| guard:blocking_dialogs (INV-UI-06, alert/confirm/prompt dilarang) | PASS (1s) |
| guard:list_export SELF-TEST (bukti-merah + CSV rusak harus memerah) | PASS (0s) |
| guard:list_export (INV-UI-07, daftar berhalaman wajib bisa diunduh) | PASS (1s) |
| guard:detail_modal SELF-TEST (bukti-merah + anti tuduh palsu) | PASS (0s) |
| guard:detail_modal (INV-UI-08, panel rincian wajib pop-up) | PASS (1s) |
| ux_audit SELF-TEST (bukti-merah baseline UX + anti tuduh palsu) | PASS (0s) |
| ux_audit --strict (INV-UX-01, loading/empty/chart baseline) | PASS (1s) |
| config_wiring (INV-CFG-01/04, satu sumber kebenaran) | PASS (0s) |
| config_wiring SELF-TEST (bukti-merah guardrail) | PASS (7s) |
| audit_doc_refs SELF-TEST (bukti-merah relasi dokumen) | PASS (0s) |
| audit_i18n_id (label antarmuka Bahasa Indonesia) | PASS (1s) |
| audit_i18n_id SELF-TEST (bukti-merah guardrail bahasa) | PASS (0s) |
| fix_i18n_id SELF-TEST (codemod tak boleh sentuh kode) | PASS (0s) |
| guard:entity_label (INV-UI-02, id entitas tak boleh tampil) | PASS (1s) |
| guard:error_notice (INV-UI-03, error tak boleh senyap) | PASS (0s) |
| guard:role_label (INV-ROLE-01, peran dari registry & izin) | PASS (0s) |
| guard:derived_fields (INV-UI-04, field turunan tak boleh dari respons daftar) | PASS (0s) |
| audit_entity_isolation SELF-TEST (bukti-merah pagar isolasi) | PASS (0s) |
| guard:write_scope SELF-TEST (INV-ENTITY-02, mode gabungan hanya-lihat) | PASS (0s) |
| guard:warehouse_scope SELF-TEST (E4.1, gudang khusus badan usaha) | PASS (0s) |
| guard:numeric_bounds (INV-NUM-01, statik+runtime) | PASS (1s) |
| seed_realistic | SKIP |
| verify_data_integrity | SKIP |
| gate runtime (IDOR/race/state/sweep/health) | SKIP |
| INV-GATE-01 anti-residu | SKIP |

## ✅ VERDICT: HIJAU — boleh lanjut / klaim selesai (cakupan non-skip).

**Tingkatan:** `--quick` (statik ~7s) · default (~25s) · `--ci` (default + receipt JSON) · `--full` (+POC fase ~95s).

_Catatan: SKIP bukan PASS. Gate runtime harus dijalankan ulang saat backend hidup._
