

#FILE NAME: input_data.py

#AUTHOR: Sudheer Kollapudi


#PURPOSE: This script contains Input and output  file paths for all SCA TOOLS.



class Arguments:
   
   #Arguments for apex_modified_new_code_packages.py sca tool
   def _apex_modified_new_code_packages(self):
      self.new_modified_difference_files_folder_path= r'C:\rw_apps\ch53k_sca\reports\IFM\A4_Testing_Reports\03_20_2015\sca_tools_inputs\new_diff_files'
      self.new_modified_procedures_and_functions_csv_file_path=r'C:\rw_apps\ch53k_sca\reports\IFM\A4_Testing_Reports\03_20_2015\sca_tools_outputs/IFM_New_And_Modified_Procedures.csv'
      return [self.new_modified_difference_files_folder_path,self.new_modified_procedures_and_functions_csv_file_path]
   
   
   #Arguments for aggregate_modified_but_not_exercised.py sca tool
   def _aggregate_modified_but_not_exercised(self):
      self.new_and_modified_procedures_csv_file_path= r'C:\rw_apps\ch53k_sca\reports\IFM\A4_Testing_Reports\03_20_2015\sca_tools_outputs/IFM_New_And_Modified_Procedures.csv'
      self.metrics_report_csv_file_path=r'C:\rw_apps\ch53k_sca\reports\IFM\A4_Testing_Reports\03_20_2015\sca_tools_outputs/ifm_a4_metrics_report_3_20_2015.csv'
      self.aggregate_report_html_file_path=r'C:\rw_apps\ch53k_sca\reports\IFM\A4_Testing_Reports\03_20_2015\sca_tools_inputs/ifm_a4_aggregate_report_3_20_2015.html'
      self.modified_but_not_exercised_csv_file_path=r'C:\rw_apps\ch53k_sca\reports\IFM\A4_Testing_Reports\03_20_2015\sca_tools_outputs/IFM_Modified_But_Not_Exercised_Procedures.csv'
      return [ self.new_and_modified_procedures_csv_file_path,
               self.metrics_report_csv_file_path,
               self.aggregate_report_html_file_path,
               self.modified_but_not_exercised_csv_file_path]
      
    
   #Arguments for Extract_Excluded_Code.py sca tool (to map the data)
   def _extract_excluded_code_1(self):
      self.xls_files_paths= [r'C:\rw_apps\ch53k_sca\reports\IFM\A4_Testing_Reports\03_20_2015\sca_tools_inputs/IFM_Test_Updates.xls']
      self.xls_files_sheet_names=[['Set #4', 'Set #4_New']]
      self.xls_files_sheet_columns=[[[2,3,4,5,17,18,19],[2,3,4,5,17,18,19]]]
      self.extract_data_with_exclusion_reason=False
      self.prev_aggr_html_file_path=None
      self.extracted_data_csv_file_path=r'C:\rw_apps\ch53k_sca\reports\IFM\A4_Testing_Reports\03_20_2015\sca_tools_outputs/IFM_Extracted_Data_For_Map_Data_Tool.csv'
      return [ self.xls_files_paths,
               self.xls_files_sheet_names,
               self.xls_files_sheet_columns,
               self.extract_data_with_exclusion_reason,
               self.prev_aggr_html_file_path,
               self.extracted_data_csv_file_path] 
      
   #Arguments for Extract_Excluded_Code.py sca tool (with Exclusion Reason)
   def _extract_excluded_code_2(self):
      self.xls_files_paths= [r'C:\rw_apps\ch53k_sca\reports\IFM\A4_Testing_Reports\03_20_2015\sca_tools_inputs/IFM_Test_Updates.xls',
                             r'C:\rw_apps\ch53k_sca\reports\IFM\A4_Testing_Reports\03_20_2015\sca_tools_inputs/IFM_Test_Cases.xls']
      self.xls_files_sheet_names=[['Set #4','Set #4_New'],['Code New for CH53K','Code Modified for CH53K']]
      self.xls_files_sheet_columns=[[[2,3,4,5,17,18,19],[2,3,4,5,17,18,19]],[[1,3,4,5,8,9,11,14],[1,3,4,5,8,9,11,14]]]
      self.extract_data_with_exclusion_reason=True
      self.prev_aggr_html_file_path=r'C:\rw_apps\ch53k_sca\reports\IFM\A3_2_Testing_Reports/ifm_aggregate_report.html'
      self.extracted_data_csv_file_path=r'C:\rw_apps\ch53k_sca\reports\IFM\A4_Testing_Reports\03_20_2015\sca_tools_outputs/IFM_Extracted_Data_With_Exclusion_Reason.csv'
      return [ self.xls_files_paths,
               self.xls_files_sheet_names,
               self.xls_files_sheet_columns,
               self.extract_data_with_exclusion_reason,
               self.prev_aggr_html_file_path,
               self.extracted_data_csv_file_path]     
      
      
      
   #Arguments for map_a3_entries.py sca tool
   def _map_a3_entries(self):
      self.Previous_aggregate_html_file_path= r'C:\rw_apps\ch53k_sca\reports\IFM\A3_2_Testing_Reports/ifm_aggregate_report.html'
      self.new_aggregate_html_file_path=r'C:\rw_apps\ch53k_sca\reports\IFM\A4_Testing_Reports\03_20_2015\sca_tools_inputs/ifm_a4_aggregate_report_3_20_2015.html'
      self.Previous_analysis_csv_file_path=r'C:\rw_apps\ch53k_sca\reports\IFM\A4_Testing_Reports\03_20_2015\sca_tools_outputs/IFM_Extracted_Data_For_Map_Data_Tool.csv'
      self.mapped_data_csv_file_path=r'C:\rw_apps\ch53k_sca\reports\IFM\A4_Testing_Reports\03_20_2015\sca_tools_outputs/IFM_Mapped_Data.csv'
      self.irregularity_report_csv_file_path=r'C:\rw_apps\ch53k_sca\reports\IFM\A4_Testing_Reports\03_20_2015\sca_tools_outputs/IFM_Irregular_Data.csv'
      return [ self.Previous_aggregate_html_file_path,
               self.new_aggregate_html_file_path,
               self.Previous_analysis_csv_file_path,
               self.mapped_data_csv_file_path,
               self.irregularity_report_csv_file_path]      
      
      
      
   #Arguments for sca_metrics.py sca tool
   def _sca_metrics(self):
      self.HTML_File= r'C:\rw_apps\ch53k_sca\reports\IFM\A4_Testing_Reports\03_20_2015\sca_tools_inputs/ifm_a4_aggregate_report_3_20_2015.html'
      self.New_Modified_File_List=r'C:\rw_apps\ch53k_sca\reports\IFM\A4_Testing_Reports\03_20_2015\sca_tools_inputs/IFM_artifacts_03_18_2015.csv'
      self.Differences_Folder_Path=r'C:\rw_apps\ch53k_sca\reports\IFM\A4_Testing_Reports\03_20_2015\sca_tools_inputs\new_diff_files_with_sign'
      self.Extracted_Excluded_Code_Csv_File_Path=r'C:\rw_apps\ch53k_sca\reports\IFM\A4_Testing_Reports\03_20_2015\sca_tools_outputs/IFM_Extracted_Data_With_Exclusion_Reason.csv'
      self.Map_Prev_Data_Csv_File_Path=r'C:\rw_apps\ch53k_sca\reports\IFM\A4_Testing_Reports\03_20_2015\sca_tools_outputs/IFM_Mapped_Data.csv'
      self.Missed_Coverage_Report_Csv_File_Path=r'C:\rw_apps\ch53k_sca\reports\IFM\A4_Testing_Reports\03_20_2015\sca_tools_outputs/IFM_Missed_Coverage.csv'
      self.Updated_Metrics_Report_Csv_File_Path=r'C:\rw_apps\ch53k_sca\reports\IFM\A4_Testing_Reports\03_20_2015\sca_tools_outputs/IFM_Updated_Metrics.csv'
      self.Excluded_Code_Report_Csv_File_Path=r'C:\rw_apps\ch53k_sca\reports\IFM\A4_Testing_Reports\03_20_2015\sca_tools_outputs/IFM_Excluded_Code.csv'
      self.Log_Text_File_Path=r'C:\rw_apps\ch53k_sca\reports\IFM\A4_Testing_Reports\03_20_2015\sca_tools_outputs/IFM_Log_File.txt'
      return [ self.HTML_File,
               self.New_Modified_File_List,
               self.Differences_Folder_Path,
               self.Extracted_Excluded_Code_Csv_File_Path,
               self.Map_Prev_Data_Csv_File_Path,
               self.Missed_Coverage_Report_Csv_File_Path,
               self.Updated_Metrics_Report_Csv_File_Path,
               self.Excluded_Code_Report_Csv_File_Path,
               self.Log_Text_File_Path]    
      
   #Arguments for previously_exercised_but_now_not.py sca tool
   def _previously_exercised_but_now_not(self):
      self.previous_aggregate_reports_and_respect_head_names= {r'C:\rw_apps\ch53k_sca\reports\IFM\A3_2_Testing_Reports/ifm_aggregate_report.html':'A3-2',
                                                               r'C:\rw_apps\ch53k_sca\reports\IFM\A3_1_Testing_Reports/ifm_round2_aggregate_report.html':'A3-1',
                                                               r'C:\rw_apps\ch53k_sca\reports\IFM\A2_Testing_Reports/ifm_aggregate_report.html':'A2'}
      self.new_aggregate_html_file_path=r'C:\rw_apps\ch53k_sca\reports\IFM\A4_Testing_Reports\03_20_2015\sca_tools_inputs/ifm_a4_aggregate_report_3_20_2015.html'
      self.previously_exercised_but_not_now_csv_file_path=r'C:\rw_apps\ch53k_sca\reports\IFM\A4_Testing_Reports\03_20_2015\sca_tools_outputs/IFM_Previously_Exercised_But_Not_Now.csv'
      return [ self.previous_aggregate_reports_and_respect_head_names,
               self.new_aggregate_html_file_path,
               self.previously_exercised_but_not_now_csv_file_path]    
      
      
     
   #Arguments for modify_aggregate_report.py sca tool
   def _modify_aggregate_report(self):
      self.HTML_File= r'C:\rw_apps\ch53k_sca\reports\IFM\A4_Testing_Reports\03_20_2015\sca_tools_inputs/ifm_a4_aggregate_report_3_20_2015.html'
      self.New_Modified_File_List=r'C:\rw_apps\ch53k_sca\reports\IFM\A4_Testing_Reports\03_20_2015\sca_tools_inputs/IFM_artifacts_03_18_2015.csv'
      self.Differences_Folder_Path=r'C:\rw_apps\ch53k_sca\reports\IFM\A4_Testing_Reports\03_20_2015\sca_tools_inputs\new_diff_files_with_sign'
      self.Excluded_Code_Cvs_Path=r'C:\rw_apps\ch53k_sca\reports\IFM\A4_Testing_Reports\03_20_2015\sca_tools_outputs/IFM_Excluded_Code.csv'
      self.New_Html_File_Path=r'C:\rw_apps\ch53k_sca\reports\IFM\A4_Testing_Reports\03_20_2015\sca_tools_outputs/Modified_ifm_a4_aggregate_report_3_20_2015.html'
      return [ self.HTML_File,
               self.New_Modified_File_List,
               self.Differences_Folder_Path,
               self.Excluded_Code_Cvs_Path,
               self.New_Html_File_Path]  
          
      
   #Arguments for consolidate_report.py sca tool
   def _consolidate_report(self):
      self.HTML_File= r'C:\rw_apps\ch53k_sca\reports\IFM\A4_Testing_Reports\03_20_2015\sca_tools_inputs/ifm_a4_aggregate_report_3_20_2015.html'
      self.New_Modified_File_List=r'C:\rw_apps\ch53k_sca\reports\IFM\A4_Testing_Reports\03_20_2015\sca_tools_inputs/IFM_artifacts_03_18_2015.csv'
      self.Differences_Folder_Path=r'C:\rw_apps\ch53k_sca\reports\IFM\A4_Testing_Reports\03_20_2015\sca_tools_inputs\new_diff_files_with_sign'
      self.Excluded_Code_Cvs_File_Path=r'C:\rw_apps\ch53k_sca\reports\IFM\A4_Testing_Reports\03_20_2015\sca_tools_outputs/IFM_Excluded_Code.csv'
      self.Prev_Agg_Reports_Html_File_Path=[r'C:\rw_apps\ch53k_sca\reports\IFM\A3_2_Testing_Reports/ifm_aggregate_report.html',
                                            r'C:\rw_apps\ch53k_sca\reports\IFM\A3_1_Testing_Reports/ifm_round2_aggregate_report.html',
                                            r'C:\rw_apps\ch53k_sca\reports\IFM\A2_Testing_Reports/ifm_aggregate_report.html']
      self.Agg_Report_Tags=['A3-2','A3-1','A2']
      self.New_Consolidate_Report_Csv_File_Path=r'C:\rw_apps\ch53k_sca\reports\IFM\A4_Testing_Reports\03_20_2015\sca_tools_outputs/IFM_Consolidate_Report.csv'
      return [ self.HTML_File,
               self.New_Modified_File_List,
               self.Differences_Folder_Path,
               self.Excluded_Code_Cvs_File_Path,
               self.Prev_Agg_Reports_Html_File_Path,
               self.Agg_Report_Tags,
               self.New_Consolidate_Report_Csv_File_Path]   
      
      
   #Arguments for check_code_exercised_in_other_apps.py sca tool
   def _check_code_exercised_in_other_apps(self):
      self.aggregate_reports_html_file_paths= [r'C:\rw_apps\ch53k_sca\reports\IFM\A4_Testing_Reports\03_20_2015\sca_tools_inputs/ifm_a4_aggregate_report_3_20_2015.html',
                                               r'C:\rw_apps\ch53k_sca\reports\FPS\A_4_SCA_Reports/fps_a4_aggregate_report.html',
                                               r'C:\rw_apps\ch53k_sca\reports\SM\A_4_SCA_Reports/sm_a4_aggregate_report_2_12_2015.html']
      
      self.metrics_reports_csv_file_paths=[r'C:\rw_apps\ch53k_sca\reports\IFM\A4_Testing_Reports\03_20_2015\sca_tools_inputs/ifm_a4_aggregate_report_3_20_2015.html',
                                           r'C:\rw_apps\ch53k_sca\reports\FPS\A_4_SCA_Reports/fps_a4_metrics_report.csv',
                                           r'C:\rw_apps\ch53k_sca\reports\SM\A_4_SCA_Reports/sm_a4_metrics_report_2_12_2015.csv']
      self.app_names=['IFM','FPS','SM']
      self.common_coverage_report_csv_file_path=r'C:\rw_apps\ch53k_sca\reports\IFM\A4_Testing_Reports\03_20_2015\sca_tools_outputs/Coverage_For_Common_Code_Packages.csv'
      
      return [ self.aggregate_reports_html_file_paths,
               self.metrics_reports_csv_file_paths,
               self.app_names,
               self.common_coverage_report_csv_file_path]  
      
#3nd class Arguments:      
      
