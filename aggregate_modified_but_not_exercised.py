

#FILE NAME: aggregate_modified_but_not_exercised.py

#AUTHOR: Sudheer Kollapudi


#PURPOSE: This script scans through the aggregate report and identifies the code package
# procedures that were modified but were not exercised using the “New and Modified for CH-53K” input file.


import re
import exceptions
import csv
import sca_utilities

totals = "TOTALS"
#string variables to hold messages.
used_not_exci = "used but not exercised"
used_and_exci ="100% exercised"
partially_exci= "partially exercised"
not_in_metri_csv = "not found in metrics csv report"
all_proc_func_used = "All procedures and functions are used"
partially_used = "partially used"
not_used="not used"
dot="."
dot_edit=".edit"


new_and_modified_procedures_csv_file_columns_ids=[0,1,3]
metrics_report_csv_file_columns_ids=[2,4,3,6]
metrics_report_columns_ids=[0,1,2,3,4,5,6,7,8]


def Is_Procedure_Used(new_and_modified_procedures_csv_file_path,#(Input)
         metrics_report_csv_file_path,#(Input,output)(this file will be overwrite with new data))
         aggregate_report_html_file_path,#(Input)
         modified_but_not_exercised_csv_file_path): #(Output)
   
#-------------------------------------------------------------------------------------
#FUNCTIONAL DESCRIPTION:

#PURPOSE: This script scans through the aggregate report and identifies the code package
#           procedures that were modified but were not exercised using the “New and Modified for CH-53K” input file.

#new_and_modified_procedures_csv_file_path:which contains new and modified procedures
#metrics_report_csv_file_path:which contains metrics data 
#aggregate_report_html_path:which contains aggregate report
#modified_but_not_exercised_csv_file_path:output .csv file which contains new and modified procedures with used or not used column 

#new_and_modified_procedures_csv_file_path file should be 
# ----------------------------------------------------------------------------------------|-------------
# Code_Package       |  Function_Procedure_Name                 |  Function_Procedure_Type|Modified/New
# -------------------|------------------------------------------|------------------------ |------------- 
# a661_manager.2.ada |  Log_Error                               |  procedure              |Modified
# -------------------|------------------------------------------|-------------------------|--------------
# a661_manager.2.ada |  Update_Bezel_Suppression_Counter        |  procedure              | Modified
# -------------------|------------------------------------------|-------------------------|--------------

#modified_but_not_exercised_csv_file_path file would be 
# ----------------------------------------------------------------------------------------|
# Code_Package       |  Function_Procedure_Name                 |  Exercised_Or_Not       |
# -------------------|------------------------------------------|-------------------------| 
# a661_manager.2.ada |  Log_Error                               |  not used               |
# -------------------|------------------------------------------|-------------------------|
# p_page_data.2.ada |  Toggle_Baro_Display        |  used but not exercised               |
# -------------------|------------------------------------------|-------------------------|

#new_and_modified_procedures_csv_file_path file would be (overwrite)
#--------------------|-----------------|-----------------|-----------|-------------------------------|----------|----------------------------------|------------------|--------------------|----------------|---------------
#Subsystem           | SubFolder       |  Filename       |           | Subprogram                    |Complexity| DO-178B Level C Cover % Statement|Covered Statements|   Total Statements |  New/Modified  |  Used/Not Used
#--------------------|-----------------|-----------------|-----------|-------------------------------|----------|----------------------------------|------------------|--------------------|----------------|-------------
#a661_api.ss         |                 | a661_api.2.ada  | Subprogram|A661_AGS_SET_POSITION_ON_WIDGET|     1    |  0%                              |    0             |     1              |     New        |  not used
#--------------------|-----------------|-----------|-----|-----------|-------------------------------|----------|----------------------------------|------------------|--------------------|----------------|---------------
#fpln_attributes.ss  |                 | f_lobe_rcf.2.ada| TOTALS    |       10                      |     13   |  0%                              |  0               |     25             |                |partially used
#--------------------|-----------------|-----------------|-----------|-------------------------------|----------|----------------------------------|---------------------------------------|----------------|---------------

#LIMITATIONS: None

#NOTES: None  

