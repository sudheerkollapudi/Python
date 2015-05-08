
#FILE NAME: sca_tools.py

#AUTHOR: Sudheer Kollapudi


#PURPOSE: This script is used to create Graphical user interface (GUI) for all tools SCA Tools.



import prep_artifacts
import apex_modified_new_code_packages
import aggregate_modified_but_not_exercised
import map_a3_entries
import ifm_missed_code
import sca_metrics
import previously_exercised_but_now_not
import modify_aggregate_report
import Extract_Excluded_Code
import sca_metrics_old
import check_code_exercised_in_other_apps
import sca_utilities
import consolidate_report

def Run_Sca_Tools():
   
#---------------------------------------------------------------   
#FUNCTIONAL DESCRIPTION:

#PURPOSE:This function is used to create Graphical user interface (GUI) for all tools SCA Tools. 
 
#LIMITATIONS: None

#NOTES: 

# ALGORITHM AND COD

   
   data= """

1.All script inputs needs to be in double quotes.

2.All Windows backslashes '\\' in the path need to be replaced with Forward slashes "/".

3.All output file's path need to be include file name.

4.Specify 'None'(as a string) if you want to assign None value to any argument.
"""   
   #msgbox(msg=data, title="                      ******** NOTE *********", ok_button="OK")   

   msg ="Select the sca tool, which you want to run?"
   title = "CH53K_Sca_Tools"
   choices = ("prep_artifacts", "apex_modified_new_code_packages",
              "aggregate_modified_but_not_exercised","map_a3_entries","sca_metrics",
              "previously_exercised_but_now_not","modify_aggregate_report",
              "-- add_modified_sign","-- extract_excluded_code","check_code_exercised_in_other_apps",
              "consolidate_report")
   #Note: choicebox not yet implemented 
   #choice = choicebox(msg, title, choices)
   
   #print choice
   #if (choice== "prep_artifacts"):
   data=""" Input:
1.provide CH-53K_prep_artifacts.csv file, containing only .2.ada files.

2.provide .CSV file which contains latest version of code packages.

Output:
1.prep_artifacts.py tool will Consolidate multiple entries for the same Artifacts.Filename
 (CH-53K_prep_artifacts.csv) into a single entry.
 
2.Generates a list of code packages that were new and modified for CH-53K that require Apex difference files.

4.Generates ".sh" file for both modified and new code packages .

5.".sh" file contains apex difference commands for or both modified and new code packages .  

Arguments:Consolidate_Prep_Artifacts(prep_artifacts_csv_file_path, #(Input) 
                               prep_artifacts_with_latest_version_csv_file_path,#(Input)
                               consolidate_prep_artifacts_csv_file_path, #(output)
                               apex_difference_commands_sh_file_path,#(output)
                               apex_difference_commands_sh_file_path, #(Input)
                               subsytem_name):  #(Input)).
 
"""   
      #Note: msgbox not yet implemented 
      #msgbox(msg=data, title="prep_artifacts Tool Description", ok_button="OK") 
         
   data="""prep_artifacts_csv_file_path: (input .csv path) file (CH-53K_prep_artifacts.csv) which contains multiple entries of 2.ada.
      
Note: columns should be: peerreviews ids =1, artifacts path=2, artifacts filename=3 ,artifacts version from=4,
     artifacts version final=6,peerreviews status=8.
     
prep_artifacts_with_latest_version_csv_file_path: (input .csv path) which contains latest version of code packages.

consolidate_prep_artifacts_csv_file_path:(output .csv path) file contains new and modified code packages.

apex_difference_commands_sh_file_path: (output .sh path) file contains the difference commands for modified and new code packages.

apex_difference_commands_sh_file_path:(output path) the path where new and modified difference files need to be placed.
Note:don't provide "/" end the end

subsytem_name: should be "ifm"or "fps" or "sm".
"""
      #Note: 'multenterbox' not yet implemented.             
