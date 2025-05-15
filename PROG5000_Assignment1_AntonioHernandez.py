#===========================================================================
# Program: PROG5000_Assignment1_AntonioHernandez
#
# Purpose: Find the suitability rating for North Mountain Cougar habitat probablity
#
# Written By: Antonio Hernandez
# Date: Oct 20, 2024
# For: Introduction to Programming: Assignment 1
#===========================================================================

#While loop to be able to rerun the program
while True:
    # Get the active layer in Layers window
    layer = iface.activeLayer()

    # Create a list to include all the unique values in the SP1 field
    species_list = []

    # Loop to find all of the unique values from SP1 attribute
    for feature in layer.getFeatures():
        value = feature['SP1']
        # Prevents NULL values from being added to the list
        if value not in species_list and value != NULL:
            # Add all the unique values to species list
            species_list.append(value)
    #Creates a input prompt that allows the user to select a species from the generated list
    species_prompt = QInputDialog()
    mode = QLineEdit.Normal
    forest_sp, ok_pressed = QInputDialog.getItem(species_prompt, "Leading Species", "Select a species code", species_list)
    
    #Ends the loop and prints a message if the user presses Cancel when prompt to choose a species
    if not ok_pressed:
            print("Have a nice day!")
            break

    # Sample query by expression chosen by user
    layer.selectByExpression(f'"SP1" = \'{forest_sp}\'', QgsVectorLayer.SetSelection)
    # Modifies the color of the selection
    iface.mapCanvas().setSelectionColor(QColor("green"))
    # Stores the selected features in the forestSelection set object
    forestSelection = layer.selectedFeatures()

    # Creates counters to keep track of the number of the three suitability ratings calculated in polygons
    low_suitability_counter = 0
    med_suitability_counter = 0
    high_suitability_counter = 0

    # Creates counters to keep track of the number of the minimum areas in each suitability rating
    minarea_low = 0
    minarea_med = 0
    minarea_high = 0

    # Creates counters to keep track of the number of the maximum areas in each suitability rating
    maxarea_low = 0
    maxarea_med = 0
    maxarea_high = 0

    # Creates a counter to keep track of the total amount of area for the polygons in each suitability rating
    totalarea_low = 0
    totalarea_med = 0
    totalarea_high = 0

    # Loop through the selection set and calculate all the values
    for currFeature in forestSelection:
        # Calculates the suitability rating by using the currFeature in the selected species

        # Checks average diameter and assigns a rating depending on the value
        avg_diameter = currFeature["AVDI"]
        # If average diameter is less than 20 cm, add 0.75 points to diameter rating
        if avg_diameter < 20:
            diameter_rate = 0.75
        # If average diameter is between 20cm and 30 cm, add 1.75 points to diameter rating
        elif avg_diameter >= 20 and avg_diameter <= 30:
            diameter_rate = 1.75
        # If average diameter is higher than 30 cm, add 2.5 points to diameter rating
        else:
            diameter_rate = 2.5

        # Checks average height and assigns a rating depending on the value
        avg_height = currFeature["HEIGHT"]
        # If average height is less than 10 m, add 1.75 points to height rating
        if avg_height < 10:
            height_rate = 1.25
        # If average height is between 10 m and 20 m, add 2.5 points to height rating
        elif avg_height >= 10 and avg_height <= 20:
            height_rate = 2.5
        # If average height is higher than 20m, add 3.75 points to height rating
        else:
            height_rate = 3.75

        # Checks cover type and assigns a rating depending on the value
        cover_type = currFeature["COVER_TYPE"]
        # If cover type is 2 (softwood), add 1 point to cover rating
        if cover_type == 2:
            cover_rate = 1
        # If cover type is 5 (mixedwood), add 2 points to cover rating
        elif cover_type == 5:
            cover_rate = 2
        # If cover type is 8 (hardwood), add 3.75 point to cover rating
        else:
            cover_rate = 3.75

        # Creates a variable called suitability_rate
        # suitability_rate is calculated by adding the diameter, height, and cover rates
        suitability_rate = diameter_rate + height_rate + cover_rate

        # Checks the area of the polygons and assigns the values depending on the suitability rating
        area = currFeature["Shape_Area"]

        # If suitability rating is less than 5, assigns "low suitability" category
        if suitability_rate < 5:
            suitability_cat = "Low suitability"
            # Counter to keep track of how many "low suitability" polygons are calculated
            low_suitability_counter += 1
            # Counter to keep track of the total area in all the low suitability polygons
            totalarea_low += area
            # If the current area is lower than the current min amount, change the minimum to the current number
            if minarea_low == 0 or area < minarea_low:
                minarea_low = area
            # If the max area is higher than the current max amount, change the maximum to the current number
            if maxarea_low == 0 or area > maxarea_low:
                maxarea_low = area
        # If suitability rating is between 5 and 8, assigns "medium suitability" category
        elif 5 <= suitability_rate <= 8:
            suitability_cat = "Medium suitability"
            # Counter to keep track of how many "medium suitability" polygons are calculated
            med_suitability_counter += 1
            # Counter to keep track of the total area in the medium suitability polygons
            totalarea_med += area
            # If the current med area is lower than the current min amount, change the minimum to the current number
            if minarea_med == 0 or area < minarea_med:
                minarea_med = area
            # If the current med area is higher than the current max amount, change the maximum to the current number
            if maxarea_med == 0 or area > maxarea_med:
                maxarea_med = area
        # If suitability rating is higher than 8, assigns "high suitability" category
        else:
            suitability_cat = "High suitability"
            # Counter to keep track of how many "high suitability" polygons are calculated
            high_suitability_counter += 1
            # Counter to keep track of the total area in the maximum suitability polygons
            totalarea_high += area
            # If the current min area is lower than the current min amount, change the minimum to the current number
            if minarea_high == 0 or area < minarea_high:
                minarea_high = area
            # If the current max area is higher than the current max amount, change the maximum to the current number
            if maxarea_high == 0 or area > maxarea_high:
                maxarea_high = area

    # Calculates the average area for each suitability condition
    # Prevents division by zero if there's no data in a suitability condition by converting the values to 0
    averagearea_low = totalarea_low / low_suitability_counter if low_suitability_counter != 0 else 0
    averagearea_med = totalarea_med / med_suitability_counter if med_suitability_counter != 0 else 0
    averagearea_high = totalarea_high / high_suitability_counter if high_suitability_counter != 0 else 0

    #Prints results report in the Python console
    print()
    print("=============================================================")
    print("%s %9s" % (9 * " ", "North Mountain Cougar Habitat Suitability Analysis"))
    print("%17d  of %1s Polygons in Study Area." % (len(forestSelection), forest_sp))
    print("=============================================================")
    print("Low Suitability:")
    print("               - Number of polygons  : %10d" % low_suitability_counter)
    print("               - Minimum polygon area: %13.3f" % minarea_low)
    print("               - Maximum polygon area: %13.3f" % maxarea_low)
    print("               - Total area          : %13.3f" % totalarea_low)
    print("               - Average polygon area: %13.3f" % averagearea_low)
    print()
    print("Medium Suitability:")
    print("               - Number of polygons  : %10d" % med_suitability_counter)
    print("               - Minimum polygon area: %13.3f" % minarea_med)
    print("               - Maximum polygon area: %13.3f" % maxarea_med)
    print("               - Total area          : %13.3f" % totalarea_med)
    print("               - Average polygon area: %13.3f" % averagearea_med)
    print()
    print("High Suitability:")
    print("               - Number of polygons  : %10d" % high_suitability_counter)
    print("               - Minimum polygon area: %13.3f" % minarea_high)
    print("               - Maximum polygon area: %13.3f" % maxarea_high)
    print("               - Total area          : %13.3f" % totalarea_high)
    print("               - Average polygon area: %13.3f" % averagearea_high)
    print("=============================================================")

    #Creates list for the prompt options to rerun the program
    rerun_list = ["Yes", "No"]
    # Creates a prompt with a drop-down list for rerunning or stopping the program
    rerun_prompt = QInputDialog()
    mode = QLineEdit.Normal
    selected_option, ok_pressed = QInputDialog.getItem(rerun_prompt, "Again?", "Do you want to select another species?:", rerun_list)

    #Breaks the loop and prints a message is the user picks the "No" option  
    if selected_option:
        if selected_option == "No":
            print("Have a nice day!")
            break
    #Breaks the loop and prints a message if the user presses the "Cancel" button
    if not ok_pressed:
            print("Have a nice day!")
            break
