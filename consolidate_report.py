
#FILE NAME: consolidate_report.py

#AUTHOR: Sudheer Kollapudi



#PURPOSE: This script is used to get consolidated report for each and and modified  lines.
#          Output .csv file will be updated with following data
#Subsystem | Package_Name | Procedure_Name | Procedure_No | Instrumented_Code_Line | Code | New or Modified Code Package 
#Code_Exercised? | Standard_Exclusion_Reason | Procedure_Number_in_A3-2_Aggregate_Report | Line_Number_in_A3-2_Aggregate_Report 
#Procedure_Number_in_A3-1_Aggregate_Report | Line_Number_in_A3-1_Aggregate_Report | Procedure_Number_in_A2_Aggregate_Report  
# Line_Number_in_A2_Aggregate_Report



import csv
import sys
import re
import sca_utilities
import os

#class object for package dictionary and data
class get_pack_dic:
   
   def __init__(self):
      self.pack_dic={}
      self.html_data=[]
      
   def get_pack_dic_and_txt_htm_data(self,html_path):   
      self.pack_dic=sca_utilities.get_packages_and_procedures_present_in_html_path(html_path)
      aggr_html_data= sca_utilities.convert_html_to_text(html_path)
      self.html_data=[self.pack_dic,aggr_html_data]
      return self.html_data
   
#end class get_pack_dic:

def Process_HTML_File(HTML_File,#(Input)
                      New_Modified_File_List,#(Input)
                      Differences_Folder,#(Input)
                      Excluded_Code_Cvs_File_Path,#(Input)
                      Prev_Agg_Reports_Html_File_Path,#(Input)
                      Agg_Report_Tags,#(Input)
                      New_Consolidate_Report_Csv_File_Path):#(Output)
   
   
#---------------------------------------------------------------   
#FUNCTIONAL DESCRIPTION:

#PURPOSE:This script is used to get consolidated report for each and and modified  lines.
#          Output .csv file will be updated with following data
#Subsystem | Package_Name | Procedure_Name | Procedure_No | Instrumented_Code_Line | Code | New or Modified Code Package 
#Code_Exercised? | Standard_Exclusion_Reason | Procedure_Number_in_A3-2_Aggregate_Report | Line_Number_in_A3-2_Aggregate_Report 
#Procedure_Number_in_A3-1_Aggregate_Report | Line_Number_in_A3-1_Aggregate_Report | Procedure_Number_in_A2_Aggregate_Report  
# Line_Number_in_A2_Aggregate_Report

#HTML_File: html file which containing the aggregate report.

#New_Modified_File_List: CSV file containing the list of new or modified files in the 2nd column.  

#Differences_Folder_Path: Folder containing the diff files generated from APEX in the format "packagename_diff.txt".

#Excluded_Code_Cvs_File_Path: csv file which contains excluded code.

#Prev_Agg_Reports_Html_File_Path: .html paths (in array) contains previous aggregate report.

#Agg_Report_Tags: contains tag names for previous aggregate report.

#New_Consolidate_Report_Csv_File_Path: csv file which contains consolidate report for new and modified lines

#LIMITATIONS: None

#NOTES: Prev_Agg_Reports_Html_File_Path,Agg_Report_Tags are expected to be parallel lists. 