#       values=multenterbox(msg=data,title="Enter Arguments"
#                              , fields=("prep_artifacts_csv_file_path","prep_artifacts_with_latest_version_csv_file_path",
#                                        "consolidate_prep_artifacts_csv_file_path","apex_difference_commands_sh_file_path",
#                                        "apex_difference_commands_sh_file_path","subsytem_name"),values=())
#       if (values[0] != "" and values[1] != "" and values[2] != "" and
#            values[3] != "" and values[4] != "" and values[5] != ""): 
#          prep_artifacts.Consolidate_Prep_Artifacts(values[0],values[1],values[2],
#                                                    values[3],values[4],values[5])
         
           
           
   #elif (choice== "apex_modified_new_code_packages"):
   data=""" Input:
1.provide difference files path (the path where _diff.txt and _new.txt files exists).

Output:
1.Generates a list of procedures and functions that were difference for CH-53K. 

Note:
Run the script for the _new files which don't have add symbol (' +|') on each line. 

Arguments: Get_New_And_Modified_Procedures(new_modified_difference_files_folder_path,#(Input)
         new_modified_procedures_and_functions_csv_file_path):#(output).
"""
      #Note: msgbox not yet implemented 
      #msgbox(msg=data, title="apex_modified_code_packages Tool Description", ok_button="OK")
         
   data="""new_modified_difference_files_folder_path: (input folder path) folder path which contains _diff.txt and _new.txt files. 
Note: don't provide slash at the end
     
new_modified_procedures_and_functions_csv_file_path: (output .csv path) list of procedures and functions that were modified and new for CH-53K.
"""
      #Note: 'multenterbox' not yet implemented.             
#       values=multenterbox(msg=data,title="Enter Arguments"
#                              , fields=("new_modified_difference_files_folder_path","new_modified_procedures_and_functions_csv_file_path"),values=())
#       
#       if (values[0] != "" and values[1] != ""):
#          apex_modified_new_code_packages.Get_New_And_Modified_Procedures(values[0],values[1])
                 
           
   #elif (choice== "aggregate_modified_but_not_exercised"):
   data=""" Input:
1.provide .csv file path, which contains new and modified functions and procedures (output of apex_modified_code_packages ,apex_new_code_packages tools).

2.provide .csv file path,which contains metrics reports for specified aggregate report.

3.provide aggregate report .html file path.

Output:
1.Generates a list of functions and procedures that are Modified but not exercised.

Arguments:Is_Procedure_Used(new_and_modified_procedures_csv_file_path,#(Input)
         metrics_report_csv_file_path,#(Input,output)(this file will be overwrite with new data))
         aggregate_report_html_file_path,#(Input)
         modified_but_not_exercised_csv_file_path): #(Output)
   
"""   #Note: msgbox not yet implemented 
      #msgbox(msg=data, title="aggregate_modified_but_not_exercised Tool Description", ok_button="OK")
         
   data="""new_and_modified_procedures_csv_file_path: (input .csv path) which contains new and modified functions and procedures.
     
metrics_report_csv_file_path: (input .csv path) which contains metrics reports.

aggregate_report_html_file_path: (input .html path) which contains aggregate report.

modified_but_not_exercised_csv_file_path:(output .csv path) which contains list of functions and procedures that are Modified but not exercised.

Note: It will overwrite provided metrics report file.

"""
      #Note: 'multenterbox' not yet implemented.             
#       values=multenterbox(msg=data,title="Enter Arguments"
#                              , fields=("new_and_modified_procedures_csv_file_path","metrics_report_csv_file_path",
#                                        "aggregate_report_html_file_path","modified_but_not_exercised_csv_file_path",),values=())
#       if (values[0] != "" and values[1] != "" and values[2] != "" and values[3] != "" ):
#          aggregate_modified_but_not_exercised.Is_Procedure_Used(values[0],values[1],values[2],values[3])  
         
               
           
   #elif (choice== "map_a3_entries"):
   data=""" Input:
1.provide .html file path, which contains previous aggregate report (A3).

2.provide .html file path,which contains new aggregate report (A4).

3.provide .csv file path, which contains previous analysis (A3) data 
  (use Extract_Excluded_Code.py script to pool all spread sheets data into single .csv file).

Output:
1.Generates a list of mapped A3 entries.  

2.Generates irregularity report (which contains the entries which are not mapped with specific reason). 

Arguments:Map_Previous_Data_With_New_Aggregate_Report(Previous_aggregate_html_file_path,#(Input)
         new_aggregate_html_file_path,#(Input)
         Previous_analysis_csv_file_path,#(Input)
         mapped_data_csv_file_path,#(Output)
         irregularity_report_csv_file_path):#(Output)
"""
      #Note: msgbox not yet implemented    
      #msgbox(msg=data, title="map_a3_entries Tool Description", ok_button="OK")
         
   data="""Previous_aggregate_html_file_path: (input .html path) which contains previous aggregate report (A3).
     
new_aggregate_html_file_path: (input .html path) which contains new aggregate report (A4).

Previous_analysis_csv_file_path: (input .csv path) which contains previous analysis (A3) data.

mapped_data_csv_file_path:(output .csv path) which contains list of mapped A3 entries.

irregularity_report_csv_file_path: (output .csv path) which contains the entries which are not mapped.
"""
      #Note: 'multenterbox' not yet implemented.             
