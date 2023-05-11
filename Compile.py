## Build Resultant File
##Builds the resultant files
##This section of code takes the cleaned up layers and attirbues tables and pushes them together into one layer called the resultant. 
##It then removes tidies up the resulant file by reparing the geometry, changing multipart to single part polygons and eliminating sliver and low area polygons by merging them with their largest neighbour. 
##This code builds on and updates original code y Dr. Cosmin Mann.

import arcpy
import time
Start = time.time()

#eliminator function to eliminate the sliver polygons 
def eliminator(fc,fcout):
    arcpy.MakeFeatureLayer_management(fc, "tempLayer")
    arcpy.SelectLayerByAttribute_management("tempLayer", "NEW_SELECTION", '"Shape_Area" < 1000')
    arcpy.Eliminate_management("tempLayer", fcout)
    arcpy.Delete_management("tempLayer")

arcpy.env.workspace = r"E:\Newmont Carbon Project\Data\Data BC\02_Data\Data_Prep_GoldenBear.gdb"

arcpy.Identity_analysis ("GoldenBear_AOI", "GoldenBear_BEC", "temp1","ALL", 0.1)
arcpy.Identity_analysis ("temp1", "GoldenBear_Caribou", "temp2","ALL", 0.1)
arcpy.Identity_analysis ("temp2", "GOLDENBEAR_F_Own", "temp3","ALL", 0.1)
arcpy.Identity_analysis ("temp3", "GOLDENBEAR_SOI", "temp4","ALL", 0.1)

arcpy.Identity_analysis ("temp4", "GoldenBear_TSA", "temp5","ALL", 0.1)
arcpy.Identity_analysis ("temp5", "GoldenBear_UWR", "temp6","ALL", 0.1)
arcpy.Identity_analysis ("temp6", "GoldenBear_VQO_", "temp7","ALL", 0.1)

arcpy.Identity_analysis ("temp7", "GoldenBear_LU_1", "temp8","ALL", 0.1)
arcpy.Identity_analysis ("temp8", "GoldenBear_Watersheds", "temp9","ALL", 0.1)
arcpy.Identity_analysis ("temp9", "GoldenBear_Lakes", "temp10","ALL", 0.1)
arcpy.Identity_analysis ("temp10", "GoldenBear_Rivers", "temp11","ALL", 0.1)
arcpy.Identity_analysis ("temp11", "GoldenBear_Wetlands", "temp12","ALL", 0.1)

eliminator("temp12","temp12e")
print("administrative_management completed: identifying inventory")

arcpy.Identity_analysis ("temp12e", "GoldenBear_R1_Poly", "temp13","ALL", 0.1)
arcpy.Identity_analysis ("temp13", "GoldenBear_Lakes_Buffer", "temp14","ALL", 0.1)
arcpy.Identity_analysis ("temp14", "GoldenBear_Rivers_Buffer", "temp15","ALL", 0.1)
arcpy.Identity_analysis ("temp15", "GoldenBear_Roads_Buffer", "temp16","ALL", 0.1)
arcpy.Identity_analysis ("temp16", "GoldenBear_streams_Buffer", "temp17","ALL", 0.1)
arcpy.Identity_analysis ("temp17", "GoldenBear_wetlands_Buffer", "temp18","ALL", 0.1)

print ("temp18 is the final feature dataset")
print ("repairing Geom, multi to sgl, eliminate more polys...")

arcpy.RepairGeometry_management ("temp18")
arcpy.MultipartToSinglepart_management("temp18","temp18_sgl")
eliminator("temp18_sgl","temp18_sgl_e1")
eliminator("temp18_sgl_e1","temp18_sgl_e2")
print ('It took ', round((time.time()-Start)/60,1), " minutes to run this script.")
