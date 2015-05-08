

#FILE NAME: sca_metrics.py

#AUTHOR: Sudheer Kollapudi



#PURPOSE: The purpose of this file is to calculate
#             modified code coverage by excluding the exclude code.


import csv
import sca_utilities
import os

#Defines keywords for defensive code
DEFENSIVE_KEY_WORDS = ['Error.Log',
                       'Err.Log',
                       'Text_Io_Api',
                       'null;']

map_code_package_id=0
map_proc_Func_id=1
map_line_id=3
map_code_id=4
csv_map_data=""
log_data=""



#####################
# Process_HTML_File
#####################
def Process_HTML_File(HTML_File, #(Input)
                      New_Modified_File_List,#(Input)
                      Differences_Folder_Path,#(Input)
                      Extracted_Excluded_Code_Csv_File_Path,#(Input)
                      Map_Prev_Data_Csv_File_Path,#(Input)
                      Missed_Coverage_Report_Csv_File_Path,#(Output)
                      Updated_Metrics_Report_Csv_File_Path,#(Output)
                      Excluded_Code_Report_Csv_File_Path,#(Output)
                      Log_Text_File_Path):#(Output)
   
#---------------------------------------------------------------   
#FUNCTIONAL DESCRIPTION:

#PURPOSE:The purpose of this file is to calculate
#             modified code coverage by excluding the exclude code.


#HTML_File: html file which containing the aggregate report.

#New_Modified_File_List: CSV file containing the list of new or modified files in the 2nd column.  

#Differences_Folder_Path: Folder containing the diff files generated from APEX in the format "packagename_diff.txt".

#Extracted_Excluded_Code_Csv_File_Path: csv file which contains excluded code.

#Map_Prev_Data_Csv_File_Path: csv file contains previous analysis data (which is mapped new aggregate report).

#Missed_Coverage_Report_Csv_File_Path: csv file contains coverage modified and new lines which are not exercised. 

#Updated_Metrics_Report_Csv_File_Path: csv file contains metrics report after excluding code.

#Excluded_Code_Report_Csv_File_Path: csv file contains excluded code with specific reason(why code was excluded)

#Log_Text_File_Path:code which is not found in differnce file.

#LIMITATIONS: None

#NOTES: Pass None for following arguments if Extracted_Excluded_Code_Csv_File_Path  not specified
#        1.Extracted_Excluded_Code_Csv_File_Path = None
#        2.Excluded_Code_Report_Csv_File_Path= None 

