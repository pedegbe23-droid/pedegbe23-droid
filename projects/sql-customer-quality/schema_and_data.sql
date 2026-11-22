-- Synthetic examples for SQLite; no real customer information.
DROP TABLE IF EXISTS customers;
CREATE TABLE customers (
  record_id INTEGER PRIMARY KEY,
  customer_id TEXT,
  segment TEXT NOT NULL,
  country TEXT,
  onboarding_date TEXT
);
INSERT INTO customers (record_id, customer_id, segment, country, onboarding_date) VALUES
(1, 'C001', 'Retail', 'US', '2026-01-15'),
(2, 'C002', 'Corporate', 'GB', '2026-02-01'),
(3, 'C002', 'Corporate', 'GB', '2026-02-01'),
(4, 'C004', 'Retail', NULL, '2026-03-12'),
(5, NULL, 'Retail', 'CA', '2026-03-22'),
(6, 'C006', 'Corporate', 'US', '2026-04-03');
