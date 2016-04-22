#**********************************************************************
# Description:
# Converts and saves table into csv file.
# Designed for the application in ArcGIS. 
#
# Arguments:
#  0 - Input table
#  1 - Save folder
#  2 - Output file name
#  3 - Export column number (starting from 0)
#  4 - Export column 2 number (optional, for second year)
#  5 - Input table year
#  6 - Input table year 2 (optional, required if column 2 is filled)
#  7 - Output file

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
    in_col = gp.GetParameter(3)
    in_col2 = gp.GetParameter(4) # column for 2040 data, optional
    in_year = gp.GetParameterAsText(5) # 2030
    in_year2 = gp.GetParameterAsText(6) # 2040 optional

    # Check that the table exist
    if not gp.Exists(in_table):
       raise Exception, "Input table does not exist"  
	   
    # Check that the folder exist
    if not gp.Exists(in_Folder):
       raise Exception, "Save folder does not exist" 

    # Output file path and name
    outfile = str(in_Folder) + "\\" + in_fileName

	   
    #Transpose the csv file according to CBLCM requirements
    if in_col2>0:
        export_cols = (1,)+(in_col,)+(in_col2,) #if you need to transpose whole table, add all column indexes instead of in_col.
    else: 
        export_cols = (1,)+(in_col,)

    data = np.genfromtxt(str(in_table),delimiter="\t", dtype=None, usecols = export_cols)
    data[0][0]=data[0][1]
    data[0][1]=in_year 
    if (in_year2<>"" and in_col2>0):
       data[0][2]=in_year2 

    np.savetxt(outfile,data.T,delimiter="\t",fmt='%s')

    # Output
    gp.AddMessage("The output table is saved in %s\\%s" % (in_Folder, in_fileName)) 
    gp.SetParameterAsText(7, outfile)

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

