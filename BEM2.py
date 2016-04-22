#**********************************************************************
# Description:
# Run BEM (model)
#  
#
# Arguments:
#  0 - BEM Model R file
#  1 - Base year (2007)
#  2 - End year (2015, 2030, 2040)
#  3 - Scenario
#  4 - Exported shared file 1 - Sectoral CO2 (BEM_CO2_SECTOR_FINAL_scenario_2007-2030)
#  
# Created by: Harutyun Shahumyan
#**********************************************************************

# Standard error handling
try:

    import arcpy
    import time
    import os
    import string
    import subprocess

    start = time.time()
    arcpy.AddMessage("")
    arcpy.AddMessage("******************************************************")
    arcpy.AddMessage("BEM model start time: %s" % time.strftime('%X %x %Z'))

    # Get input arguments 
    in_Program = arcpy.GetParameterAsText(0)
    in_BaseYear = arcpy.GetParameterAsText(1) 
    in_EndYear = arcpy.GetParameterAsText(2)
    in_Scenario = arcpy.GetParameterAsText(3)

     # Check that the program exist
    if not arcpy.Exists(in_Program):
       raise Exception, "Input program does not exist"

    # Run the model / program
    arcpy.AddMessage("")
    arcpy.AddMessage("Running %s" % (in_Program)) 
    arcpy.AddMessage("Base year: %s" % (in_BaseYear))  
    arcpy.AddMessage("End year: %s" % (in_EndYear)) 
    arcpy.AddMessage("Scenario: %s" % (in_Scenario))
 

    desc = arcpy.Describe(in_Program)
    sourceFilePath = desc.path


    pathRScript = "C:\\Program Files\\R\\R-3.0.1\\bin\\x64"
    runProgram = "RScript" + " " + in_Program +" "+ in_BaseYear +" "+ in_EndYear+" "+ in_Scenario
   # runProgram2 = in_Program +" "+ in_BaseYear +" "+ in_EndYear
    arcpy.AddMessage("Running: %s" % (runProgram)) 

    os.chdir(pathRScript)
   # os.system("RScript.exe E:\\BEM2\\BEM2_MODEL.R 2007 2030")
    os.system(runProgram)

   # proc = subprocess.Popen([pathRScript,runProgram2 ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  #  stdout, stderr = proc.communicate()

 
    # Export shared file
    arcpy.AddMessage("Exporting exchange data files ...")


    outputFile_CO2Sectors = sourceFilePath + "\\OUTPUT\\" + "BEM_CO2_FINAL_"+ in_Scenario +"_2007-"+ in_EndYear +".csv"

    arcpy.AddMessage(outputFile_CO2Sectors)
    arcpy.SetParameter(4, outputFile_CO2Sectors)


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
