=========================================
 OMERO Species Annotation Search
=========================================

Description:
------------
This Python script connects to an OMERO server and searches for species names within 
image annotations (ROIs) across all groups that the user is a member of. The script 
allows the user to specify species names and then retrieves images and shapes where 
those species appear in annotations. The results are saved to a CSV file.

Features:
---------
- Connects to an OMERO server with user-provided credentials.
- Retrieves all OMERO groups the user belongs to.
- Searches for species names in image shape annotations (ROIs).
- Scans all available images within each group.
- Saves results to a CSV file.

CSV Output Format:
------------------
If matches are found, the script saves the results in a CSV file with the following columns:

| Column      | Description                                         |
|------------ |-----------------------------------------------------|
| group_id    | ID of the OMERO group where the match was found.    |
| image_id    | ID of the image containing the annotation.          |
| shape_id    | ID of the shape (ROI) containing the species name.  |
| species_name | The species name found in the annotation.          |

Requirements:
-------------
The script requires the following Python libraries:
- pandas
- omero-gateway
- tkinter (built-in for most Python distributions)

Installation:
-------------
Before running the script, install the required dependencies:

1. Install necessary Python packages:
pip install pandas pip install omero-py
2. If `tkinter` is not installed, install it manually (Linux users only):
sudo apt-get install python3-tk

Usage:
------
1. Run the script:
python filter_shapes.py
2. Enter OMERO server credentials when prompted.
3. Provide a comma-separated list of species names to search for.
4. The script will scan all groups and images for the specified species.
5. If matches are found, the script will prompt you to save the results to a CSV file.

Author:
-------
This script was developed by **Daurys De Alba**.
For inquiries, contact:
- Email: daurysdealbaherra@gmail.com
- Email: DeAlbaD@si.edu
