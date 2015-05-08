

#FILE NAME: map_a3_entries.py

#AUTHOR: Sudheer Kollapudi



#PURPOSE: this script is used to map the A.3 entries from the previous analysis 
#         (“IFM_Test_Updates.xlsx” spreadsheet (sheets “Set_#4” and “Set_#4_New”)) 
#          to future aggregate reports for IFM SCA run against re-instrumented IFM SW (A.4, C.0, D.0, etc.). 

#         Note:This script is specifically designed to map the data form A3 analysis reports(.xls
#              sheets) to future analysis reports of CH53K program. we can use this script for other programs by doing small
#              script updates.  
          # Script using following columns in provided .csv file(Previous_analysis_csv_file_path)
          #[0,1,2,3,4]
          # 0: Package Name
          # 1: Procedure Number
          # 2: Beginning Report line
          # 3: Ending Report Line
          # 4: Coverage
          #if you want update column IDS for any other programs, just update below code which was present at line no 94.
          
          #prev_anal_data = sca_utilities.get_csv_data(Previous_analysis_csv_file_path,[0,1,2,3,4],True)


import os
import csv
import re
import sca_utilities

code_coverage="Code Coverage for Unit: "
prev_code_package_id=0
prev_proc_Func_id=1
prev_not_cover_code_start_id=2
prev_not_cover_code_end_id=3
coverage_id=4
no_coverage="No Coverage Data Exists"

def Map_Previous_Data_With_New_Aggregate_Report(Previous_aggregate_html_file_path,#(Input)
         new_aggregate_html_file_path,#(Input)
         Previous_analysis_csv_file_path,#(Input)
         mapped_data_csv_file_path,#(Output)
         irregularity_report_csv_file_path):#(Output)

#---------------------------------------------------------------   
#FUNCTIONAL DESCRIPTION:

#PURPOSE: this script is used to map the A.3 entries from the previous analysis 
#         (“IFM_Test_Updates.xlsx” spreadsheet (sheets “Set_#4” and “Set_#4_New”)) 
#         to future aggregate reports for IFM SCA run against re-instrumented IFM SW (A.4, C.0, D.0, etc.).

  
#Previous_aggregate_html_file_path: html file path which contains previous aggregate reports.
#new_aggregate_html_file_path:html file path which contains new aggregate reports.
#Previous_analysis_csv_file_path:which contains previous code analysis.
#mapped_data_csv_file_path:csv file which contains mapped data.
#irregularity_report_csv_file_path: csv file to hold the data if any data not mapped between new and previous aggregate reports.

#LIMITATIONS: None

#NOTES: This script is specifically designed to map the data form A3 analysis reports(.xls
#              sheets) to future analysis reports of CH53K program. we can use this script for other programs by doing small
#              script updates.  
          # Script using following columns in provided .csv file(Previous_analysis_csv_file_path)
          #[0,1,2,3,4]
          # 0: Package Name
          # 1: Procedure Number
          # 2: Beginning Report line
          # 3: Ending Report Line
          # 4: Coverage
          #if you want update column IDS for any other programs, just update below code which was present at line no 82
          
          #prev_anal_data = sca_utilities.get_csv_data(Previous_analysis_csv_file_path,[0,1,2,3,4],True)

