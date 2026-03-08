# Day 18: Adversarial PII Redaction Edge-Case Test Report

## PII Edge-Case Inputs

### Test 1: Phone with country code and spaces

- **Raw Input:** "+1 234 567 8901"
- **Redacted Output:** [To be filled]
- **PII Leak:** [Y/N]

### Test 2: Phone with dots

- **Raw Input:** "234.567.8901"
- **Redacted Output:** [To be filled]
- **PII Leak:** [Y/N]

### Test 3: Email with subdomain

- **Raw Input:** "user@mail.subdomain.com"
- **Redacted Output:** [To be filled]
- **PII Leak:** [Y/N]

### Test 4: Email with plus-tag

- **Raw Input:** "name+tag@domain.com"
- **Redacted Output:** [To be filled]
- **PII Leak:** [Y/N]

### Test 5: Mixed case email

- **Raw Input:** "User.Name@Domain.COM"
- **Redacted Output:** [To be filled]
- **PII Leak:** [Y/N]

---

## Summary

These edge cases test the robustness of PII redaction. Results will inform patching and improvements.
