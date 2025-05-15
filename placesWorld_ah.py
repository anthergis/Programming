#===========================================================================
# Program: placesWorld_ah.py
#
# Purpose: Determine the longitude and latitude quadrant of places
#
# Programmer: Antonio Hernandez
# Date: November 18, 2024
# For: Introduction to Programming: Assignment 2
#===========================================================================

import os

# Function to determine latitude position
def getNSHemi(yCoord):
    if yCoord >= 0:
        return "North"
    else:
        return "South"

# Function to determine longitude position
def getEWHemi(xCoord):
    if xCoord >= 0:
        return "Eastern"
    else:
        return "Western"

# Main function
def main():
    # Prompt for user to enter a filename
    title = "Filename"
    label = "Please enter a filename: "
    file_name, ok_pressed = QInputDialog.getText(None, title, label, QLineEdit.Normal)

    # Prompt for user to enter a working directory
    title = "Working Directory"
    label = "Please enter a working directory: "
    work_dir, ok_pressed = QInputDialog.getText(None, title, label, QLineEdit.Normal)

    # Checks if the directory exists and changes to it
    if os.path.exists(work_dir):
        os.chdir(work_dir)
    # Sets working directory to default if user prompt does not exist
    else:
        print("Directory does not exist. Directory set to C:/temp")
        work_dir = "C:/temp"

    # Creates text file with the user input
    outfile = os.path.join(work_dir, "%s.txt" % file_name)
    
    # Get all vector layers in the project
    layers = QgsProject.instance().mapLayers().values()

    # Dictionary to store data for 14 values
    report_dict = {
        "total_places_NE": 0, "total_places_NW": 0,
        "total_places_SE": 0, "total_places_SW": 0,
        "total_pop_NE": 0, "total_pop_NW": 0,
        "total_pop_SE": 0, "total_pop_SW": 0,
        "highest_pop_place": "", "highest_pop_value": 0,
        "lowest_pop_place": "", "lowest_pop_value": 100000000,
        "highest_pop_quadrant": "", "lowest_pop_quadrant": ""
    }

    # Loop through each layer in the project
    for layer in layers:
    #select all features if the user does not select any points
        if layer.selectedFeatureCount() == 0:
            layer.selectAll()

        # Loop through each selected feature in the current layer
        for feature in layer.getSelectedFeatures():
            # Get geometry of feature and extract x (longitude) and y (latitude) coordinates
            geom = feature.geometry()
            xCoord = geom.asPoint().x()
            yCoord = geom.asPoint().y()
            
            # Retrieves the name and population of the places
            place = feature['nameascii']  
            population = feature['pop_max']
            
            # Determines the hemisphere and quadrant of a place based on the coordinates
            nsHemi = getNSHemi(yCoord)
            ewHemi = getEWHemi(xCoord)
            
            #Updates the total population in each quadrant
            #Adds 1 to the count for each quadrant and keeps a running total
            if nsHemi == "North" and ewHemi == "Eastern":
                report_dict["total_pop_NE"] += population
                report_dict["total_places_NE"] += 1
                quadrant = "northeastern"
            elif nsHemi == "North" and ewHemi == "Western":
                report_dict["total_pop_NW"] += population
                report_dict["total_places_NW"] += 1
                quadrant = "northwestern"
            elif nsHemi == "South" and ewHemi == "Eastern":
                report_dict["total_pop_SE"] += population
                report_dict["total_places_SE"] += 1
                quadrant = "southeastern"
            elif nsHemi == "South" and ewHemi == "Western":
                report_dict["total_pop_SW"] += population
                report_dict["total_places_SW"] += 1
                quadrant = "southwestern"
            
            #Updates the place and population with the highest value
            if population > report_dict["highest_pop_value"]:
                report_dict["highest_pop_place"] = place
                report_dict["highest_pop_value"] = population
                report_dict["highest_pop_quadrant"] = quadrant
            
            #Updates the place and population with the lowest value
            if population < report_dict["lowest_pop_value"]:
                report_dict["lowest_pop_place"] = place
                report_dict["lowest_pop_value"] = population
                report_dict["lowest_pop_quadrant"] = quadrant

    #Writes the report to the text file
    with open(outfile, "w") as file:
        file.write("Report of Selected World Places\n")
        file.write("==========================================================================\n")
        file.write(str(report_dict["total_places_NE"]) + " northeastern places have a total population of " + str(report_dict["total_pop_NE"]) + "\n")
        file.write(str(report_dict["total_places_NW"]) + " northwestern places have a total population of " + str(report_dict["total_pop_NW"]) + "\n")
        file.write(str(report_dict["total_places_SE"]) + " southeastern places have a total population of " + str(report_dict["total_pop_SE"]) + "\n")
        file.write(str(report_dict["total_places_SW"]) + " southwestern places have a total population of " + str(report_dict["total_pop_SW"]) + "\n")
        file.write("==========================================================================\n")
        file.write("The " + report_dict["highest_pop_quadrant"] + " place of " + report_dict["highest_pop_place"] + " has the highest population of " + str(report_dict["highest_pop_value"]) + "\n")
        file.write("The " + report_dict["lowest_pop_quadrant"] + " place of " + report_dict["lowest_pop_place"] + " has the lowest population of " + str(report_dict["lowest_pop_value"]) + "\n")

    # Deselect all the features in the layer
    for layer in layers:
        layer.removeSelection()

# Runs the main function
main()