# ALGORITHM AND CODE  


   #check check_file_types
   sca_utilities.check_file_type(new_and_modified_procedures_csv_file_path,'.csv')
   sca_utilities.check_file_type(metrics_report_csv_file_path,'.csv')
   sca_utilities.check_file_type(modified_but_not_exercised_csv_file_path,'.csv')
   sca_utilities.check_file_type(aggregate_report_html_file_path,'.html')
   
  
   modi_but_not_exci_for_zero_percent=[]
   modi_but_not_exerci=[] 
   modi_but_not_exerci.append(["Code_Packages","Function_Procedure_Name","Exercised_Or_Not"])
   #list to hold all code packages 
   code_packages=[]
   #list to hold 0,1,3 columns data of new_and_modified_procedures_csv_file_path
   new_and_modified_procedures_data=[]
   #list to hold 2,4,3,6 columns data of metrics_report_csv_file_path
   metrics_csv_data = []
   #list to hold 0,1,2,3,4,5,6,7,8 columns data of metrics_report_csv_file_path
   metrics_all_columns_csv_data=[]

   #---------code to get form both csv files ------------------------     
   new_and_modified_procedures_data=sca_utilities.get_csv_data(new_and_modified_procedures_csv_file_path,
                                                               new_and_modified_procedures_csv_file_columns_ids,True) 
   code_packages=sca_utilities.get_csv_data(metrics_report_csv_file_path,
                                                               [2],True) 
   metrics_all_columns_csv_data=sca_utilities.get_csv_data(metrics_report_csv_file_path,
                                                               metrics_report_columns_ids,False) 
   metrics_csv_data=sca_utilities.get_csv_data(metrics_report_csv_file_path,
                                                               metrics_report_csv_file_columns_ids,True)
   
   #append headings of columns for metrics_report_csv_file_path
   metrics_all_columns_csv_data[0].append("New/Modified")
   metrics_all_columns_csv_data[0].append("Used/Not Used")
   
   #---------code to convert html dat to text data --------------------------
   text_data = sca_utilities.convert_html_to_text(aggregate_report_html_file_path)
   
   #-------------------------------- code for individual procedures and function to find exercised or not ------------------    
   #loop for each new and modified procedures  
   for code_package_data in new_and_modified_procedures_data:
      code_package_data_found=False
      row_value=1
      #search new and modified procedures in metrics report
      for aggr_data in metrics_csv_data:
         
         #if new and modified procedures found in metrics report then check that procedure used in aggregate report or not.
         if ((code_package_data[0].lower() == aggr_data[0].lower()) and (code_package_data[1].lower()==aggr_data[1].lower())and(aggr_data[2] != totals)):
            code_package_data_found=True
            metrics_all_columns_csv_data[row_value].append(code_package_data[2])
            
            if aggr_data[3] != "100%":
               #if procedure is  "0%" then check that procedure is used in aggregate report or not.
               if aggr_data[3] == "0%":
                  package_name_without_ada_extension=code_package_data[0][:-6]
                  found_dot = package_name_without_ada_extension.find(dot)
                  found_dot_edit=package_name_without_ada_extension.find(dot_edit)
                  found_in_html = 0 
                  
                  #check that procedure is used in aggregate report or not 
                  if(found_dot_edit == -1 and found_dot != -1):
                     found_in_with_dot = (text_data.lower()).find((code_package_data[0][found_dot+1:-6]+dot+code_package_data[1]).lower())
                     found_in_without_dot = (text_data.lower()).find((package_name_without_ada_extension+dot+code_package_data[1]).lower())
                     if (found_in_with_dot != -1):
                        found_in_html= found_in_with_dot
                     elif(found_in_without_dot != -1):
                        found_in_html = found_in_without_dot
                  else:
                     found_in_html = (text_data.lower()).find((package_name_without_ada_extension+dot+code_package_data[1]).lower()) 
                  #if procedure is found then update the list with 'used but not exercised'    
                  if (found_in_html !=0 and found_in_html !=-1):
                     modi_but_not_exerci.append([code_package_data[0],code_package_data[1],used_not_exci])
                     metrics_all_columns_csv_data[row_value].append(used_not_exci)
                  #if procedure is not found then update the list with ' not used'       
                  else:
                     modi_but_not_exerci.append([code_package_data[0],code_package_data[1],not_used])  
                     metrics_all_columns_csv_data[row_value].append(not_used)  
               #if procedure is partially exercised then update the list with 'partially exercised'       
               else:
                  modi_but_not_exerci.append([code_package_data[0],code_package_data[1],partially_exci])
            #if procedures is 100% exercised then update list with "100% exercised"      
            else:   
               modi_but_not_exerci.append([code_package_data[0],code_package_data[1],used_and_exci])  
            break   
         row_value +=1
      
      #if procedure not found in csv metrics report then updated 'not found in metrics csv report'           
      if(code_package_data_found == False):
         modi_but_not_exerci.append([code_package_data[0],code_package_data[1],not_in_metri_csv])
   #for code_package_data in new_and_modified_procedures_data:      
