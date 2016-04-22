#**********************************************************************
# Description:
# Run SILO (model)
#  
#
# Arguments:
#  0 - SILO Model jar file
#  1 - Scenario (base, ron, ...)
#  2 - End year (2007, 2012, 2015, 2030, 2040)
#  3 - Exported shared file 1 - Activities.csv
#  4 - Exported shared file 2 - Households (hh_year.csv)
#  5 - Exported shared file 3 - Population (pp_year.csv)
#  6 - Exported shared file 4 - Results spatial (resultFileSpatial_year.csv)
#  7 - Exported shared file 5 - Households by size (HH_By_SIZ_INC_year.csv)
#  8 - Exported shared file 6 - Households by workers (HH_By_WRKS_INC_year.csv)
#  9 - Exported shared file 7 - Change of household and job numbers (resultFileSpatial_2030VS2010.csv)
#  
# Created by: Harutyun Shahumyan
#**********************************************************************

# Standard error handling
try:

    import arcpy
    import time
    import os
    import string

    start = time.time()
    arcpy.AddMessage("")
    arcpy.AddMessage("******************************************************")
    arcpy.AddMessage("SILO model start time: %s" % time.strftime('%X %x %Z'))

    # Get input arguments 
    in_Program = arcpy.GetParameterAsText(0)
    in_Scenario = arcpy.GetParameterAsText(1) 
    in_EndYear = arcpy.GetParameterAsText(2)

     # Check that the program exist
    if not arcpy.Exists(in_Program):
       raise Exception, "Input program does not exist"

    # Run the model / program
    arcpy.AddMessage("")
    arcpy.AddMessage("Running %s" % (in_Program)) 
    arcpy.AddMessage("Scenario: %s" % (in_Scenario))  
    arcpy.AddMessage("End year: %s" % (in_EndYear)) 

    desc = arcpy.Describe(in_Program)
    sourceFilePath = desc.path
    os.chdir(sourceFilePath)
    os.system(in_Program)

 
    # Export shared file
    arcpy.AddMessage("Exporting exchange data files ...")

    outputFile_activities = sourceFilePath + "\\scenOutput\\" + in_Scenario + "\\activitiesBySilo_"+in_EndYear+".csv"
    outputFile_results = sourceFilePath + "\\scenOutput\\" + in_Scenario + "\\resultFileSpatial_"+in_EndYear+".csv"
    outputFile_resultsChange = sourceFilePath + "\\scenOutput\\" + in_Scenario + "\\resultFileSpatial_"+in_EndYear+"VS2010.csv"
    outputFile_hh = sourceFilePath + "\\microData\\hh_"+in_EndYear+".csv"
    outputFile_pp = sourceFilePath + "\\microData\\pp_"+in_EndYear+".csv"
    outputFile_hhbysz = sourceFilePath + "\\scenOutput\\" + in_Scenario + "\\HH_By_SIZ_INC_"+in_EndYear+".csv"
    outputFile_hhbywr = sourceFilePath + "\\scenOutput\\" + in_Scenario + "\\HH_By_WRKS_INC_"+in_EndYear+".csv"

    arcpy.AddMessage(outputFile_activities)
    arcpy.SetParameter(3, outputFile_activities)
    arcpy.AddMessage(outputFile_hh)
    arcpy.SetParameter(4, outputFile_hh)
    arcpy.AddMessage(outputFile_pp)
    arcpy.SetParameter(5, outputFile_pp)
    arcpy.AddMessage(outputFile_results)
    arcpy.SetParameter(6, outputFile_results)
    arcpy.AddMessage(outputFile_hhbysz)
    arcpy.SetParameter(7, outputFile_hhbysz)
    arcpy.AddMessage(outputFile_hhbywr)
    arcpy.SetParameter(8, outputFile_hhbywr)
    arcpy.AddMessage(outputFile_resultsChange)
    arcpy.SetParameter(9, outputFile_resultsChange)

    elapsed = (time.time() - start)

    arcpy.AddMessage("")
    arcpy.AddMessage("Model end time: %s" % time.strftime('%X %x %Z'))
    arcpy.AddMessage("Processing time in seconds is %s" % str(elapsed ))
    arcpy.AddMessage("******************************************************")
    arcpy.AddMessage("")


# Handle script errors
except Exception, errMsg:

    # If we have messages of severity error (2), we assume a GP tool raised it,
    #  so we'll output that.  Otherwise, we assume we raised the error and the
    #  information is in errMsg.
    #
    if arcpy.GetMessages(2):   
        arcpy.AddError(arcpy.GetMessages(2))
    else:
        arcpy.AddError(str(errMsg))   
