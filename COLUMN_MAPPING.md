# Quick Reference: Column Mapping

## Old → New Column Mapping

### Main Fields
- `Is_laundering` → `is_fraud`
- `Date` → `transaction_date`
- `Time` → `transaction_time`
- `Amount` → `transaction_amount`
- `Sender_account` → `customer_id` (primary identifier)
- `Receiver_account` → `merchant_id`

### Location Fields
- `Sender_bank_location` → `billing_country`
- `Receiver_bank_location` → `shipping_country` + `location`
- (New) → `ip_country`

### Payment Fields
- `Payment_currency` → `transaction_currency`
- `Received_currency` → `billing_currency`
- `Payment_type` → `transaction_type`
- (New) → `payment_method`, `card_type`, `card_present`, `cvv_match`

### New Fields Not in Old Dataset
- Device & Session: device_type, ip_address, session_id, session_duration_seconds
- Customer Info: customer_age, account_age_days, num_page_views
- Transaction Patterns: previous_transactions_24h/7d/30d, same_merchant_last_30d, num_unique_merchants_30d
- Risk Indicators: failed_login_attempts, velocity_score, num_locations_7d
- Distance: distance_from_home_km, distance_from_last_transaction_km, time_since_last_transaction_minutes
- Verification: email_verified, phone_verified, shipping_address_verified
- Merchant: merchant_category, merchant_reputation, merchant_id
- Flags: is_weekend, is_holiday, currency_mismatch

## Code Changes Checklist

### When Loading CSV Data
- ✅ Must have all 47 columns
- ✅ Column names must match exactly (case-sensitive)
- ✅ is_fraud: binary (0 or 1)
- ✅ transaction_date: YYYY-MM-DD format
- ✅ transaction_time: HH:MM:SS format
- ✅ All numeric fields must be numeric type
- ✅ All categorical fields must be string type

### When Making Predictions
Old code:
```python
transaction = {
    'Time': time,
    'Date': str(date),
    'Sender_account': sender_account,
    'Receiver_account': receiver_account,
    'Amount': amount,
    'Payment_currency': payment_currency,
    ...
}
```

New code:
```python
transaction = {
    'transaction_time': transaction_time,
    'transaction_date': str(transaction_date),
    'customer_id': customer_id,
    'merchant_id': merchant_id,
    'transaction_amount': transaction_amount,
    'transaction_currency': transaction_currency,
    ...
}
```

### Feature Engineering Updates
Old engineered features:
- hour, is_weekend, is_night_transaction
- log_amount, is_round_amount, is_structuring_amount
- is_cross_border, is_currency_mismatch
- sender_frequency, receiver_frequency

New engineered features (includes above + new):
- is_high_velocity (velocity_score > 70)
- has_failed_logins (failed_login_attempts > 0)
- unverified_email, unverified_phone, unverified_address
- verification_gap (sum of unverified flags)

## Profile Structure Changes

### Old Profile
```python
{
    'account': 'ACC0001',
    'total_transactions': 100,
    'sent_transactions': 50,
    'received_transactions': 50,
    'total_volume': 500000,
    'sent_volume': 250000,
    'received_volume': 250000,
    'suspicious_transactions': 10,
    'unique_counterparties': 15,
    ...
}
```

### New Profile
```python
{
    'customer_id': 'CUST00001',
    'total_transactions': 100,
    'total_volume': 500000,
    'fraudulent_transactions': 5,
    'cross_border_count': 15,
    'unverified_transactions': 20,
    'customer_age': 35,
    'account_age_days': 730,
    'unique_merchants': 25,
    ...
}
```

## Database/API Updates (if applicable)

If using a database or external API, update:

1. **SELECT statements** - Use new column names
2. **INSERT statements** - Match 47-column structure
3. **WHERE clauses** - Use `is_fraud` not `Is_laundering`
4. **JOINs** - Use `customer_id` as primary key
5. **Aggregations** - Use `transaction_amount` not `Amount`
6. **Filters** - Update date filters to use `transaction_date`

## Testing Checklist

Before running with actual data:
- [ ] CSV file has exactly 47 columns
- [ ] Column names match exactly (see column list above)
- [ ] is_fraud column contains only 0 or 1
- [ ] transaction_date is YYYY-MM-DD format
- [ ] transaction_time is HH:MM:SS format
- [ ] No NULL values in required fields
- [ ] Data types are correct (numeric vs string)
- [ ] Date ranges are reasonable (2023-2024 for recent data)
- [ ] Run synthetic data first to verify system works
- [ ] Check model metrics after training on actual data

## Troubleshooting

**Error: KeyError for column names**
→ Check CSV has all 47 columns with exact names

**Error: is_fraud not found**
→ File still has Is_laundering, rename it

**Error: datetime parsing**
→ Verify date format is YYYY-MM-DD, time is HH:MM:SS

**Poor model performance**
→ May need to retrain, old model incompatible with new features

**Missing customer profiles**
→ Check customer_id column exists and has unique values
