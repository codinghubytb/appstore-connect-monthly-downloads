# App Store Connect Monthly Downloads

Fetch monthly download statistics from App Store Connect API.

## Requirements

- Python 3.7+
- App Store Connect API credentials

## Installation

```bash
pip install -r requirements.txt
```

## Configuration

1. Generate API credentials in [App Store Connect](https://appstoreconnect.apple.com/access/api)
2. Download your private key (.p8 file)
3. Configure the following in the main script:
   - `KEY_ID`: Your API Key ID
   - `ISSUER_ID`: Your Issuer ID
   - `PATH_TO_KEY`: Path to your .p8 private key file
   - `VENDOR_NUMBER`: Your vendor number
   - `APP_SKU`: Your app's SKU

## Usage

```python
python example.py
```

Returns JSON array with monthly download data:
```json
[
  {
    "month": "Jan 2024",
    "activeUsers": 1234
  }
]
```

## Features

- Fetches last 12 months of download data
- Filters by specific app SKU
- Separates new downloads from updates
- Returns data in chronological order
