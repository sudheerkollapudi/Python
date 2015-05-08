

#FILE NAME: modify_aggregate_report.py

#AUTHOR: Sudheer Kollapudi


#PURPOSE: This script is used to mark all new and modified code lines in an aggregate report with following specified symbols,
#         by scanning new and modified difference files  
#         ">>>" if new or modified line of code is exercised
#         "!>>" if new or modified line of code is not exercised
#         "E>>" if new or modified line of code is excluded



import csv
import fileinput
import sys
import re
import sca_utilities
import os
green_col_code='"color:#009900;"'

def Process_HTML_File(HTML_File,#(Input)
                      New_Modified_File_List,#(Input)
                      Differences_Folder,#(Input)
                      Excluded_Code_Cvs_Path,#(Input)
                      New_Html_File_Path):#(Output)
   
#---------------------------------------------------------------   
#FUNCTIONAL DESCRIPTION:

#PURPOSE:This script is used to mark all new and modified code lines in an aggregate report with following specified symbols,
#         by scanning new and modified difference files  
#         ">>>" if new or modified line of code is exercised
#         "!>>" if new or modified line of code is not exercised
#         "E>>" if new or modified line of code is excluded

#HTML_File:containing the aggregate report (the file will be updated with ">>>",(!>>)) 

#New_Modified_File_ListCSV file containing the list of new or modified files in the 2nd column.  

#Differences_Folder: Folder containing the diff files generated from APEX in the format "packagename_diff.txt"

#Excluded_Code_Cvs_Path: he file which contains Excluded code (DEFENSIVE or CODE INSPECTION code)
#            "None" if you don't want to add *>> symbol for Excluded_Code
#
#New_Html_File_Path:specify New_Html_File_Path as "None" if you want to overwrite the provided html path(HTML_File)
#                   else specify the path to create new one. 



#LIMITATIONS: None

#NOTES: None  

# ALGORITHM AND CODE 
   
   #get packages, procedure and function dictionary
   pack_func_dic = sca_utilities.get_packages_and_procedures_present_in_html_path(HTML_File)
   
   #res the Excluded Code from Cvs file if it specified
   if Excluded_Code_Cvs_Path != "None":
      excluded_data=sca_utilities.get_file_data_in_lines(Excluded_Code_Cvs_Path)   
   #if Excluded_Code_Cvs_Path != "None":   
   
   #get all new and modified code packages
   files_modified_list = _Compile_File_List(File = New_Modified_File_List)
   
   html_parser = sca_utilities.MyHTMLParser()
   html_file = open(HTML_File, 'rb')
   
   current_package = ''
   current_procedure = ''
   
   process_package = False
   line=0
   #variables to hold hit and not hit and exclude lines
   hit_lines=[]
   not_hit_lines=[]
   exclude_lines=[]
   
   #loop through each line of the html file
   for row in html_file:
      line+=1
      
      #Reset parser so the data doesn't carry over from line to line
      html_parser.reset_vars()
      
      #Process HTML line
      html_parser.feed(row)
      
      #If this is the start of a new package
      if html_parser.package_name() !='' and html_parser.package_name() != current_package:
      
         current_package = html_parser.package_name()
         #set True if package is found
         if files_modified_list.count(current_package) != 0:
            process_package = True
         else:
            process_package = False
         #end if files_modified_list.count(current_package) != 0: 
           
      #end if html_parser.package_name() !='' and html_parser.package_name() != current_package:     
      
      #only process the html if the file was new or modified
      if process_package:
         
         #get procedure name from dictionary
         if (html_parser.line_not_hit() or html_parser.line_hit()):
            pack_no=html_parser.line_number().split()[0]
            current_procedure=pack_func_dic[current_package][int(pack_no)-1]
            #process the html text to get exact code 
            code = sca_utilities.get_only_code_text(html_parser.line_text())
         #end if (html_parser.line_not_hit() or html_parser.line_hit()):
         
         #If this line was not hit
         if html_parser.line_not_hit():
            #append line if code is excluded
            if (_Is_Code_Excluded (excluded_data,current_package,current_procedure,html_parser.line_number()) and 
                Excluded_Code_Cvs_Path != "None"):
               exclude_lines.append(line)
            #append line if code is not hit   
            elif _Check_For_Line_Data(Differences_Folder, current_package, current_procedure, code):
               not_hit_lines.append(line)
            #end if (_Is_Code_Excluded (excluded_data,current_package,current_procedure,html_parser.line_number()) and    
         
         elif html_parser.line_hit():
            #append line if code is hit   
            #check to see if line was modified for 53k
            if _Check_For_Line_Data(Differences_Folder, current_package, current_procedure, code):
               hit_lines.append(line)
            #end  if _Check_For_Line_Data(Differences_Folder, current_package, current_procedure, code):    
         #end if html_parser.line_not_hit():      
      #end if process_package
   #end for row
   
   html_file.close()
   
   line=0
   #over write the provided html file
   if(New_Html_File_Path == "None"):
      
      #loop for all lines in html
      for line_in in fileinput.input([HTML_File], inplace=True):
         line+=1
         
         #get staring index and end index to insert symbols
         if(line in hit_lines or line in not_hit_lines or line in exclude_lines):
            str_with_out_col=line_in[36:]
            ints=map(int, re.findall(r'\d+', str_with_out_col))
            ints_len=len(str(ints[0])+str(ints[1]))
            if (line_in.find(green_col_code) != -1):
               index_start=((10-ints_len)*6)+1+ints_len+36
            else:  
               index_start=((11-ints_len)*6)+ints_len+36  
            #end if (line_data.find(green_col_code) != -1):    
            index_end=index_start+18
         #end if(line in hit_lines or line in not_hit_lines or line in exclude_lines):   
         #insert symbols
         if line in hit_lines:
            sys.stdout.write(line_in[:index_start]+">>>" + line_in[index_end:])  
         elif line in not_hit_lines:
            sys.stdout.write(line_in[:index_start]+"!>>" + line_in[index_end:])
         elif line in exclude_lines:
            sys.stdout.write(line_in[:index_start]+"E>>" + line_in[index_end:])   
         else:
            sys.stdout.write(line_in)
         #end  if line in hit_lines:   
           
      # for line_in in fileinput.input([HTML_File], inplace=True):
      fileinput.close()
      
   # creat new html file    
   else:
      new_html_data=[]
      html_data=sca_utilities.get_file_data_in_lines(HTML_File)
      
      #loop for all lines in html
      for line_data in html_data:
         line+=1    
         
         ##get staring index and end index to insert symbols
         if(line in hit_lines or line in not_hit_lines or line in exclude_lines):
            str_with_out_col=line_data[36:]
            ints=map(int, re.findall(r'\d+', str_with_out_col))
            ints_len=len(str(ints[0])+str(ints[1]))
            if (line_data.find(green_col_code) != -1):
               index_start=((10-ints_len)*6)+1+ints_len+36
            else:  
               index_start=((11-ints_len)*6)+ints_len+36  
            #end if (line_data.find(green_col_code) != -1):    
            index_end=index_start+18
         ##end if(line in hit_lines or line in not_hit_lines or line in exclude_lines):   
         
         #insert symbols
         if line in hit_lines:
            new_html_data.append(line_data[:index_start]+">>>" + line_data[index_end:]) 
         elif line in not_hit_lines:
            new_html_data.append(line_data[:index_start]+"!>>" + line_data[index_end:])
         elif line in exclude_lines:
            new_html_data.append(line_data[:index_start]+"E>>" + line_data[index_end:])   
         else:
            new_html_data.append(line_data)   
         #end  if line in hit_lines:   
      #end for line_data in html_data: 
           
      #write data into html file   
      new_html_file = open(New_Html_File_Path,"w")
      new_html_file.writelines(new_html_data)
      new_html_file.close()
   #end if(New_Html_File_Path == "None"):   
   
