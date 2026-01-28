# Day 15 PII Redaction Test Report

## Test 1

**Raw input:**
Contact me at alice@example.com or (555) 123-4567.
**Redacted output:**
Contact me at [REDACTED_PII] or [REDACTED_PII].
**PII leaked?** N

---

## Test 2

**Raw input:**
My number is 555-123-4567 and my backup is 5551234567.
**Redacted output:**
My number is [REDACTED_PII] and my backup is [REDACTED_PII].
**PII leaked?** N

---

## Test 3

**Raw input:**
Send details to bob.smith@work-mail.com or call +1 555 123 4567.
**Redacted output:**
Send details to [REDACTED_PII] or call [REDACTED_PII].
**PII leaked?** N

---

All tested PII formats (emails and various phone numbers) were successfully redacted and replaced with [REDACTED_PII]. No PII leaked in the redacted outputs.
