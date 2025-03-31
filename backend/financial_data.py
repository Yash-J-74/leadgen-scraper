import asyncio
import io
# from typing import Dict, Optional
from yahooquery import search
from playwright.sync_api import sync_playwright
import pandas as pd
from io import StringIO

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:87.0) Gecko/20100101 Firefox/87.0'
}

urls = {
    'income annually': "https://stockanalysis.com/stocks/{company}/financials/",
    'income quarterly': "https://stockanalysis.com/stocks/{company}/financials/?p=quarterly",
    'balance sheet annually': "https://stockanalysis.com/stocks/{company}/financials/balance-sheet/",
    'balance sheet quarterly': "https://stockanalysis.com/stocks/{company}/financials/balance-sheet/?p=quarterly",
    'cash flow annually': "https://stockanalysis.com/stocks/{company}/financials/cash-flow-statement/",
    'cash flow quarterly': "https://stockanalysis.com/stocks/{company}/financials/cash-flow-statement/?p=quarterly",
    'ratio annually': "https://stockanalysis.com/stocks/{company}/financials/ratios/",
    'ratio quarterly': "https://stockanalysis.com/stocks/{company}/financials/ratios/?p=quarterly"
}

def get_stock_symbol(company_name: str) -> str:
    result = search(company_name, )
    quotes = result.get('quotes', [])
    if quotes:
        return quotes[0].get('symbol', '')
    else:
        print(f"No stock symbol found for '{company_name}'.")
        return ""

def fetch_financial_data(company: str, buffer: io.BytesIO):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        page.set_extra_http_headers(headers)
        
        # Use the in-memory buffer for the Excel writer
        writer = pd.ExcelWriter(buffer, engine='openpyxl')

        for key, url_template in urls.items():
            company_sym = get_stock_symbol(company)
            if not company_sym:
                print(f"Skipping {key} as no stock symbol was found for the company.")
                continue
            
            url = url_template.format(company=company_sym)
            page.goto(url)
            
            # Wait for the table to load
            page.wait_for_selector("#main-table-wrap", state="visible")
            
            # Extract the table's HTML
            tables = page.evaluate("document.querySelector('#main-table').outerHTML")
            df = pd.read_html(StringIO(tables))[0]
            
            # Flatten multi-index columns if present
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = [' '.join(col).strip() for col in df.columns.values]
            
            # Write the DataFrame to the Excel file
            df.to_excel(writer, sheet_name=key, index=False)
        
        # Close the Excel writer
        writer.close()
        browser.close()

# asyncio.run(fetch_financial_data("Nvidia"))