#**********************************************************************
# Description:
# MSTM model wrapper
#  
#
# Arguments:
#  0 - MSTM Model executable file
#  1 - MSTM Scenario folder
#  2 - Modelling year (should be similar to recent SILO End year)
#  3 - Output for SILO 1: HwyOP_iter6.omx (Saved in Scenario folder)
#  4 - Output for SILO 2: WTrnPK.omx (Saved in Scenario folder)
#  5 - Output: VMT_VHT_byCty.csv (Saved in Scenario folder\Validation)
#  6 - Output: VMT_BySWFT.csv (Saved in Scenario folder\Validation)
#  7 - Output: Ridership file MCEstimate.rpt (Saved in Scenario folder)
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
    arcpy.AddMessage("MSTM model start time: %s" % time.strftime('%X %x %Z'))
 

    # Get input arguments 
    in_Program = arcpy.GetParameterAsText(0)
    in_Scenario = arcpy.GetParameterAsText(1)
    in_Year = arcpy.GetParameterAsText(2)

 
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
    sourceFilePath = in_Scenario
    skm2SILO1=sourceFilePath+"\\HwyOP_iter6.skm"
    skm2SILO2=sourceFilePath+"\\WTrnPK.skm"

    # Convert Skim Matrices from the MSTM to OMX Matrices for SILO
    cube2omx_converter = "E:\\models\\cube2omx\\cube2omx.exe"
    os.system(cube2omx_converter+ " " + skm2SILO1)
    os.system(cube2omx_converter+ " " + skm2SILO2)
    omx2SILO1=sourceFilePath+"\\HwyOP_iter6.omx"
    omx2SILO2=sourceFilePath+"\\WTrnPK.omx"

    # Rename output files to include the modelling year as defined in SILO properties file
    omx2SILO1_year=sourceFilePath+"\\HwyOP_iter6_"+str(in_Year)+".omx"
    omx2SILO2_year=sourceFilePath+"\\WTrnPK_"+str(in_Year)+".omx"
    if arcpy.Exists(omx2SILO1_year):
	os.remove(omx2SILO1_year)
    os.rename(omx2SILO1, omx2SILO1_year)
    if arcpy.Exists(omx2SILO2_year):
	os.remove(omx2SILO2_year)
    os.rename(omx2SILO2, omx2SILO2_year)


    arcpy.AddMessage("Exporting data files for SILO:") 
    arcpy.AddMessage(omx2SILO1_year)
    arcpy.AddMessage(omx2SILO2_year)
    arcpy.SetParameter(3, omx2SILO1_year)
    arcpy.SetParameter(4, omx2SILO2_year)


    VMT_VHT_byCty=sourceFilePath+"\\Validation\\VMT_VHT_byCty.csv"
    VMT_BySWFT=sourceFilePath+"\\Validation\\VMT_BySWFT.csv"
    MCEstimate=sourceFilePath+"\\MCEstimate.rpt"

    arcpy.AddMessage("Exporting other data files:") 
    arcpy.AddMessage(VMT_VHT_byCty)
    arcpy.AddMessage(VMT_BySWFT)
    arcpy.AddMessage(MCEstimate)
    arcpy.SetParameter(5, VMT_VHT_byCty)
    arcpy.SetParameter(6, VMT_BySWFT)
    arcpy.SetParameter(7, MCEstimate)
    
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