# ALGORITHM AND CODE 
   
   temp1_head=["Subsystem",'Package_Name','Procedure_Name','Procedure_No',
               'Instrumented_Code_Line','Code','New or Modified Code Package',
               'Code_Exercised?','Standard_Exclusion_Reason']
   #get packages, procedure and function dictionary
   pack_func_dic = sca_utilities.get_packages_and_procedures_present_in_html_path(HTML_File)
   excluded_data=sca_utilities.get_csv_data(Excluded_Code_Cvs_File_Path,[0,1,2,3,4],True)   
   prev_aggs_data = []
   indx=0
   temp2_head=[]
   
   
   for path in Prev_Agg_Reports_Html_File_Path:
      #get dictionary and text of previous aggregate reports
      html=get_pack_dic()
      prev_aggs_data.append(html.get_pack_dic_and_txt_htm_data(path))
      temp2_head.append('Procedure_Number_in_'+Agg_Report_Tags[indx]+'_Aggregate_Report')
      temp2_head.append('Line_Number_in_'+Agg_Report_Tags[indx]+'_Aggregate_Report')
      indx+=1
   #end for path in Prev_Agg_Reports_Html_File_Path:
      
   new_consolidated_sca_data=[]
   new_consolidated_sca_data.append(temp1_head+temp2_head)   
   #get new and modified code packages from csv file 
   files_modified_list_all = sca_utilities._Compile_File_List(File = New_Modified_File_List)
   files_modified_list = []
   for value in files_modified_list_all:
      files_modified_list.append(value[1])
   #end for value in files_modified_list_all:
   
   #create html_parser class object
   html_parser = sca_utilities.MyHTMLParser()
   html_file = open(HTML_File, 'rb')
   
   current_package = ''
   current_procedure = ''
   
   process_package = False
   sub_sys=''
   
   #loop through each line of the html file
   for row in html_file:
      
      #Reset parser so the data doesn't carry over from line to line
      html_parser.reset_vars()
      
      #Process HTML line
      html_parser.feed(row)
      
      #If this is the start of a new package
      if html_parser.package_name() !='' and html_parser.package_name() != current_package:
      
         current_package = html_parser.package_name()
         if files_modified_list.count(current_package) != 0:
            #get subsystem name
            sub_sys=files_modified_list_all[files_modified_list.index(current_package)][0]
            sub_sys=sub_sys[sub_sys.rfind('/')+1:]
            process_package = True
         else:
            process_package = False
         #end if files_modified_list.count(current_package) != 0:
      #end if html_parser.package_name() !='' and html_parser.package_name() != current_package:
              
      #only process the html if the file was new or modified
      if process_package:
         
         #hit lines and not hit lines
         if (html_parser.line_not_hit() or html_parser.line_hit()):
            pack_no=html_parser.line_number().split()[0]
            current_procedure=pack_func_dic[current_package][int(pack_no)-1]
            code = sca_utilities.get_only_code_text(html_parser.line_text())
            
            if html_parser.line_not_hit():
               no_yes='NO'
            elif html_parser.line_hit():
               no_yes='YES'
            #end if html_parser.line_not_hit():
               
            #check line is new and modified line
            line_found=_Check_For_Line_Data(Differences_Folder, current_package, current_procedure, code)
            #if line is new or modified 
            if line_found[0]:
               temp=[]
               temp.append(sub_sys)
               temp.append(current_package)
               temp.append(current_procedure)
               temp.append(html_parser.line_number().split()[0])
               temp.append(html_parser.line_number().split()[1])
               temp.append(code)
               temp.append(line_found[1])
               temp.append(no_yes)
               is_code_excluded = _Is_Code_Excluded (excluded_data,current_package,current_procedure,html_parser.line_number())
               #check code is excluded or not
               if is_code_excluded[0]:
                  temp.append(is_code_excluded[1])
               else:   
                  temp.append(" ") 
               #end  if is_code_excluded[0]:  
               
               #llop for all aggregate repoart 
               for prev_agg_data in prev_aggs_data:
                  #check code exercised in previous aggregate reports
                  found_in_previous=sca_utilities._Check_For_Exci_Or_Not(current_package,current_procedure,code,
                                                       html_parser.line_number().split()[0],html_parser.line_number().split()[1],
                                                       prev_agg_data[0],prev_agg_data[1])
                  temp.append(found_in_previous[0])   
                  temp.append(found_in_previous[1])     
               #end for prev_agg_data in prev_aggs_data:   
                           
               new_consolidated_sca_data.append(temp)    
                 
            #end if line_found[0]:
      #end if process_package
   #end for row
   sca_utilities.write_csv_data(New_Consolidate_Report_Csv_File_Path,new_consolidated_sca_data)
   
   html_file.close()