# ALGORITHM AND CODE 

   
   #get data form Map_Prev_Data_Csv_File_Path csv file 
   csv_map_data =sca_utilities.get_csv_data(Map_Prev_Data_Csv_File_Path,[0,1,2,3],True)
   extracted_excluded_code = sca_utilities.get_csv_data(Extracted_Excluded_Code_Csv_File_Path,[0,1,2,3,4,5],True)
   
   #get packages, procedure and function dictionary
   pack_func_dic = sca_utilities.get_packages_and_procedures_present_in_html_path(HTML_File)
   
   #get all new and modified code packages 
   files_modified_list_all = sca_utilities._Compile_File_List(File = New_Modified_File_List)
   files_modified_list = []
   for value in files_modified_list_all:
      files_modified_list.append(value[1])
   #end for value in files_modified_list_all:   
   
   # Access MyHTMLParser class
   html_parser = sca_utilities.MyHTMLParser()
   #open html file
   html_file = open(HTML_File, 'rb')
   
   current_package = ''
   current_procedure = ''
   missed_list = [['Subsystem','Package Name','Procedure Name', 'Instrumented Code Line','Code']]
   metrics_list = [['Subsystem','Package Name', 'Lines Covered', 'Lines Instrumented']]
   if(Extracted_Excluded_Code_Csv_File_Path != "None"):
      missed_list = [['Subsystem','Package Name','Procedure Name', 'Instrumented Code Line','Code','Should be exercised']]
      excluded_code_list=[['Package Name', 'Procedure Name', 'Excluded Code Line','Code',"Standardized Reason","Exercised or Not"]]
   
   
   print 'Analysis in Progress ',
   count = 0
   instrumented = 0
   covered = 0
   process_package = False
   sub_sys=""
   #loop through each line of the html file
   for row in html_file:
      #Reset parser so the data doesn't carry over from line to line
      html_parser.reset_vars()
      
      #Process HTML line
      html_parser.feed(row)
         
      #If this is the start of a new package
      if html_parser.package_name() !='' and html_parser.package_name() != current_package:
      
         #store off data for previous package
         if process_package:
            temp_list = []
            temp_list.append(sub_sys)
            temp_list.append(current_package)
            temp_list.append(covered)
            temp_list.append(instrumented)
            metrics_list.append(temp_list)
            covered = 0
            instrumented = 0
         #end  if process_package:
         current_package = html_parser.package_name()
         
         if files_modified_list.count(current_package) != 0:
            #get the subsystem 
            sub_sys=files_modified_list_all[files_modified_list.index(current_package)][0]
            sub_sys=sub_sys[sub_sys.rfind('/')+1:]
            process_package = True
         else:
            process_package = False
         
        #end if files_modified_list.count(current_package) != 0:
      #end if html_parser.package_name() !='' and html_parser.package_name() != current_package:
      
      #only process the html if the file was new or modified
      if process_package:
         
         #get current_procedure for hit and not hit lines
         if (html_parser.line_not_hit() or html_parser.line_hit()):
            pack_no=html_parser.line_number().split()[0]
            current_procedure=pack_func_dic[current_package][int(pack_no)-1]
            code = sca_utilities.get_only_code_text(html_parser.line_text())
         #end  if (html_parser.line_not_hit() or html_parser.line_hit()):
            
         #If this line was not hit
         if html_parser.line_not_hit():  
            
            #check to see if it is defensive code
            if _Is_Code_Defensive(html_parser.line_text()):
               
               if(Extracted_Excluded_Code_Csv_File_Path != "None"):
                  excluded_code_list.append([current_package,current_procedure,html_parser.line_number(),code,"DEFENSIVE KEY WORDS",'NO'])
               #end if(Extracted_Excluded_Code_Csv_File_Path != "None"):   
            elif(Extracted_Excluded_Code_Csv_File_Path != "None"):
               #check line is excluded or not 
               is_insep_defen_not_sup = _Is_Code_Inspection_Defensive_Not_Supported(extracted_excluded_code,current_package,
                                                                                    current_procedure,html_parser.line_number(),code)
               if is_insep_defen_not_sup[0]:
                  excluded_code_list.append([current_package,current_procedure,html_parser.line_number(),code,is_insep_defen_not_sup[1],'NO'])
                  
                  #check to see if line was modified for 53k
               elif _Check_For_Modified_Line(Differences_Folder_Path, current_package, current_procedure, code,html_parser.line_number()):
                  temp_list = []
                  temp_list.append(sub_sys)
                  temp_list.append(current_package)
                  temp_list.append(current_procedure)
                  temp_list.append(html_parser.line_number())
                  temp_list.append(html_parser.line_text().replace("\n",""))
                  #check the line in missed code
                  if (_missed_code(temp_list)and Map_Prev_Data_Csv_File_Path != None):
                     temp_list.append("yes")
                  #end if (_missed_code(temp_list)and Map_Prev_Data_Csv_File_Path != None):   
                  missed_list.append(temp_list)
                  instrumented += 1
               #end if  if is_insep_defen_not_sup[0]:   
            #end elif(Extracted_Excluded_Code_Csv_File_Path != "None"):      
               
            else:
               #check to see if line was modified for 53k
               if _Check_For_Modified_Line(Differences_Folder_Path, current_package, current_procedure, code,html_parser.line_number()):
                  temp_list = []
                  temp_list.append(sub_sys)
                  temp_list.append(current_package)
                  temp_list.append(current_procedure)
                  temp_list.append(html_parser.line_number())
                  temp_list.append(html_parser.line_text().replace("\n",""))
                  if (_missed_code(temp_list)and Map_Prev_Data_Csv_File_Path != None):
                     temp_list.append("yes")
                  missed_list.append(temp_list)
                  instrumented += 1
         
         elif html_parser.line_hit():
            #check to see if line was modified for 53k
            if _Check_For_Modified_Line(Differences_Folder_Path, current_package, current_procedure, code,html_parser.line_number()):
               ##check to see if it is defensive code
               if _Is_Code_Defensive(html_parser.line_text()):
                  if(Extracted_Excluded_Code_Csv_File_Path != "None"):
                     excluded_code_list.append([current_package,current_procedure,html_parser.line_number(),code,"DEFENSIVE KEY WORDS",'YES'])
                  #end if(Extracted_Excluded_Code_Csv_File_Path != "None"):   
               elif(Extracted_Excluded_Code_Csv_File_Path != "None"):
                  is_insep_defen_not_sup = _Is_Code_Inspection_Defensive_Not_Supported(extracted_excluded_code,current_package,
                                                                                    current_procedure,html_parser.line_number(),code)
                  if is_insep_defen_not_sup[0]:
                     excluded_code_list.append([current_package,current_procedure,html_parser.line_number(),code,is_insep_defen_not_sup[1],'YES'])
                  #end if is_insep_defen_not_sup[0]:   
               #end if _Is_Code_Defensive(html_parser.line_text()):      
               covered += 1
               instrumented +=1
            #end if _Check_For_Modified_Line(Differences_Folder_Path, current_package, current_procedure, code,html_parser.line_number()):
         #end if html_parser.line_not_hit():  
            
      #end if process_package
         
      #Display in progress Text
      count += 1
      if count >= 10:
         print '.',
         count = 0  
   #end for row
   
   #store off data for previous package
   if process_package:
      temp_list = []
      temp_list.append(sub_sys)
      temp_list.append(current_package)
      temp_list.append(covered)
      temp_list.append(instrumented)
      metrics_list.append(temp_list)
      covered = 0
      instrumented = 0
   html_file.close()  
   
   print 'Write output'
   #Record Results in file
   sca_utilities.write_csv_data(Missed_Coverage_Report_Csv_File_Path,missed_list)
   sca_utilities.write_csv_data(Updated_Metrics_Report_Csv_File_Path,metrics_list)
   
   text_file=open(Log_Text_File_Path,"wb")
   text_file.write(log_data)
   text_file.close()
   
   if (Extracted_Excluded_Code_Csv_File_Path != "None"):
      sca_utilities.write_csv_data(Excluded_Code_Report_Csv_File_Path,excluded_code_list)
   #end if (Extracted_Excluded_Code_Csv_File_Path != "None"):  
   
