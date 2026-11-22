-- SQLite: sample data profiling checks.

-- Record count and missing identifiers/countries by segment.
SELECT segment,
       COUNT(*) AS total_records,
       SUM(CASE WHEN customer_id IS NULL OR TRIM(customer_id) = '' THEN 1 ELSE 0 END) AS missing_ids,
       SUM(CASE WHEN country IS NULL OR TRIM(country) = '' THEN 1 ELSE 0 END) AS missing_countries
FROM customers
GROUP BY segment
ORDER BY segment;

-- Duplicate nonblank customer identifiers.
SELECT customer_id, COUNT(*) AS occurrences
FROM customers
WHERE customer_id IS NOT NULL AND TRIM(customer_id) <> ''
GROUP BY customer_id
HAVING COUNT(*) > 1
ORDER BY occurrences DESC, customer_id;

-- Monthly onboarding volume (counts records, not distinct customers).
SELECT SUBSTR(onboarding_date, 1, 7) AS onboarding_month,
       COUNT(*) AS records
FROM customers
GROUP BY SUBSTR(onboarding_date, 1, 7)
ORDER BY onboarding_month;
