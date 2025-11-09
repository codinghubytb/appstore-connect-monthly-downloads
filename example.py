from src.appstore_get_data import fetch_monthly_downloads, AppStoreConnect
import json

# Fill with your real paths
KEY_ID="xxxxxxxx"
ISSUER_ID="xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
PATH_TO_KEY=r"path\to\your\private_key.p8"
VENDOR_NUMBER="xxxxxxxx",
APP_SKU="xxxxxxxx"

if __name__ == "__main__":
    client = AppStoreConnect(KEY_ID, ISSUER_ID, PATH_TO_KEY)
    
    # Fetch monthly data
    monthly_data = fetch_monthly_downloads(
        client,
        VENDOR_NUMBER,
        app_sku=APP_SKU,
        months_back=12
    )
    
    # Output as JSON array
    print(json.dumps(monthly_data, indent=2))