# ALGORITHM AND CODE 
#-------------------------------------------------------------------   
   
   #check file type
   sca_utilities.check_file_type(Previous_aggregate_html_file_path,'.html')
   sca_utilities.check_file_type(new_aggregate_html_file_path,'.html')
   sca_utilities.check_file_type(Previous_analysis_csv_file_path,'.csv')
   sca_utilities.check_file_type(mapped_data_csv_file_path,'.csv')
   sca_utilities.check_file_type(irregularity_report_csv_file_path,'.csv')
   
   #to get all packages,function and procedures in aggregate report     
   prev_code_pack_dic=sca_utilities.get_packages_and_procedures_present_in_html_path(Previous_aggregate_html_file_path)
   new_code_pack_dic=sca_utilities.get_packages_and_procedures_present_in_html_path(new_aggregate_html_file_path)
   
   #get extracted data from csv file 
   prev_anal_data = sca_utilities.get_csv_data(Previous_analysis_csv_file_path,[0,1,2,3,4],True)
   
   #convet html data into text data
   prev_aggr_text_data= sca_utilities.convert_html_to_text(Previous_aggregate_html_file_path)
   new_aggr_text_data= sca_utilities.convert_html_to_text(new_aggregate_html_file_path)
   
   #code to map A.3 entries.
   if (len(prev_anal_data)!=0):
      
      #heading for mapped A3 data and irregular data
      map_data=[["Code Package Name","Procedure Name","Original Procedure Number","Original Procedure Line Number",
                 "New Procedure Number","New Procedure Line Number","Code","Coverage"]]
      irre_data=[["Code Package Name","Procedure Name","Original Procedure Number","Original Procedure Line Number",
                 "New Procedure Number","New Procedure Line Number","Code","Coverage",'comment']]
      
      for prev_data in prev_anal_data:
         proc_func_name=""
         new_pro_func_no=0
         #get procedure or function name (from previous aggregate report)
         try:
            proc_func_name = prev_code_pack_dic[prev_data[prev_code_package_id]][int(float(prev_data[prev_proc_Func_id]))-1]
         except:
            #if procedure or function not found store the data into irregular report
            irre_data.append([prev_data[prev_code_package_id],"",prev_data[prev_proc_Func_id],"","","","", 
                              prev_data[coverage_id],"Procedure or package not found in previous agg report"])
         #end try   
         
         #if procedure or function name found in previous aggregate report then get new procedure or function number in new aggregate report
         if(proc_func_name !=""):
            #get new procedure or function number from new aggregate report
            try:
               new_proc_func_arry= new_code_pack_dic[prev_data[prev_code_package_id]]
               new_pro_func_no = new_proc_func_arry.index(proc_func_name)
               new_pro_func_no=new_pro_func_no+1
            except:
               #if procedure or function not found in new aggregate report, store the data into irregular report
               irre_data.append([prev_data[prev_code_package_id],"",prev_data[prev_proc_Func_id],"","","","",
                                 prev_data[coverage_id],"Procedure or package not found in new agg report"])  
         #end if(proc_func_name !=""):
            
         #if new procedure or function is found 
         if (new_pro_func_no != 0):
            #loop for range of lines
            for lines_in in range(int(float(prev_data[prev_not_cover_code_start_id])),int(float(prev_data[prev_not_cover_code_end_id]))+1):
               
               prve_line_data=""
               new_line_data=""
               #get previous line data
               prve_line_data=sca_utilities.Get_Line_Data(prev_aggr_text_data,prev_data[prev_code_package_id],int(float(prev_data[prev_proc_Func_id])),
                                            lines_in)
               #if previous line data found
               if (prve_line_data[0] != ""):
                  
                  #if previous line data found and exercised
                  data_to_search = prve_line_data[0] 
                  if prve_line_data[1]:
                     
                     
                     new_line_data=sca_utilities.Check_Each_Line_Of_Pro_Func(new_aggr_text_data,prev_data[prev_code_package_id],
                                                 proc_func_name,new_pro_func_no,data_to_search)
                     #if new line data found
                     if (new_line_data != "" and new_line_data !=no_coverage):
                        #if new line data found and exercised, then store the data into irregular report
                        if(new_line_data.split()[2]== '*'):
                           irre_data.append([prev_data[prev_code_package_id],proc_func_name,prev_data[prev_proc_Func_id],lines_in,
                                             int(new_line_data.split()[0]),int(new_line_data.split()[1]),str(data_to_search),prev_data[coverage_id],
                                             "specified line exercised in both agg reports"])
                        else:
                           #if new line data found and not exercised, then store the data into mapped report  
                           map_data.append([prev_data[prev_code_package_id],proc_func_name,prev_data[prev_proc_Func_id],lines_in,
                                             int(new_line_data.split()[0]),int(new_line_data.split()[1]),str(data_to_search),prev_data[coverage_id]]) 
                        #end if(new_line_data.split()[2]== '*'):     
                     else:
                        #if new line data not found, then store the data into irregular report
                        irre_data.append([prev_data[prev_code_package_id],proc_func_name,prev_data[prev_proc_Func_id],lines_in,
                                             "","", str(data_to_search),prev_data[coverage_id],"Data not found in New agg"])    
                     #end if (new_line_data != "" and new_line_data !=no_coverage):     
                  else:
                     #if previous line data found and not exercised
                     #check line data matched in new and previous aggregate reports
                     new_line_data=sca_utilities.Check_Each_Line_Of_Pro_Func(new_aggr_text_data,prev_data[prev_code_package_id],
                                                 proc_func_name,new_pro_func_no,data_to_search)
                     #if new line data found
                     if (new_line_data != "" and new_line_data !=no_coverage):
                        #if new line data found and exercised, then store the data into irregular report
                        if(new_line_data.split()[2]== '*'):
                           irre_data.append([prev_data[prev_code_package_id],proc_func_name,prev_data[prev_proc_Func_id],lines_in,
                                             int(new_line_data.split()[0]),int(new_line_data.split()[1]),str(data_to_search) ,prev_data[coverage_id],
                                             "specified line exercised in new agg reports"])
                        else:
                           #if new line data found and not exercised, then store the data into mapped report
                           map_data.append([prev_data[prev_code_package_id],proc_func_name,prev_data[prev_proc_Func_id],lines_in,
                                             int(new_line_data.split()[0]),int(new_line_data.split()[1]),str(data_to_search),prev_data[coverage_id]]) 
                       #end if(new_line_data.split()[2]== '*'):
                     else:
                         #if new line data not found found, then store the data into irregular report
                        irre_data.append([prev_data[prev_code_package_id],proc_func_name,prev_data[prev_proc_Func_id],lines_in,
                                             "","", str(data_to_search),prev_data[coverage_id],"Data not found in New agg"])   
                    #end if (new_line_data != "" and new_line_data !=no_coverage):    
                     
               else:
                  #if previous line data not found, then store the data into irregular report
                  irre_data.append([prev_data[prev_code_package_id],proc_func_name,prev_data[prev_proc_Func_id],lines_in,
                                             "","", "",prev_data[coverage_id],"Data not found in previous agg"])
               #end if (prve_line_data != "" and prve_line_data !=no_coverage):   
            #end for lines_in in range(int(float(prev_data[prev_not_cover_code_start_id]))      
         #end if (new_pro_func_no != 0):
                     
      
      print "writing output"       
      sca_utilities.write_csv_data(mapped_data_csv_file_path,map_data)  
      sca_utilities.write_csv_data(irregularity_report_csv_file_path,irre_data)
      
   #end code to map A.3 entries.  
#end def Map_Previous_Data_With_New_Aggregate_Report(Previous_aggregate_html_file_path,#(Input)  