####################
#_Is_Code_Defensive
####################
def _Is_Code_Defensive(Line_Of_Code):
#---------------------------------------------------------------   
#FUNCTIONAL DESCRIPTION:

#PURPOSE: to check the line contains DEFENSIVE_KEY_WORDS or not

#LIMITATIONS: None

#NOTES: None  

# ALGORITHM AND CODE      

   defensive = False
   for keyword in DEFENSIVE_KEY_WORDS:
      if Line_Of_Code.find(keyword) != -1:
         defensive = True
         break
      #end if
   #end for
   
   return defensive

#end def _Is_Code_Defensive

###########################
#_Check_For_Modified_Line
###########################

def _Check_For_Modified_Line(Diff_Folder, Package, Procedure, Code_Line,line_no):
   
#FUNCTIONAL DESCRIPTION:

#PURPOSE: to check the given line modified or new 

#LIMITATIONS: None

#NOTES: None  

# ALGORITHM AND CODE     

   global log_data
   
   #initialize local variables
   modified_for_53k = True

   File = os.path.join(Diff_Folder,Package)
   Diff_File = File[:-6] + "_diff.txt"
   New_File = File[:-6] + "_new.txt"
   diff_data=[]

   try:
      diff_file = open(Diff_File, 'rb')
      diff_data=diff_file.readlines()
   except:
      try:
         diff_file = open(New_File, 'rb')
         diff_data=diff_file.readlines()
      except:
         print "Unable to find " + Diff_File
         return True
      
   proc_found = False
   data_found=False
   end_proc_found=False
   out_row=0
   
   #loop for each line of new or modified file
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
            #end  if (diff_data[in_row].find("end "+temp_proc_name) !=-1 and diff_data[in_row].find('-|') ==-1):
            
            temp_count = diff_data[in_row].replace(" ","").find(Code_Line.replace(" ",""))
            
            #check line is found or not
            if temp_count != -1:
               data_found=True
               
               #check line is modified or not
               if diff_data[in_row].find('+|') != -1:
                  modified_for_53k = True
                  break
               else:
                  modified_for_53k = False
               #end if diff_data[in_row].find('+|') != -1:   
               
            #end if temp_count != -1:      
            total_in_rows=in_row
            
      #update line no       
      if total_in_rows != 0 :
         out_row=total_in_rows
      else:
         out_row +=1  
      #end  if total_in_rows != 0 :  
      
      #break the loop if end of procedure found
      if proc_found and end_proc_found:
         break
      #end if proc_found and end_proc_found:
         
         #end if temp_count
         
      #end if proc_name == Procedure
         
   #end for row

      
   #end for row
   #write data if log file found
   if data_found == False:
      log_data += Package+"   "+"   "+str(line_no)+"   "+Procedure+"   "+Code_Line+"\n"
   
   diff_file.close()
   
   return modified_for_53k
   
