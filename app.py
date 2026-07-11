
import os
import time

def analyze_document():
    print("Initializing Local Document Processor...")
    time.sleep(1) # Simulates a quick loading pause
    
    print("Reading invoice file locally...")
    time.sleep(1)

    # Simulated invoice data instead of calling the cloud
    mock_invoice_documents = [
        {
            "fields": {
                "VendorName": "Xordinary Bakery Supplies",
                "InvoiceTotal": "R 2,450.00"
            }
        }
    ]
    
    print("\n--- Analysis Results ---")
    for invoice in mock_invoice_documents:
        vendor_name = invoice["fields"].get("VendorName")
        if vendor_name:
            print(f"Vendor Name: {vendor_name}")
            
        total = invoice["fields"].get("InvoiceTotal")
        if total:
            print(f"Invoice Total: {total}")
    print("------------------------\n")

if __name__ == "__main__":
    analyze_document()
