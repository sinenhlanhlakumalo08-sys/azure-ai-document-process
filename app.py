import streamlit as st
from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentAnalysisClient

# Set up page layout
st.set_page_config(page_title="Azure Document Processor", page_icon="📄")
st.title("📄 Azure AI Document Intelligence")
st.write("Upload an invoice or document to extract key information using Azure AI.")

# Securely grab credentials from Streamlit secrets
try:
    ENDPOINT = st.secrets["AZURE_DOCUMENT_ENDPOINT"]
    KEY = st.secrets["AZURE_DOCUMENT_KEY"]
    # Initialize Azure Document Analysis Client
    client = DocumentAnalysisClient(endpoint=ENDPOINT, credential=AzureKeyCredential(KEY))
except Exception as e:
    st.error("Missing Azure configuration secrets! Please add them to Advanced Settings.")
    st.stop()

# Frontend File Uploader component
uploaded_file = st.file_uploader("Choose a document...", type=["pdf", "jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Read file bytes
    file_bytes = uploaded_file.read()
    
    with st.spinner("Analyzing document with Azure AI..."):
        try:
            # Use Azure's prebuilt invoice model to process the uploaded file bytes
            poller = client.begin_analyze_document("prebuilt-invoice", file_bytes)
            result = poller.result()
            
            st.success("Analysis complete!")
            st.subheader("📋 Extracted Key-Value Fields")
            
            # Loop over processed documents and pull out common invoice fields
            for invoice in result.documents:
                vendor_name = invoice.fields.get("VendorName")
                if vendor_name:
                    st.write(f"**Vendor Name:** {vendor_name.value} *(Confidence: {vendor_name.confidence:.2f})*")
                    
                invoice_date = invoice.fields.get("InvoiceDate")
                if invoice_date:
                    st.write(f"**Invoice Date:** {invoice_date.value}")
                    
                invoice_total = invoice.fields.get("InvoiceTotal")
                if invoice_total:
                    st.write(f"**Total Amount Due:** {invoice_total.value}")
                
                st.write("---")
                
            # Fallback to display raw text paragraphs found if fields aren't caught cleanly
            if not result.documents:
                st.info("No specific invoice layout fields detected. Here is the raw extracted text:")
                for page in result.pages:
                    for line in page.lines:
                        st.write(line.content)
                        
        except Exception as err:
            st.error(f"An error occurred during Azure processing: {err}")