#       values=multenterbox(msg=data,title="Enter Arguments"
#                              , fields=("Previous_aggregate_html_file_path","new_aggregate_html_file_path",
#                                        "Previous_analysis_csv_file_path","mapped_data_csv_file_path",
#                                        "irregularity_report_csv_file_path"),values=())
#       if (values[0] != "" and values[1] != "" and values[2] != "" and values[3] != "" and values[4] != ""):
#          map_a3_entries.Map_Previous_Data_With_New_Aggregate_Report(values[0],values[1],values[2],values[3],values[4])
         
          
           
   #elif (choice== "sca_metrics"):
   data=""" Input:
1.provide .html file path, which contains aggregate report. 

2.provide .csv file path, which contains modified and new code packages at column no 2 (output of prep_artifacts).

3.provide folder path, which contains new and modified difference files (_new.txt,_diff.txt files folder).

4.provide .csv file path which contains extracted excluded code.
  (use Extract_Excluded_Code.py script to pool all spread sheets data into single .csv file)
  
5.provide .csv file path which contains previous anaslysis data

Output:
1.Generates missed coverage report.

2.Generates updated metrics report.

3.Generates excluded code with specific reason

4.Generates log file which contains the code not found in difference files

Arguments:Process_HTML_File(HTML_File, #(Input)
                      New_Modified_File_List,#(Input)
                      Differences_Folder_Path,#(Input)
                      Extracted_Excluded_Code_Csv_File_Path,#(Input)
                      Map_Prev_Data_Csv_File_Path,#(Input)
                      Missed_Coverage_Report_Csv_File_Path,#(Output)
                      Updated_Metrics_Report_Csv_File_Path,#(Output)
                      Excluded_Code_Report_Csv_File_Path,#(Output)
                      Log_Text_File_Path):#(Output)
"""
      #Note: msgbox not yet implemented    
      #msgbox(msg=data, title="sca_metrics Tool Description", ok_button="OK")
         
   data="""HTML_File: (input .html path) which contains aggregate report.
     
New_Modified_File_List: (input .csv path) which contains modified and new code packages at column no 2. 

Differences_Folder:(input folder path) which contains which contains new and modified difference files.

Extracted_Excluded_Code_Csv_File_Path: (input .csv path) which contains the code need to be excluded.

Map_Prev_Data_Csv_File_Path:(input .csv path) contains previous analysis data

Missed_Coverage_Report_Csv_File_Path:(output .csv path) which contains missed coverage report. 

Updated_Metrics_Report_Csv_File_Path:(output .csv path)which contains missed metrics report.

Excluded_Code_Report_Csv_File_Path:(output .csv path) which contains the code which is excluded with specific reason)

Log_Text_File_Path:(output .txt path) which contains the code not found in difference files 

Note:
1. Extracted_Excluded_Code_Csv_Path, Missed_Coverage_Report are optional, so if you are using those arguments please specify 'None'(as a string)

2. Difference folder path requires a trailing forward slash.
"""
      #Note: 'multenterbox' not yet implemented.             
