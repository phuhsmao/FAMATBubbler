import pandas as pd

def get_tens_place(n):
    return abs(n) // 10 % 10  # Use abs() to handle negative numbers correctly


def create_roster_for_sheet(excel_filepath, sheet_name):
    """
    Creates a Palm Harbor style roster (one line per student) from Excel sheet data,
    extracting data based on cell positions and deriving division from Student ID.

    Args:
        excel_filepath (str): Path to the Excel file.
        sheet_name (str): Name of the Excel sheet (School Name).

    Returns:
        str: Palm Harbor style roster string, or None on error.
    """
    print(f"\n--- Processing sheet: '{sheet_name}' ---")

    try:
        df = pd.read_excel(excel_filepath, sheet_name=sheet_name, header=None)
    except Exception as e:
        print(f"Error reading sheet '{sheet_name}': {e}")
        return None

    if df.empty:
        print(f"Warning: Sheet '{sheet_name}' is empty.")
        return None

    school_name = df.iloc[0, 2]
    school_id_cell = df.iloc[1, 2]

    if pd.notna(school_name):
        school_name = str(school_name)
    else:
        school_name = sheet_name
        print(f"Warning: School Name in C1 empty, using sheet name.")

    school_id = "N/A"
    if pd.notna(school_id_cell):
        try:
            school_id = str(int(school_id_cell))
        except ValueError:
            print(f"Warning: Invalid School ID in C2 for '{sheet_name}'.")
        except TypeError:
            print(f"Warning: School ID in C2 for '{sheet_name}' is not a number.")
    else:
        print(f"Warning: School ID in C2 for '{sheet_name}' is empty.")

    roster_output = f"Roster: {school_name} #{school_id}\n"
    roster_output += "Student Name Division Team 1 ID Team 2 ID No Team ID \n"

    division_map = { # Division mapping based on 2nd to last digit of Student ID
        "1": {"div_name": "4th Grade", "div_num": 1, "div_id": 10},
        "2": {"div_name": "5th Grade", "div_num": 2, "div_id": 20},
        "3": {"div_name": "6th Grade", "div_num": 3, "div_id": 30},
        "4": {"div_name": "7th Grade", "div_num": 4, "div_id": 40},
        "5": {"div_name": "Algebra", "div_num": 5, "div_id": 50},
        "6": {"div_name": "Geometry", "div_num": 6, "div_id": 60},
    }
    default_division_info = {"div_name": "Division", "div_num": 0, "div_id": "00"} # Default division

    start_row = 8

    for index, row in df.iloc[start_row:].iterrows():
        student_id_cell = row.iloc[6]
        student_name_cell = row.iloc[2]
        student_num_cell = row.iloc[3] # Student # from Column D (index 3)

        if pd.notna(student_id_cell):
            student_id = ""
            student_number = "" # Changed variable name to student_number to match requested output line
            try:
                student_id = str(int(student_id_cell))
            except ValueError:
                student_id = "Invalid ID"
                print(f"Warning: Invalid Student ID in row {index + 2} of '{sheet_name}'.")
            except TypeError:
                student_id = "Invalid ID"
                print(f"Warning: Non-numeric Student ID in row {index + 2} of '{sheet_name}'.")

            try:
                student_number = str(int(student_num_cell)) # Changed variable name to student_number
            except ValueError:
                student_number = "Invalid No"
                print(f"Warning: Invalid Student No '{student_num_cell}' in row {index + 2} of '{sheet_name}'. Setting Student No to 'Invalid No'.")
            except TypeError:
                student_number = "Invalid No"
                print(f"Warning: Non-numeric Student No '{student_num_cell}' in row {index + 2} of '{sheet_name}'. Setting Student No to 'Invalid No'.")


            student_name = str(student_name_cell) if pd.notna(student_name_cell) else "N/A"

            # --- Format Student Name to Lastname, Firstname ---
            if "," in student_name:
                student_name_formatted = student_name.strip()
            else:
                parts = student_name.split()
                if len(parts) >= 2:
                    last_name = parts[-1].strip()
                    first_name = " ".join(parts[:-1]).strip()
                    student_name_formatted = f"{last_name}, {first_name}"
                else:
                    student_name_formatted = student_name.strip()

            if student_name_formatted != "N/A": # Skip rows with "N/A" names
                # --- Determine Division from Student ID (2nd to last digit) ---
                division_digit = student_id[-2] if len(student_id) >= 2 else "0" # Default to "0" if ID too short
                division_info = division_map.get(division_digit, default_division_info) # Use default if digit not in map
                division_name = division_info["div_name"]
                division_number = get_tens_place(division_info["div_id"]) # Changed variable name to division_number
                div_num = division_info["div_num"] # Get div_num for "No" values

                student_number = str(student_number).zfill(3)

                # --- Construct "No" values based on div_num (Corrected) ---
                no_val_1 = f"{div_num}1" # Use div_num here (Corrected)
                no_val_2 = f"{div_num}2" # Use div_num here (Corrected)
                no_val_0 = f"{div_num}0" # Use div_num here (Corrected)


                roster_output += (f"{student_name_formatted} {division_name} {school_id} {student_number} {division_number}1 {school_id} {student_number} {division_number}2 {school_id} {student_number} {division_number}0\n") # Correct roster line with requested variables - LINE UPDATED BASED ON USER REQUEST

    return roster_output


# --- Main Script (No changes needed in main part) ---
excel_file = '2025 Mighty Mu Student Codes.xlsx'  # <<<--- Make sure your file name is correct!
schools_to_process = [
    "Clearwater Fundamental Middle",
]

school_rosters = {}
for sheet_name in schools_to_process:
    roster = create_roster_for_sheet(excel_file, sheet_name)
    if roster:
        school_rosters[sheet_name] = roster

if school_rosters:
    print("\n--- Generated Rosters ---")
    for school_name, roster_text in school_rosters.items():
        print(roster_text)
else:
    print("\nNo rosters were generated.")