#def Process_HTML_File(HTML_File,      

def _Compile_File_List(File):
   
#---------------------------------------------------------------   
#FUNCTIONAL DESCRIPTION:

#PURPOSE: To get list of code packages in .csv file

#LIMITATIONS: None

#NOTES: None  

# ALGORITHM AND CODE   

   #Setup file for CSV read
   modified_file = open(File, 'rb')
   modified_reader = csv.reader(modified_file)
   
   #initialize list
   file_list = []
   
   #Loop through all of the CSV file
   for row in modified_reader:
      
      #The package name is in the 2nd column
      file_list.append(row[1])
   #end for
   
   modified_file.close()
   
   return file_list

#end def _Compile_File_List

def _Check_For_Line_Data(Diff_Folder, Package, Procedure, Code_Line):
   
#---------------------------------------------------------------   
#FUNCTIONAL DESCRIPTION:

#PURPOSE: Is used to check specified line is modified or not.

#LIMITATIONS: None

#NOTES: None  

# ALGORITHM AND CODE   
   
   modified_for_53k = False
   File = os.path.join(Diff_Folder,Package)
   Diff_File = File[:-6] + "_diff.txt"
   New_File = File[:-6] + "_new.txt"
   diff_data=[]
   #initialize local variables
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
   end_proc_found =False
   out_row=0
   
   while (out_row<len(diff_data)):
      
      temp_proc_name = sca_utilities._Check_For_Proc(diff_data[out_row])
         
      #if this is the procedure the code was found in
      #search for the line
      total_in_rows=0
      if temp_proc_name.lower() == Procedure.lower():
         proc_found = True
         for in_row in range(out_row+1,len(diff_data)):
            if (diff_data[in_row].find("end "+temp_proc_name) !=-1 and diff_data[in_row].find('-|') ==-1):
               end_proc_found = True
               break
            temp_count = diff_data[in_row].replace(" ","").find(Code_Line.replace(" ",""))
            if temp_count != -1:
               if (diff_data[in_row].find('+|') != -1):
                  modified_for_53k = True
                  break
               else:
                  modified_for_53k = False
            total_in_rows=in_row
      if total_in_rows != 0 :
         out_row=total_in_rows
      else:
         out_row +=1      
      if proc_found and end_proc_found:
         break   
            #end if '+|'
         
         #end if temp_count
         
      #end if proc_name == Procedure
         
   #end  while (out_row<len(diff_data)):
   diff_file.close()
   return modified_for_53k
   
#end def _Check_For_Modified_Line

def _Is_Code_Excluded (csv_data,package,procedure,line_number):
   
#---------------------------------------------------------------   
#FUNCTIONAL DESCRIPTION:

#PURPOSE: Is used to check specified line is excluded or not.

#LIMITATIONS: None

#NOTES: None  

# ALGORITHM AND CODE 
   
   insep_defen_not_sup = False
   for data in csv_data:
     
      data=data.split(",")
      #check for given procedure and package 
      if(package.lower()==(data[0].lower()).strip() and
         procedure.lower()==(data[1].lower()).strip() and
         line_number == data[2]):
         insep_defen_not_sup = True
         break
  
   return insep_defen_not_sup
   
#end _Is_Code_Excluded (csv_data,package,procedure,line_number):
