# Copilot Instructions for MeroShare

## Project Overview

MeroShare is a Python automation tool for applying to IPOs/FPOs and Right Shares on Nepal's MeroShare platform (CDSC). It reads account credentials from a CSV file and automates the share application process via the MeroShare web API.

## Architecture

- **Single-file design**: All logic resides in [main.py](../main.py) with a `MeroShare` class
- **CSV-driven multi-account support**: Reads credentials from `Acnt.csv` (one row per account)
- **Session-based API interaction**: Uses `requests.Session()` for API calls to `webbackend.cdsc.com.np`

### Data Flow
1. Parse `Acnt.csv` → instantiate `MeroShare` per account
2. If `BankId=0` → run `first_time_setup()` (user selects bank, updates CSV manually)
3. If `BankId≠0` → run `apply_shares()` (auto-applies to all eligible Ordinary Shares)

## Key API Endpoints Pattern

All endpoints use base URL `https://webbackend.cdsc.com.np/api/meroShare/`:
- `capital/` - Get DP (Depository Participant) list
- `auth/` - Login, returns `Authorization` header
- `ownDetail/` - Get BOID and demat info
- `bank/` - List/get bank details
- `companyShare/applicableIssue/` - Get available IPOs/FPOs
- `applicantForm/share/apply` - Submit application

## CSV Format (`Acnt.csv`)

```csv
DP,Password,Username,Apply Kitta,CRN,Transaction PIN,BankId
1023600,password,username,10,crnumber,1234,0
```

- `BankId=0` triggers first-time setup flow
- After setup, user must manually update `BankId` in CSV

## Development Commands

```powershell
# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# Run the application
python main.py
```

## Code Conventions

- **No external dependencies** beyond `requests` - keep it minimal
- **Print-based UI**: Uses print statements for user feedback (ASCII art boxes for status)
- **Authorization flow**: Token from login response header, passed to subsequent requests
- **Right Share handling**: Different payload with `shareCriteriaId` for rights issues

## When Modifying

- Preserve the dual-mode logic (`first_time_setup` vs `apply_shares` based on `BankId`)
- Keep credential handling in CSV (no hardcoded secrets)
- The API mimics browser headers - maintain these if adding new endpoints
- Share types filter: Currently only applies to `"Ordinary Shares"` shareGroupName
