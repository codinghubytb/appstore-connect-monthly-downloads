import requests
import time
import gzip
from datetime import datetime, timedelta
from io import StringIO
from authlib.jose import jwt
import pandas as pd


class AppStoreConnect:
    """App Store Connect API client"""
    
    def __init__(self, key_id, issuer_id, private_key_path):
        self.key_id = key_id
        self.issuer_id = issuer_id
        with open(private_key_path, 'r') as f:
            self.private_key = f.read()
        self.base_url = "https://api.appstoreconnect.apple.com/v1"
    
    def _generate_token(self):
        """Generate JWT token for API authentication"""
        expiration_time = int(round(time.time() + (19.0 * 60.0)))
        
        header = {
            "alg": "ES256",
            "kid": self.key_id,
            "typ": "JWT"
        }
        
        payload = {
            "iss": self.issuer_id,
            "exp": expiration_time,
            "aud": "appstoreconnect-v1"
        }
        
        token = jwt.encode(header, payload, self.private_key)
        return token.decode()
    
    def _make_request(self, method, endpoint, params=None):
        """Make authenticated API request"""
        token = self._generate_token()
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        url = f"{self.base_url}/{endpoint}"
        response = requests.request(method, url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    
    def get_sales_report(self, vendor_number, report_date, frequency="MONTHLY"):
        """
        Fetch sales report data
        
        Args:
            vendor_number: Vendor number from App Store Connect
            report_date: Date in YYYY-MM format
            frequency: Report frequency (MONTHLY, DAILY, WEEKLY, YEARLY)
        
        Returns:
            pandas.DataFrame: Sales data
        """
        params = {
            "filter[frequency]": frequency,
            "filter[reportDate]": report_date,
            "filter[reportSubType]": "SUMMARY",
            "filter[reportType]": "SALES",
            "filter[vendorNumber]": vendor_number
        }
        
        token = self._generate_token()
        headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/a-gzip"
        }
        
        url = f"{self.base_url}/salesReports"
        response = requests.get(url, headers=headers, params=params)
        
        if response.status_code == 200:
            decompressed = gzip.decompress(response.content)
            df = pd.read_csv(StringIO(decompressed.decode('utf-8')), sep='\t')
            return df
        
        return None


def fetch_monthly_downloads(api_client, vendor_number, app_sku=None, months_back=12):
    """
    Fetch monthly download statistics
    
    Args:
        api_client: AppStoreConnect instance
        vendor_number: Vendor number
        app_sku: App SKU (optional, filters to specific app)
        months_back: Number of months to fetch
    
    Returns:
        list: Monthly download data as list of dicts
    """
    results = []
    
    for i in range(months_back):
        date = datetime.now() - timedelta(days=30 * (i + 1))
        report_date = date.strftime("%Y-%m")
        month_name = date.strftime("%b %Y")
        
        try:
            df = api_client.get_sales_report(vendor_number, report_date, "MONTHLY")
            
            if df is not None and not df.empty:
                # Filter by SKU if provided
                if app_sku and 'SKU' in df.columns:
                    df = df[df['SKU'] == app_sku]
                    if df.empty:
                        continue
                
                # Calculate metrics
                total_units = int(df['Units'].sum()) if 'Units' in df.columns else 0
                
                # Separate downloads (Product Type 1) vs updates (Product Type 7)
                downloads = 0
                if 'Product Type Identifier' in df.columns and 'Units' in df.columns:
                    downloads = int(df[df['Product Type Identifier'] == '1']['Units'].sum())
                
                if downloads == 0:
                    downloads = total_units
                
                if downloads > 0:
                    results.append({
                        "month": month_name,
                        "activeUsers": downloads
                    })
        
        except:
            continue
    
    # Sort chronologically
    results.sort(key=lambda x: datetime.strptime(x["month"], "%b %Y"))
    return results