# IncidentAI — Sample App Specification (the testbed)

> Minimal 3-service e-commerce order flow + PostgreSQL + simulated payment.
> Deliberately tiny: it exists to produce faults and to be repairable, not to be a real store.

## Services & ports

| Service | Port | Role |
|---------|-----:|------|
| gateway | 8000 | API entry / BFF; routes to orders & inventory |
| orders | 8001 | Orchestrates order creation |
| inventory | 8002 | Product catalog + stock |
| payment-stub | 8003 | Simulated external payment provider |
| postgres | 5432 | `orders_db`, `inventory_db` |

## Endpoints

**Gateway (8000)**
- `GET /health`
- `GET /api/products`
- `POST /api/orders` → `{sku, qty}`
- `GET /api/orders/{id}`

**Inventory (8002)**
- `GET /health`
- `GET /products`
- `GET /products/{sku}`
- `POST /inventory/reserve` → `{sku, qty}` → `200 {reserved:true}` or `409`

**Orders (8001)**
- `GET /health`
- `POST /orders` → `{sku, qty}`
- `GET /orders/{id}`

**Payment stub (8003)**
- `GET /health`
- `POST /charge` → `{amount_cents, ref}` → `{status:"charged", txn_id}` or `500`

## Data model (keep minimal)

**inventory_db.products**
`sku (PK), name, price_cents, stock`

**orders_db.orders**
`id (UUID), sku, qty, status, payment_ref, created_at`

## Happy path

1. Client → gateway `POST /api/orders`.
2. Gateway → orders `POST /orders`.
3. Orders validates payload.
4. Orders → inventory `POST /inventory/reserve` (decrements stock).
5. If reserved: orders → payment `POST /charge`.
6. Payment returns `charged`.
7. Orders writes the order row, returns `201`.
8. Gateway returns `201` to the client.

## Fault hooks (deterministic)

- **Startup env flags:** `FAULT_<SERVICE>_<NAME>` (e.g., `FAULT_INV_DB_LEAK=true`).
- **Runtime toggle:** `POST /_fault {name, value}` per service, enabled only in the testbed.
- Examples: `FAULT_INV_DB_POOL_MAX`, `FAULT_INV_DB_LEAK`, `FAULT_ORD_DB_SLOW_MS`, `FAULT_PAYMENT_LATENCY_MS`, `FAULT_PAYMENT_FAIL`, `FAULT_GW_BUSY_LOOP`.

## Telemetry expectations

- OTel auto-instrumentation for HTTP + DB + outbound HTTP.
- Custom spans: `inventory.reserve`, `orders.payment.charge`.
- Metrics: request duration histogram, error counter, DB pool gauges (custom).
- Structured JSON logs with `trace_id` and `service`.

## Non-goals

- No auth in the demo app (Keycloak belongs to the platform).
- No fancy UI (curl/scripts are enough; the React app is the platform's).
- Keep the domain tiny — every line exists to produce or repair faults.
