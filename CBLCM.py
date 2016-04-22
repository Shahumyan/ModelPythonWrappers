#**********************************************************************
# Description:
# CBLCM model wrapper
#  
#
# Arguments:
#  0 - CBLCM Model bat file
#  1 - Output folder
#  2 - Output Land cover image file (Growth_I001_2030.tif)
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
    arcpy.AddMessage("CBLCM model start time: %s" % time.strftime('%X %x %Z'))
 

    # Get input arguments 
    in_Program = arcpy.GetParameterAsText(0)
    in_OutputFolder = arcpy.GetParameterAsText(1)


    # Check that the program exist
    if not arcpy.Exists(in_Program):
       raise Exception, "Input program does not exist"

  
    # Run the model / program
    arcpy.AddMessage("")
    arcpy.AddMessage("Running %s" % (in_Program))  

    desc = arcpy.Describe(in_Program)
    sourceFilePath = desc.path
    os.chdir(sourceFilePath)
    os.system(in_Program)

    # Export shared files
    OutputImage = in_OutputFolder + "\Images\Growth_I001_2030.tif"
    
    arcpy.SetParameter(2, OutputImage)

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