#end -------------------------------- code for individual procedures and function to find exercised or not ------------------      
   
#-------------------------------- code for code packages to find used, not used, partially used------------------  
   #get code packages which are zero 0% exercised
   code_packages = list(set(code_packages))
   code_packages_with_zero_exci = [] 
   for code_package in code_packages:
      for aggr_data in metrics_csv_data:
         if((code_package.lower() == aggr_data[0].lower()) and (aggr_data[2] == totals) and (aggr_data[3] == "0%")):
            code_packages_with_zero_exci.append(code_package)
            #if(code_package == aggr_data[0] and aggr_data[2] == totals) and (aggr_data[3] == "0%")):
      #for aggr_data in metrics_csv_data:       
   #for code_package in code_packages:
   
   #check all procedures and function of package used or not
   for code_package in code_packages_with_zero_exci:
      total_fuc_pro=0
      found=0
      for aggr_data in metrics_csv_data:
         if (code_package.lower() == aggr_data[0].lower() and aggr_data[2] != totals):
            total_fuc_pro+=1
            package_name_without_ada_extension=aggr_data[0][:-6]
            found_dot = package_name_without_ada_extension.find(dot)
            found_dot_edit=(package_name_without_ada_extension.lower()).find(dot_edit)
            found_in_html = 0 
            if(found_dot_edit == -1 and found_dot!=-1):
               found_in_with_dot = (text_data.lower()).find((aggr_data[0][found_dot+1:-6]+dot+aggr_data[1]).lower())
               found_in_without_dot = (text_data.lower()).find((package_name_without_ada_extension+dot+aggr_data[1]).lower())
               if (found_in_with_dot != -1):
                  found_in_html= found_in_with_dot
               elif(found_in_without_dot != -1):
                  found_in_html = found_in_without_dot
            else:
               found_in_html = (text_data.lower()).find((package_name_without_ada_extension+dot+aggr_data[1]).lower())     
            if (found_in_html !=0 and found_in_html !=-1):
               found +=1    
      if(total_fuc_pro!=0):
         if (total_fuc_pro == found):
            modi_but_not_exci_for_zero_percent.append([code_package,all_proc_func_used])
         elif(found==0):   
            modi_but_not_exci_for_zero_percent.append([code_package,not_used]) 
         else:
            modi_but_not_exci_for_zero_percent.append([code_package,partially_used]) 
   #for code_package in code_packages_with_zero_exci:
   
#end -------------------------------- code for code packages to find used, not used, partially used------------------  
   
   #append comments of particular code package if TOTALS found in the list.
   for zero_ex_pack in modi_but_not_exci_for_zero_percent:
      row_value=0
      for data in metrics_all_columns_csv_data:
         
         if data[2]== zero_ex_pack[0] and data[3] == "TOTALS" :
            metrics_all_columns_csv_data[row_value].append("  ")
            metrics_all_columns_csv_data[row_value].append(zero_ex_pack[1])
            break
         row_value+=1
   
   print "Writing output data"
   sca_utilities.write_csv_data(modified_but_not_exercised_csv_file_path,modi_but_not_exerci)
   sca_utilities.write_csv_data(metrics_report_csv_file_path,metrics_all_columns_csv_data)
    
#def Is_Procedure_Used(new_and_modified_procedures_csv_file_path,#(Input)   
                   