#       values=multenterbox(msg=data,title="Enter Arguments"
#                              , fields=("HTML_File(required)","New_Modified_File_List(required)","Differences_Folder(required)",
#                                        "Extracted_Excluded_Code_Csv_File_Path(optional)","Map_Prev_Data_Csv_File_Path(optional)",
#                                        "Missed_Coverage_Report_Csv_File_Path(required)","Updated_Metrics_Report_Csv_File_Path(required)",
#                                        "Excluded_Code_Report_Csv_File_Path(optional)","Log_Text_File_Path(required)"),values=())
#       
#       if (values[0] != "" and values[1] != "" and values[2] != "" and
#           values[3] != "" and values[4] != "" and values[5] != "" and
#           values[6] != "" and values[7] != "" and values[8] != ""):
#          sca_metrics.Process_HTML_File(values[0],values[1],values[2],values[3],values[4],
#                                        values[5],values[6],values[7],values[8])     
           
           
           
           
   #elif (choice== "previously_exercised_but_now_not"):
   data=""" Input:
1.provide .html file paths (provide previous aggregate reposts and respect head_names in dictionary format)

2.provide .html file path, which contains new aggregate report.

Output:
1.Generates the .csv file which contains the not exercised lines which are previously exercised. 

Arguments:Get_Previously_Exercised_But_Not_Now_Code(previous_aggregate_reports_and_respect_head_names,#(Input) Dictionary
                                             new_aggregate_html_file_path,#(Input)
                                             previously_exercised_but_not_now_csv_file_path):#(Output).
"""
      #Note: msgbox not yet implemented    
      #msgbox(msg=data, title="previously_exercised_but_now_not Tool Description", ok_button="OK")
         
   data="""previous_aggregate_reports_and_respect_head_names: (input .html paths array) which contains aggregate report.
provide previous aggregate reposts and respect head_names in dictionary format
like{"A3-2_csv_file_path":'A3-2',
      "A3-1_csv_file_path":'A3-',
      "A2_csv_file_path":'A2'}      
     
new_aggregate_html_file_path: (input .htm path) which contains new aggregate report.

previously_exercised_but_not_now_csv_file_path:(output .csv path) which contains the not exercised lines which are previously exercised.

"""
      #Note: 'multenterbox' not yet implemented.             
#       values=multenterbox(msg=data,title="Enter Arguments"
#                              , fields=("previous_aggregate_reports_and_respect_head_names","new_aggregate_html_file_path",
#                                        "previously_exercised_but_not_now_csv_file_path"),values=())
#       if (values[0] != "" and values[1] != "" and values[2] != ""):
#          values[0]=eval(values[0])
#          previously_exercised_but_now_not.Get_Previously_Exercised_But_Not_Now_Code(values[0],values[1],values[2])
         
         
         
   #elif (choice== "check_code_exercised_in_other_apps"):
   data=""" Input:
1.provide .html file paths in array, which contains all apps aggregate reports.

2.provide .csv file path, which contains all apps metrics reports.

3.provide apps names ['IFM','FPS','SM']

Output:
1.Generates the .csv file which contains updated coverage report for all common packages.

Arguments: Check_Code_In_Other_Apps(aggregate_reports_html_file_paths,#(Input)
                             metrics_reports_csv_file_path,#(Input)
                             app_names,#(Input)
                             common_covrage_report_csv_file_path):#(output)
"""
      #Note: msgbox not yet implemented    
      #msgbox(msg=data, title="previously_exercised_but_now_not Tool Description", ok_button="OK")
         
   data="""aggregate_reports_html_file_paths: (input .html paths array) which contains aggregate reports (["path1","path2","path3"]).
     
metrics_reports_csv_file_path: (input .csv paths array) which contains metrics reports (["path1","path2","path3"]).

app_names:(input apps names array] pass apps names in array

common_covrage_report_csv_file_path:(output .csv path) which contains updated coverage report for all common packages.

Note:
pass the apps aggregate,metrics reports paths at zero index of array, which you want compare with others.

"""
      #Note: 'multenterbox' not yet implemented.             
