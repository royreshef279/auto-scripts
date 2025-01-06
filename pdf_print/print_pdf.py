import PyPDF2

def parse_page_ranges(page_ranges, max_pages):
    """
    Parse the page range string into a list of page numbers.
    
    Args:
        page_ranges (str): A string representing page ranges (e.g., "1,3-4,6-8,10").
        max_pages (int): The maximum number of pages in the PDF.
    
    Returns:
        list of int: A list of valid page numbers.
    """
    pages = set()
    try:
        ranges = page_ranges.split(",")
        for r in ranges:
            if "-" in r:
                start, end = map(int, r.split("-"))
                if start > end or start < 1 or end > max_pages:
                    raise ValueError(f"Invalid range: {r}")
                pages.update(range(start, end + 1))
            else:
                page = int(r)
                if page < 1 or page > max_pages:
                    raise ValueError(f"Invalid page: {page}")
                pages.add(page)
    except ValueError as e:
        print(e)
        return None
    return sorted(pages)

def extract_pages_to_pdf(pdf_paths, page_ranges, output_path="output.pdf"):
    """
    Extracts specified pages from given PDF files and saves them as a single PDF.
    
    Args:
        pdf_paths (list of str): Paths to the input PDF files.
        page_ranges (list of str): Page ranges to extract from each PDF.
        output_path (str): Path to the output PDF file.
    """
    pdf_writer = PyPDF2.PdfWriter()
    pages_added = False

    for pdf_path, page_range in zip(pdf_paths, page_ranges):
        try:
            with open(pdf_path, "rb") as pdf_file:
                pdf_reader = PyPDF2.PdfReader(pdf_file)
                max_pages = len(pdf_reader.pages)
                
                # Parse the page ranges
                pages = parse_page_ranges(page_range, max_pages)
                if pages is None:
                    print(f"Skipping {pdf_path} due to invalid ranges.")
                    continue
                
                # Add the specified pages to the writer
                for page_number in pages:
                    page = pdf_reader.pages[page_number - 1]  # Page numbers are 0-based
                    pdf_writer.add_page(page)
                pages_added = True
        
        except Exception as e:
            print(f"Error processing {pdf_path}: {e}")
    
    if pages_added:
        # Save the extracted pages to a new PDF
        with open(output_path, "wb") as output_file:
            pdf_writer.write(output_file)
        print(f"Extracted pages saved to {output_path}")
    else:
        print("No valid pages were extracted. No output file created.")

if __name__ == "__main__":
    # Input the number of PDFs to process
    num_pdfs = int(input("How many PDFs do you want to process? "))
    
    # Input the file paths and page ranges
    print("Enter the paths of the PDF files:")
    pdf_paths = [input(f"Path to PDF {i+1}: ") for i in range(num_pdfs)]
    
    print("Enter the page ranges to extract from each PDF (e.g., '1,3-4,6-8'):")
    page_ranges = [input(f"Page ranges for PDF {i+1}: ") for i in range(num_pdfs)]
    
    # Output file name
    output_file = input("Enter the name for the output PDF (default is 'output.pdf'): ").strip() or "output.pdf"
    
    # Extract and save pages
    extract_pages_to_pdf(pdf_paths, page_ranges, output_file)
