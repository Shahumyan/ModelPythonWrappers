#**********************************************************************
# Description:
# MEM model wrapper
#  
#
# Arguments:
#  0 - MEM Model bat file //Cube script (.s) file
#  1 - CUBE Voyager run program 
#  2 - Output folder
#  3 - Output 1: AQ_byCty.csv (Air quality for cities)
#  4 - Output 2: AQ_BASE_PM.CSV  (Summary of air quality for MD)
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
    arcpy.AddMessage("MEM model start time: %s" % time.strftime('%X %x %Z'))
 

    # Get input arguments 
    in_Program = arcpy.GetParameterAsText(0)
    in_CubeVoyager = arcpy.GetParameterAsText(1)
    in_OutputFolder = arcpy.GetParameterAsText(2)

    # Check that the program exist
    if not arcpy.Exists(in_Program):
       raise Exception, "Input program does not exist"

    # MSTM run parameters
    runCommand="\""+in_CubeVoyager+"\" "+in_Program
  
    # Run the model / program
    arcpy.AddMessage("")
    arcpy.AddMessage("Running %s" % (in_Program))  
 #   arcpy.AddMessage("Running %s" % (runCommand)) 

    desc = arcpy.Describe(in_Program)
    sourceFilePath = desc.path
    os.chdir(sourceFilePath)
    os.system(in_Program)
    #os.system(runCommand)

    # Export shared files
    outputFile1 = "\AQ_byCty.csv"
    outputFile2 = "\AQ_BASE_PM.csv"
    arcpy.SetParameterAsText(3, in_OutputFolder+outputFile1)
    arcpy.SetParameterAsText(4, in_OutputFolder+outputFile2)

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
