import streamlit as st
import glob
import os
from replace_logo import replace_logo

st.set_page_config(page_title="PDF Brand Updater", layout="centered")

st.title("📄 PDF Brand Updater")
st.markdown("Upload your 'Morning Coffee' PDF to automatically replace the logo and update the details.")

# File uploader
uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])

# Logo selection (optional, but good to have)
# We can look for the default logo in the current directory
logo_files = glob.glob("*.png")
default_logo = logo_files[0] if logo_files else None

if uploaded_file is not None:
    st.success("PDF uploaded successfully!")
    
    if default_logo:
        st.info(f"Using default logo: {os.path.basename(default_logo)}")
        
        if st.button("Process PDF"):
            with st.spinner("Processing..."):
                try:
                    # Pass the uploaded file object (stream) directly
                    # and the logo path
                    output_bytes = replace_logo(
                        pdf_input=uploaded_file, 
                        logo_path=default_logo, 
                        position="right",
                        output_path=None # We want bytes back
                    )
                    
                    st.success("Processing complete!")
                    
                    # Generate new filename: Replace "Prudent" with "Prosecure"
                    original_name = uploaded_file.name
                    new_name = original_name.replace("Prudent", "Prosecure")
                    # Fallback if "Prudent" wasn't in the name, just prepend "Prosecure_"
                    if new_name == original_name:
                         new_name = f"Prosecure_{original_name}"

                    # Download button
                    st.download_button(
                        label="Download Updated PDF",
                        data=output_bytes,
                        file_name=new_name,
                        mime="application/pdf"
                    )
                except Exception as e:
                    st.error(f"An error occurred: {e}")
    else:
        st.error("No logo file found in the server directory. Please contact support.")