#       values=multenterbox(msg=data,title="Enter Arguments"
#                              , fields=("aggregate_reports_html_file_paths","metrics_reports_csv_file_path",
#                                        "app_names","common_covrage_report_csv_file_path"),values=())
#       if (values[0] != "" and values[1] != "" and values[2] != "" and values[3] != ""):
#          values[0]=eval(values[0])
#          values[1]=eval(values[1])
#          values[2]=eval(values[2])
#          check_code_exercised_in_other_apps.Check_Code_In_Other_Apps(values[0],values[1],values[2],values[3])
                
         
                  
   #elif (choice== "modify_aggregate_report"):
   data=""" Input:
1.provide .html file path, which contains aggregate report. 

2.provide .csv file path, which contains modified and new code packages at column no 2 (output of prep_artifacts).

3.provide folder path, which contains new and modified difference files (_new.txt,_diff.txt files folder).

4. provide .csv file path, which contains excluded code 

Output:
Note:
Provided aggregate report would be overwrite with modified aggregate report  if New_Html_File_Path is "None".
New aggregate report will be created if New_Html_File_Path is a file path.

Arguments:Process_HTML_File(HTML_File,#(Input)
                      New_Modified_File_List,#(Input)
                      Differences_Folder,#(Input)
                      Excluded_Code_Cvs_Path,#(Input)
                      New_Html_File_Path):#(Output)
"""
      #Note: msgbox not yet implemented    
      #msgbox(msg=data, title="modify_aggregate_report Tool Description", ok_button="OK")
         
   data="""HTML_File: (input .html path) which contains aggregate report.
     
New_Modified_File_List: (input .csv path)  which contains modified and new code packages.

Differences_Folder:(input folder path) which contains new and modified difference files.

Exluded_Code_Cvs_Path:(input .csv path) which contains excluded code. 

New_Html_File_Path:(output .html path) which contains modified aggregate. 

Note:
1.Provided aggregate report would be overwrite with modified aggregate report  if New_Html_File_Path is "None".

2.New aggregate report will be created if New_Html_File_Path is a file path.

3. Difference folder path requires a trailing forward slash.

"""
      #Note: 'multenterbox' not yet implemented.             
#       values=multenterbox(msg=data,title="Enter Arguments"
#                              , fields=("HTML_File","New_Modified_File_List","Differences_Folder",
#                                        "Excluded_Code_Cvs_Path(optional)" ,"New_Html_File_Path(optional)"),values=())
#       if (values[0] != "" and values[1] != "" and values[2] != ""
#           and values[3] != "" and values[4] != ""):
#          modify_aggregate_report.Process_HTML_File(values[0],values[1],values[2],values[3],values[4])   
         
         
   #elif (choice== "-- add_modified_sign"):
   data=""" Input:
1.provide folder path in which you want add sign inside all files.

2.provide sign that you want to add (ex:" +|").

Output:
Note:
1.All of the '_diff' and '_new' files can be in the same folder.

2.Output would be overwrite all files inside specified folder with specified sign.

Arguments:add_modified_sign(new_files_path,
                             sign):
"""
      #Note: msgbox not yet implemented     
      #msgbox(msg=data, title="add_modified_sign Tool Description", ok_button="OK")
         
   data="""new_files_path: (input folder path) folder path in which you want add sign inside all files.
Note: Don't specify slash '/' at the end.

sign: sign that you want to add (ex:" +|").

Note:

1.All of the '_diff' and '_new' files can be in the same folder.

2.Output would be overwrite all files inside specified folder with specified sign.

"""
      #Note: 'multenterbox' not yet implemented.             
#       values=multenterbox(msg=data,title="Enter Arguments"
#                              , fields=("new_files_path","sign"),values=())
#       if (values[0] != "" and values[1] != "" ):
#          sca_utilities.add_modified_sign(values[0],values[1])
         
   #elif (choice== "-- extract_excluded_code"):
   data="""Note: 
1.save file as .xls format, if file in .xlsx fromat

2.Make sure that "Subprogram Number, Beginning/Ending Report Line" columns shouldn't have multiple entries like(4,6,13 | 4,7,20).

3.Column Id starts with zero.
      
Input:
1.provide the xls files path in one dimensional array ["fullpath-1","fullpath-2"].

2.provide the xls files sheet names in two dimensional array [["Set #4","Set #4_New"],["xxxxx","xxxx"]]. 

3.provide the xls files sheet columns in three dimensional array [[[2,3,4,5,17,18,19],[2,3,4,5,17,18,19]],[[1,2,2],[1,2,2,2]]].

4.provide previous aggregate html path.

5.provide extract_data_with_exclusion_reason as False if script is running to extract the data from previous analysis without standardized exclusion reason.
                                               True if script is running to extract the data with standardized exclusion reason.
 
Output:
1.Generates .csv file by merging all specified xls files data.

Arguments:Extract_Data_From_Xls(xls_files_paths,#(Input) 
         xls_files_sheet_names,#(Input)
         xls_files_sheet_columns,#(Input) 
         extract_data_with_exclusion_reason,#(Input) 
         prev_aggr_html_file_path,#(Input)
         extracted_data_csv_file_path):#(Output)
"""
      #Note: msgbox not yet implemented    
      #msgbox(msg=data, title="extract_excluded_code Tool Description", ok_button="OK")
         
   data="""xls_files_paths: (input array ) the xls files path in one dimensional array ["fullpath-1","fullpath-2"].
     
xls_files_sheet_names: (input array) the xls files sheet names in two dimensional array [["Set #4","Set #4_New"],["xxxxx","xxxx"]].

xls_files_sheet_columns: (input array) the xls files sheet columns in three dimensional array [[[2,3,4,5,17,18,19],[2,3,4,5,17,18,19]],[[1,2,2],[1,2,2,2]]].

extract_data_with_exclusion_reason: True or False.

prev_aggr_html_file_path:(input html path) previous aggregate html path (provide None for when your running for tool no -5).

extracted_data_csv_file_path: (output .csv path).

"""
      #Note: 'multenterbox' not yet implemented.             
