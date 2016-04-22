#**********************************************************************
# Description:
# Converts and saves table into csv file.
# Designed for the application in ArcGIS. 
#
# Arguments:
#  0 - Input table
#  1 - Save folder
#  2 - Save file name
#  3 - output csv file
#
# Created by: Harutyun Shahumyan
#**********************************************************************

# Standard error handling - put everything in a try/except block
#
try:

    # Import system modules
    import string
    import arcgisscripting
    import arcpy
    import csv  
    import numpy as np

    # Create the Geoprocessor object
    gp = arcgisscripting.create()  

    # Get input arguments 
    in_table = gp.GetParameter(0)  
    in_Folder = gp.GetParameter(1)
    in_fileName = gp.GetParameterAsText(2)
	
    # Output file path and name
    outfile = str(in_Folder) + "\\" + in_fileName + ".csv"
	
    # Check that the table exist
    if not gp.Exists(in_table):
       raise Exception, "Input table does not exist"  
	   
    # Check that the folder exist
    if not gp.Exists(in_table):
       raise Exception, "Save folder does not exist"  
	   
    #--make a list of all of the fields in the table  
    fields = arcpy.ListFields(in_table)  
    field_names = [field.name for field in fields]  
  
    with open(outfile,'wb') as f:  
	w = csv.writer(f, delimiter='\t')  
	#--write all field names to the output file  
	w.writerow(field_names)  
	  
	#--now we make the search cursor that will iterate through the rows of the table  
	for row in arcpy.SearchCursor(in_table):  
		field_vals = [int(row.getValue(field.name)) for field in fields]  
		w.writerow(field_vals)  
	del row
 
    # Output
    gp.AddMessage("The output table is saved in %s\\%s.csv" % (in_Folder, in_fileName)) 
    gp.SetParameterAsText(3, outfile)

# Handle script errors
#
except Exception, errMsg:

    # If we have messages of severity error (2), we assume a GP tool raised it,
    #  so we'll output that.  Otherwise, we assume we raised the error and the
    #  information is in errMsg.
    #
    if gp.GetMessages(2):   
        gp.AddError(gp.GetMessages(2))
    else:
        gp.AddError(str(errMsg))   

