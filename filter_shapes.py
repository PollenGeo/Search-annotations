import pandas as pd
from omero.gateway import BlitzGateway
import tkinter as tk
from tkinter import filedialog, simpledialog


def connect_to_omero():
    """Connect to OMERO with user credentials and retrieve all groups."""
    root = tk.Tk()
    root.withdraw()

    host = simpledialog.askstring("OMERO Login", "Enter OMERO Host:", initialvalue="xxx") #Put your initial host
    username = simpledialog.askstring("OMERO Login", "Enter OMERO Username:")
    password = simpledialog.askstring("OMERO Login", "Enter OMERO Password:", show="*")

    conn = BlitzGateway(username, password, host=host, port=4064, secure=True)
    if not conn.connect():
        raise ConnectionError("Failed to connect to OMERO. Check your credentials.")

    print("Connected to OMERO successfully!")

    # Retrieve all groups
    groups = conn.getGroupsMemberOf()
    group_dict = {g.getId(): g.getName() for g in groups}

    if not group_dict:
        raise ValueError("No groups found for this user.")

    return conn, group_dict


def search_species_in_all_groups(conn, groups, species_list):
    """Search images and shapes that contain any of the species names in their annotation across all groups."""
    results = []

    for group_id, group_name in groups.items():
        conn.setGroupForSession(group_id)  # Switch to the group
        print(f"Searching in Group ID: {group_id} ({group_name})")

        # Get all images in the group
        images = list(conn.getObjects("Image"))

        for image in images:
            image_id = image.getId()

            # Check all ROIs of the image
            for roi in image.getROIs():
                for shape in roi.getShapes():
                    if shape.getTextValue():
                        shape_text = shape.getTextValue().getValue().lower()
                        
                        # Check if any species is in the annotation
                        for species in species_list:
                            if species.lower() in shape_text:
                                results.append({
                                    "group_id": group_id,
                                    "image_id": image_id,
                                    "shape_id": shape.getId().getValue(),
                                    "species_name": species
                                })

    return results


def save_results_to_csv(results):
    """Save the results to a CSV file."""
    if not results:
        print("No matches found for the species.")
        return

    df = pd.DataFrame(results)
    
    # Select the location to save the CSV file
    file_path = filedialog.asksaveasfilename(
        title="Save CSV File",
        defaultextension=".csv",
        filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")]
    )

    if not file_path:
        print("No file selected. Exiting.")
        return

    df.to_csv(file_path, index=False)
    print(f"Results saved to {file_path}")


if __name__ == '__main__':
    root = tk.Tk()
    root.withdraw()  # Hide the main Tkinter window

    try:
        conn, group_dict = connect_to_omero()

        # Ask the user for species names (comma-separated)
        species_input = simpledialog.askstring("Search Species", "Enter species names separated by commas:")

        if not species_input:
            print("No species name entered. Exiting.")
        else:
            species_list = [s.strip() for s in species_input.split(",")]  # Clean input list

            # Search in all groups
            results = search_species_in_all_groups(conn, group_dict, species_list)

            # Save the results to a CSV file
            save_results_to_csv(results)

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        if conn:
            conn.close()
