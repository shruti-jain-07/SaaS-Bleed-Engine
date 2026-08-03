# Data Validation & Cleaning Rules

1. **File Format Enforcement:** Only `.csv` for transactions and `.pdf` for contracts.
2. **Schema Verification:** Ensures required columns exist (`transaction_id`, `date`, `vendor_name`, `amount`, `department_id`, `card_last_four`).
3. **Deduplication:** Drops duplicate `transaction_id` rows within the upload stream and ignores records already saved in the database.
4. **Data Normalization:** Capitalizes vendor names (Title Case) and reformats `card_last_four` to 4 digits.
5. **Amount Filter:** Rejects zero or negative amounts.