#end def Process_HTML_File(HTML_File,#(Input)   


def _Check_For_Line_Data(Diff_Folder, Package, Procedure, Code):
   
#FUNCTIONAL DESCRIPTION:

#PURPOSE: to check the given line modified or new 

#LIMITATIONS: None

#NOTES: None  

# ALGORITHM AND CODE       
   
   
   modified_for_53k = [False]
   
   #update Diff_File,New_File 
   File = os.path.join(Diff_Folder,Package)
   Diff_File = File[:-6] + "_diff.txt"
   New_File = File[:-6] + "_new.txt"
   diff_data=[]
   
   #initialize local variables
   #get file data
   try:
      diff_file = open(Diff_File, 'rb')
      diff_data=diff_file.readlines()
      new_modi="Modified"
   except:
      try:
         diff_file = open(New_File, 'rb')
         diff_data=diff_file.readlines()
         new_modi="New"
      except:
         print "Unable to find " + Diff_File
         return True
      #end  try:
   #end  try:
      
   proc_found = False
   end_proc_found =False
   out_row=0
   
   #loop for each line
   while (out_row<len(diff_data)):
      
      temp_proc_name = sca_utilities._Check_For_Proc(diff_data[out_row])
         
      #if this is the procedure the code was found in
      #search for the line
      total_in_rows=0
      if temp_proc_name.lower() == Procedure.lower():
         proc_found = True
         for in_row in range(out_row+1,len(diff_data)):
            #check end of procedure
            if (diff_data[in_row].find("end "+temp_proc_name) !=-1 and diff_data[in_row].find('-|') ==-1):
               end_proc_found = True
               break
            #end if (diff_data[in_row].find("end "+temp_proc_name) !=-1 and diff_data[in_row].find('-|') ==-1):
            
            temp_count = diff_data[in_row].replace(" ","").find(Code.replace(" ",""))
            #check line is modified or not
            if temp_count != -1:
               if (diff_data[in_row].find('+|') != -1):
                  modified_for_53k = [True,new_modi]
                  break
               else:
                  modified_for_53k = [False,new_modi]
               #end if (diff_data[in_row].find('+|') != -1):
                  
            #end if temp_count != -1:      
            total_in_rows=in_row
         #end for in_row in range(out_row+1,len(diff_data)):  
      #end if temp_proc_name.lower() == Procedure.lower():
         
      #update the line no      
      if total_in_rows != 0 :
         out_row=total_in_rows
      else:
         out_row +=1    
      #end if total_in_rows != 0 :   
      #break the loop if end of procedure found
      if proc_found and end_proc_found:
         break   
      #end if proc_found and end_proc_found:ure
         
   #end  while (out_row<len(diff_data)):
   
   diff_file.close()
   return modified_for_53k
   
#end def _Check_For_Line_Data(Diff_Folder, Package, Procedure, Code):
      

def _Is_Code_Excluded (csv_data,package,procedure,line_number):
   
#FUNCTIONAL DESCRIPTION:

#PURPOSE: To check code exclude or not 

#LIMITATIONS: None

#NOTES: None  

# ALGORITHM AND CODE       
   
   insep_defen_not_sup = [False]
   for data in csv_data:
      #if data found return exluded reason.
      if(package.lower()==(data[0].lower()).strip() and
         procedure.lower()==(data[1].lower()).strip() and
         line_number == data[2]):
         insep_defen_not_sup = [True,data[4].replace("\n",'').strip()]
         break
      #end if(package.lower()==(data[0].lower()).strip() and
   #end for data in csv_data:
      
   return insep_defen_not_sup
   
#end def _Is_Code_Inspection_Defensive_Not_Supported  
