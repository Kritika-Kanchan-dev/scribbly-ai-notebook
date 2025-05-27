import os
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

def process_file(uploaded_file):
    """
    Process uploaded file and extract text content
    """
    try:
        # Get file extension
        file_name = uploaded_file.name
        file_extension = os.path.splitext(file_name)[1].lower()
        
        # Read file content
        file_content = uploaded_file.read()
        
        # Basic text extraction based on file type
        if file_extension == '.txt':
            # Plain text file
            text_content = file_content.decode('utf-8')
            
        elif file_extension in ['.pdf']:
            # For PDF files, you'll need to install PyPDF2 or similar
            # pip install PyPDF2
            try:
                import PyPDF2
                import io
                
                pdf_reader = PyPDF2.PdfReader(io.BytesIO(file_content))
                text_content = ""
                for page in pdf_reader.pages:
                    text_content += page.extract_text()
                    
            except ImportError:
                return "PDF processing requires PyPDF2. Please install it: pip install PyPDF2"
                
        elif file_extension in ['.docx']:
            # For DOCX files, you'll need to install python-docx
            # pip install python-docx
            try:
                import docx
                import io
                
                doc = docx.Document(io.BytesIO(file_content))
                text_content = ""
                for paragraph in doc.paragraphs:
                    text_content += paragraph.text + "\n"
                    
            except ImportError:
                return "DOCX processing requires python-docx. Please install it: pip install python-docx"
                
        else:
            # Try to decode as text for other file types
            try:
                text_content = file_content.decode('utf-8')
            except UnicodeDecodeError:
                return f"Unsupported file type: {file_extension}"
        
        return text_content.strip()
        
    except Exception as e:
        return f"Error processing file: {str(e)}"