#       values=multenterbox(msg=data,title="Enter Arguments"
#                              , fields=("xls_files_paths","xls_files_sheet_names","xls_files_sheet_columns",
#                                        "extract_data_with_exclusion_reason","prev_aggr_html_file_path",
#                                        "extracted_data_csv_file_path"),values=())
#       if (values[0] != "" and values[1] != "" and values[2] != "" and
#           values[3] != "" and values[4] != "" and values[5] != ""):
#           values[0]=eval(values[0])
#           values[1]=eval(values[1])
#           values[2]=eval(values[2])
#           values[3]=eval(values[3])
#           if values[4]== 'None':
#              values[4]=eval(values[4])
#           Extract_Excluded_Code.Extract_Data_From_Xls(values[0],values[1],values[2],
#                                                       values[3],values[4],values[5])
          
   #elif (choice== "consolidate_report"):
   data=""" Input:
1.provide .html file path, which contains new aggregate report. 

2.provide .csv file path, which contains modified and new code packages at column no 2 (output from prep_artifacts).

3.provide folder path, which contains new and modified difference files (_new.txt,_diff.txt files folder).

4.provide .html file paths (array), Which contains previous aggregate reports.

5.provide aggregate report tags (array), previous aggregate report refernce names.

Output:
1.It generates consolidate report for modified and new lines.

Arguments: Process_HTML_File(HTML_File,
                      New_Modified_File_List,
                      Differences_Folder,
                      Excluded_Code_Cvs_File_Path,
                      Prev_Agg_Reports_Html_File_Paths,
                      Agg_Report_Tags,
                      New_Consolidate_Report_Csv_File_Path):
"""
      #Note: msgbox not yet implemented    
      #msgbox(msg=data, title="modify_aggregate_report Tool Description", ok_button="OK")
      
   data="""HTML_File: (input .html path) which contains aggregate report.
     
New_Modified_File_List: (input .csv path)  which contains modified and new code packages.

Differences_Folder:(input folder path) which contains new and modified difference files.

Excluded_Code_Cvs_File_Path:(input .csv path) which contains excluded code. 

Prev_Agg_Reports_Html_File_Paths:(input .html paths in arrya) which contains previous aggregate reports..

Agg_Report_Tags:(input array) which contains previous aggregate report refernce names.

New_Consolidate_Report_Csv_File_Path:(output .csv path) which contains consolidate report for modified and new lines.

"""
      #Note: 'multenterbox' not yet implemented.            
#       values=multenterbox(msg=data,title="Enter Arguments"
#                              , fields=("HTML_File","New_Modified_File_List","Differences_Folder",
#                                        "Excluded_Code_Cvs_File_Path" ,"Prev_Agg_Reports_Html_File_Paths",
#                                        "Agg_Report_Tags",'New_Consolidate_Report_Csv_File_Path'),values=())
#       if (values[0] != "" and values[1] != "" and values[2] != ""
#           and values[3] != "" and values[4] != "" and values[5] != "" and values[6] != ""):
#          values[4]=eval(values[4])
#          values[5]=eval(values[5])
#          consolidate_report.Process_HTML_File(values[0],values[1],values[2],values[3],
#                                               values[4],values[5],values[6])
      