#end def _Check_For_Modified_Line

def _Is_Code_Inspection_Defensive_Not_Supported (extracted_excluded_code,package,procedure,line_number,line_text):
   
#FUNCTIONAL DESCRIPTION:

#PURPOSE: to check the given line is excluded or not 

#LIMITATIONS: None

#NOTES: None  

# ALGORITHM AND CODE    
   
   insep_defen_not_sup = [False]
   
   #loop for each vale in extracted_excluded_code
   for data in extracted_excluded_code: 
      
      #check the specified line found or not
      if(package.lower()==(data[0].lower()).strip() and
         procedure.lower()==(data[1].lower()).strip() and
         line_number.split()[1]== data[3] and 
         ((line_text.lower()).replace(" ","")).replace("\n","") == (data[4].lower()).replace(" ","") ):
         insep_defen_not_sup = [True,data[5]]
         break
      #end if(package.lower()==(data[0].lower()).strip() and
      
   #end  for data in extracted_excluded_code: 
   
   return insep_defen_not_sup
   
#end def _Is_Code_Inspection_Defensive_Not_Supported  

def _missed_code (miss_cover_data):

#FUNCTIONAL DESCRIPTION:

#PURPOSE: to check the given line is missed code or not 

#LIMITATIONS: None

#NOTES: None  

# ALGORITHM AND CODE   
   
   match=False
   for row in csv_map_data:
      #check the specified line found or not
      if (((row[map_code_package_id].replace(" ","")).lower() == (miss_cover_data[0].replace(" ","")).lower())and
          ((row[map_proc_Func_id].replace(" ","")).lower() == (miss_cover_data[1].replace(" ","")).lower()) and
          (row[map_line_id] == miss_cover_data[2].split()[1]) and 
          ((row[map_code_id].replace(" ","")).lower() == (miss_cover_data[3].replace(" ","")).lower())):
         match=True
         break   
      #end if (((row[map_code_package_id].replace(" ","")).lower() == (miss_cover_data[0].replace(" ","")).lower())and  
       
   #end  for row in csv_map_data:   
   return match

#end _missed_code
