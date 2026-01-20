import os
from pdf2image import convert_from_path
from PIL import Image  # Pillow (PIL Fork) library for image manipulation

def pdf_to_images_pdf2image(pdf_path, output_folder="output_images", image_format="png", dpi=300, output_name="page", poppler_path=None): # Added poppler_path parameter
    """
    Splits a PDF file into individual images using pdf2image library, with optional poppler_path.

    Requires poppler-utils to be installed.

    Args:
        pdf_path (str): Path to the input PDF file.
        output_folder (str, optional): Folder to save the output images. Defaults to "output_images".
        image_format (str, optional): Image format for output (e.g., "png", "jpeg", "tiff"). Defaults to "png".
        dpi (int, optional): DPI (dots per inch) for image resolution. Defaults to 300.
        output_name (str, optional): Base name for output images. Defaults to "page".
        poppler_path (str, optional): Path to the poppler bin directory. If None, it relies on system PATH.
    """

    if not os.path.exists(pdf_path):
        print(f"Error: PDF file not found at '{pdf_path}'")
        return

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    try:
        images = convert_from_path(
            pdf_path,
            dpi=dpi,
            output_folder=output_folder,
            fmt=image_format,
            output_file=output_name,
            paths_only=False,
            thread_count=1,
            userpw=None,
            use_cropbox=False,
            strict=False,
            poppler_path=poppler_path  # Pass poppler_path here
        )

        for i, image in enumerate(images):
            output_file = os.path.join(output_folder, f"{output_name}_{i + 1}.{image_format.lower()}")
            image.save(output_file, format=image_format.upper())
            print(f"Page {i + 1} saved as '{output_file}'")

        print(f"\nPDF '{pdf_path}' successfully split into images in '{output_folder}' using pdf2image.")

    except Exception as e:
        print(f"An error occurred: {e}")
        print("Make sure you have poppler-utils installed and the path is correctly specified.")
        if poppler_path:
            print(f"You specified poppler_path: '{poppler_path}'")
        else:
            print("pdf2image is relying on poppler-utils being in your system's PATH.")
        print("See installation instructions in the pdf2image documentation: https://pdf2image.readthedocs.io/en/stable/installation.html")


if __name__ == "__main__":
    pdf_file_path = "pdfs/middle open.pdf"
    output_image_folder = "images"

    # **Important: Replace with the actual path to your poppler 'bin' directory:**
    my_poppler_path = r"C:\poppler-24.08.0\Library\bin"  # Example for Windows - use raw string (r"...") to avoid backslash issues

    pdf_to_images_pdf2image(
        pdf_file_path,
        output_folder=output_image_folder,
        image_format="png",
        dpi=50,
        output_name="pdf_page_popplerpath",
        poppler_path=my_poppler_path  # Pass the path here
    )

    # Example without poppler_path (relies on PATH):
    # pdf_to_images_pdf2image(pdf_file_path, output_folder="pdf_images_path", image_format="png", dpi=300, output_name="pdf_page_path")