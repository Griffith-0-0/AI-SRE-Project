# IncidentAI — Fault Catalog

> The labeled fault set that feeds Phase 1 (detection) and the benchmark (Phase 6).
> Each fault has a **deterministic injection**, a **known true root cause**, and a **known-good fix**.

## The hero incident

**INC-HERO-001 — Inventory DB connection-pool exhaustion.**

Why this is the hero (and the MVP demo target):

- **Real propagation** — an inventory fault cascades to orders and finally to the gateway, so RCA has a real chain to reason about.
- **Rich signals** — pool metrics, latency histograms, timeout logs, cross-service traces.
- **Unambiguous ground truth** — one clear root cause, one clear fix.
- **Deterministic** — a single flag produces the failure reliably.
- **Repairable (L1)** — the fix is a small, single-file code change (connection leak → `try/finally`), ideal for the repair benchmark.

### Injection

- Startup flags on the inventory service: `FAULT_INV_DB_POOL_MAX=2`, `FAULT_INV_DB_LEAK=true`.
- Each request to `/inventory/reserve` leaks one connection (never returned).
- After a few requests the pool is saturated; new requests block, then time out.

### Symptom timeline

| Time | What happens |
|------|--------------|
| t0 | Normal order traffic. |
| t1 | Inventory pool `active` climbs to `max`. |
| t2 | Inventory requests block on pool acquire → latency rises. |
| t3 | Orders' call to inventory hits its timeout → orders returns 504/500. |
| t4 | Gateway returns 5xx to clients; error rate spikes. |

### Signals

- **Metrics:** `inventory_db_pool_active` = max; `inventory_db_pool_wait_seconds` high; p99 latency ↑ on inventory → orders → gateway; error rate ↑.
- **Traces:** slow inventory span waiting on DB; orders span shows upstream timeout; gateway span slow.
- **Logs:** inventory `pool timeout`; orders `inventory call timeout`; gateway `upstream timeout`.

### Ground truth

- **True root cause:** inventory DB connection-pool exhaustion (connection leak).
- **Known-good fix:** return connections reliably (`try/finally`), raise pool max, add a statement timeout.

### Determinism contract

Reset DB + restart inventory + clear the fault flag before every run; drive requests with a fixed script. Require **3 clean runs** before this incident enters the corpus.

---

## Fault catalog

| ID | Fault | Target | Injection | Root cause (ground truth) | Difficulty |
|----|-------|--------|-----------|---------------------------|:---:|
| **F1** | DB pool exhaustion | inventory | `FAULT_INV_DB_POOL_MAX=2` + `FAULT_INV_DB_LEAK=true` | Connection leak exhausts pool | Medium |
| **F2** | Slow DB query | orders | `FAULT_ORD_DB_SLOW_MS=2000` | Unindexed/slow order query | Easy–Med |
| **F3** | Payment latency | payment stub | `FAULT_PAYMENT_LATENCY_MS=5000` | Slow external dependency | Easy |
| **F4** | Payment errors | payment stub | `FAULT_PAYMENT_FAIL=1` | Dependency failing 100% | Easy |
| **F5** | CPU exhaustion | gateway | busy-loop endpoint / `stress-ng` | CPU saturation | Easy |
| **F6** | Service crash | orders | kill process / pod | Orders process down | Easy |
| **F7** | Bad deploy (timeout too low) | orders | env `INVENTORY_TIMEOUT_MS=50` | Misconfigured timeout | Medium |
| **F8** | Network partition | orders↔inventory | Chaos Mesh partition | Network link severed | Hard |

### Difficulty tiers (for the benchmark)

- **Easy** — single-service symptom, obvious signal (F3, F4, F5, F6).
- **Medium** — cross-service propagation, needs correlation (F1, F2, F7).
- **Hard** — infra-level or ambiguous, needs topology reasoning (F8).

## Ground truth format

Every injected run records:

```json
{
  "fault_id": "F1",
  "service": "inventory",
  "injection": "FAULT_INV_DB_POOL_MAX=2;FAULT_INV_DB_LEAK=true",
  "started_at": "...",
  "duration_s": 300,
  "true_root_cause": "inventory DB connection-pool exhaustion (connection leak)",
  "known_good_fix": "return connections in finally; raise pool max; statement timeout"
}
```

## Rules

1. **Isolated environments only** — no production or external side effects.
2. **Deterministic** — seedable, time-boxed, repeatable; 3 clean runs before acceptance.
3. **One root cause per fault** — keep the label unambiguous; multi-root incidents go to the "hard" tier later.
4. **Hold-out** — once a fault enters the hidden hold-out split, never edit it.
