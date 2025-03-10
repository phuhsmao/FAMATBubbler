import os

def rename_png_to_jpg(folder_path):
    """
    Renames all files with the .png extension to .jpg in the specified folder.

    Args:
        folder_path (str): The path to the folder containing the files to rename.
    """
    if not os.path.isdir(folder_path):
        print(f"Error: Folder '{folder_path}' does not exist.")
        return

    for filename in os.listdir(folder_path):
        if filename.lower().endswith(".png"):
            base_filename, ext = os.path.splitext(filename)
            new_filename = base_filename + ".jpg"
            old_filepath = os.path.join(folder_path, filename)
            new_filepath = os.path.join(folder_path, new_filename)

            try:
                os.rename(old_filepath, new_filepath)
                print(f"Renamed '{filename}' to '{new_filename}'")
            except OSError as e:
                print(f"Error renaming '{filename}': {e}")

    print("Renaming process complete.")

if __name__ == "__main__":
    folder_to_rename = input("Enter the path to the folder containing PNG files: ")
    rename_png_to_jpg(folder_to_rename)