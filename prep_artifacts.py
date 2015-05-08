
#FILE NAME: prep_artifacts.py

#AUTHOR: Sudheer Kollapudi


#PURPOSE: To consolidate multiple entries of code packages (present in provided prep_artifacts.csv) into a single entry. 
#         This script differentiate the code packages into two categories namely new and modified, and generates the 
#         apex difference commands for all new and modified code packages.
               


import csv
import sca_utilities 
import os
#---------------------- User inputs -----------------------#
ch53k_fps_subsystems=["a661_api.ss","a661_manager.ss","a661_page.ss","error_services.ss","exec_main.ss","extended_fpln.ss",
                      "flight_plan.ss","fm_periodic_rsi.ss","fm_periodic_types.ss","fpln_attributes.ss","fpln_sync_mgr.ss",
                      "fps_arinc429.ss","fps_arinc661.ss","fps_ethernet.ss","fps_fpln.ss","fps_manager.ss","fps_plugin_utils.ss",
                      "fps_remote_services.ss","fps_services.ss","fps_udp.ss","fps_wrapper.ss","graphics.ss","interfaces.ss",
                      "perf_services.ss"]
ch53k_ifm_subsystems=["exec_main.ss","a661_api.ss","a661_manager.ss","a661_page.ss","aircraft.ss"
                     ,"alt_flight_plan.ss","annunciation.ss","arinc.ss","cdu_page_mgr.ss","database.ss"
                     ,"discretes.ss","eicas_manager.ss","error_services.ss","ext_eqpt_ctrl.ss"
                     ,"extended_fpln.ss","extended_perf.ss","fault_reporter.ss","file_services.ss"
                     ,"flight_plan.ss","fm_partition_output.ss","fm_periodic_rsi.ss","fm_periodic_rsp.ss","fm_periodic.ss"
                     ,"fpln_attributes.ss","fpln_isolation.ss","fpln_sync_mgr.ss","fps_remote_services.ss"
                     ,"guidance.ss","hlms.ss","interfaces.ss","lru.ss","mdl.ss","mdl_app.ss","mil_1553.ss"
                     ,"nav_db.ss","navigation.ss","page.ss","perf.ss","perf_database.ss","perf_services.ss"
                     ,"raim.ss","rsi_control.ss","status.ss","util_app.ss","zeroize.ss"]
ch53k_sm_subsystems=["exec_main.ss","cdu.ss","discretes.ss","dlu.ss","eicas_manager.ss"
                     ,"error_services.ss","ext_eqpt_ctrl.ss","file_services.ss","flight_recorder.ss"
                     ,"gppu.ss","interfaces.ss","lru.ss","mdl_app.ss","mfd.ss","ofp_loadsets.ss"
                     ,"page.ss","page_interfaces.ss","sm_config_mgmt.ss","status.ss","status_test.ss"
                     ,"stopwatch_mgmt.ss"]


excluded_ch53k_subsystem=["mdl.ss"]

#columns numbers (according to data in .csv file)
peerreviews_id=0
artifacts_path=1
artifacts_filename=2
artifacts_version_from=3
artifacts_version_final=5
peerreviews_status=7
#end ---------------------- User inputs -----------------------#
none="(none)"
space=" "
new = "New"
modified = "Modified"
fw_slash="/"

def Get_Data_From_Csv(path,subsystem):
#---------------------------------------------------------------   
#FUNCTIONAL DESCRIPTION:

#PURPOSE: To get the specified subsystem data from .csv file by comparing specified subsystem and
#          artifacts_path (first column of .csv file).

#LIMITATIONS: None

#NOTES: None  

# ALGORITHM AND CODE
   csv_file = open(path,'rb')
   csv_reader = csv.reader(csv_file)
   csv_data=[]
   for row in csv_reader:
      if subsystem in row[artifacts_path]:
         csv_data.append([row[peerreviews_id],row[artifacts_path],row[artifacts_filename],row[artifacts_version_from],row[artifacts_version_final],row[peerreviews_status]])
      #endif subsystem in row[artifacts_pathm]:
   #end for row in csv_reader:
   csv_file.close()
   if (len(csv_data)==0):
      subsystem_not_present = "NO SUBSYSTEM"
      return subsystem_not_present
   else:
      return csv_data
   #if (len(subsystem_data)==0)
#def Get_Data_From_Csv(path,subsystem):
  
def Consolidate_Prep_Artifacts(prep_artifacts_csv_file_path, #(Input) 
                               prep_artifacts_with_latest_version_csv_file_path,#(Input)
                               consolidate_prep_artifacts_csv_file_path, #(output)
                               #csv_modi_out_put_path,  #(output) #code to get only modified code packages 
                               apex_difference_commands_sh_file_path,#(output)
                               apex_difference_files_folder_path, #(Input)
                               subsytem_name):  #(Input))
 
   
#---------------------------------------------------------------------------------------------
#FUNCTIONAL DESCRIPTION: 

#PURPOSE: To consolidate multiple entries of code packages (present in provided prep_artifacts.csv,prep_artifacts_csv_file_path) 
#         into a single entry(consolidate_prep_artifacts_csv_file_path). 
#         This script differentiate the code packages into two categories namely new and modified, and generates the 
#         apex difference commands for all new and modified code packages(apex_difference_commands_sh_file_path).

#prep_artifacts_csv_file_path: (input path)which contains prep artifacts data.
#consolidate_prep_artifacts_csv_file_path: (output path)which contains consolidated prep artifacts data
#csv_modi_out_put_path:(output path) which contains only modified code packages 
#apex_difference_commands_sh_file_path:(output path) which contains difference commands for modified and new code packages
#apex_difference_files_folder_path (string)path where ada new and modified difference files need to be placed)
#subsytem_name="ifm","fps","sm"

# LIMITATIONS: None

#NOTES: 
#prep_artifacts_csv_file_path file columns should be
#PeerReviews.ID | Artifacts.Path | Artifacts.Filename | Artifacts.VersionFrom | Artifacts.VersionTo | Artifacts.VersionFinal | PeerReviews.ArtifactType | PeerReviews.Status

#consolidate_prep_artifacts_csv_file_path file columns would be
#Artifacts.Path        | Artifacts.Filename   |  Artifacts.VersionFrom | Artifacts.VersionFinal | code_package_type
#/fms/app/exec_main.ss | app_initialize.2.ada |  CH53G_CNS/1           | CH53K_IFM/2            | Modified

#apex_difference_commands_sh_file_path file would be
#difference -previous "/fms/app/perf.ss eicas_data.2.ada CTES_FM 8" -current "/fms/app/perf.ss eicas_data.2.ada CH53K_IFM 8" > C:/rw_apps/CH-53K/CH-53K_IFM_SCA/A4_Testing_Reports/03_03_2015/new_diff_files/eicas_data_diff.txt

# ALGORITHM AND CODE
   
   #check file type
   sca_utilities.check_file_type(prep_artifacts_csv_file_path,'.csv')
   sca_utilities.check_file_type(consolidate_prep_artifacts_csv_file_path,'.csv')
   sca_utilities.check_file_type(prep_artifacts_with_latest_version_csv_file_path,'.csv')
   sca_utilities.check_file_type(apex_difference_commands_sh_file_path,'.sh')
   
   #get data from prep_artifacts_with_latest_version_csv_file_path
   art_data_with_lat_ver = sca_utilities.get_csv_data(prep_artifacts_with_latest_version_csv_file_path,[0,1,2],True) 
   #list variables to hold the output data
   consolidate_prep_artifacts_data=[]
   #output_csv_modi_data=[] #code to get only modified code packages 
   apex_difference_commands_txt_data=[]
   consolidate_prep_artifacts_data.append(["Artifacts.Path","Artifacts.Filename","Artifacts.VersionFrom","Artifacts.VersionFinal","code_package_type"])
   #output_csv_modi_data.append(["Artifacts.Path","Artifacts.Filename"]) #code to get only modified code packages 
  
   #assign list of subsystems for specified apps
   if subsytem_name.lower() == "fps":
      ch53k_subsystems=ch53k_fps_subsystems
   elif subsytem_name.lower() == "ifm": 
      ch53k_subsystems=ch53k_ifm_subsystems  
   elif subsytem_name.lower() == "sm": 
      ch53k_subsystems=ch53k_sm_subsystems  
   #if subsytem_name.lower() == "fps": 
       
   #loop for each subsystems for specified apps
   for subsys in ch53k_subsystems:
      
      #check specified subsystem present in provided ('prep_artifacts_csv_file_path') .csv file
      subsystem_data=Get_Data_From_Csv(prep_artifacts_csv_file_path,fw_slash+subsys) 
      
      #if subsystem is excluded
      if subsys in excluded_ch53k_subsystem:
         print subsys+ " is excluded"
      elif (subsystem_data == "NO SUBSYSTEM"): #if specified subsystem is not present in .csv file
         print subsys+" is not in .csv file"
      else:
         #if specified subsystem is present in .csv file
         
         #list for artifacts filenames
         file_names= [] 
         for file_data in subsystem_data:
            file_names.append(file_data[artifacts_filename])
         #end for loop 
         #To remove duplicates
         file_names = list(set(file_names))
         
         #get data of each ada file 
         for file_name in file_names:
            
            prep_id = []
            art_path = []
            art_filename = []
            art_version_from =[]
            art_version_final=[]
            old_version = ""
            new_mod=""
            old_version_for_diff =""
            
            for file_data in subsystem_data:
               
               if(file_name == file_data[artifacts_filename]and file_data[5].lower() == "closed"):
                  prep_id.append(int(file_data[0][10:]))
                  art_path.append(file_data[1])
                  art_filename.append(file_data[2])
                  art_version_from.append(file_data[3])
                  art_version_final.append(file_data[4])
               #end if(file_name == file_data[artifacts_filename])
            #for file_data in subsystem_data:
            
            #sort prep ID's to get earliest and latest prep IDs.
            if (len(prep_id)!=0):
               sorted_prep_id=sorted((e,i) for i,e in enumerate(prep_id))
               sort_out =[sorted_prep_id[0][1],sorted_prep_id[len(sorted_prep_id)-1][1]]
               file_type=""
               
               #to check latest version 
               latest_version='' 
               path=''
               file_found=False
               for art_data in art_data_with_lat_ver:
                  if(art_data[1].strip().lower()==art_filename[sort_out[1]].strip().lower()):
                     file_found=True
                     if art_data[2].strip().lower()==art_version_final[sort_out[1]].strip().lower():
                        latest_version=art_version_final[sort_out[1]]
                     else:
                        latest_version=art_data[2].strip()
                     #end if art_data[2].strip().lower()==art_version_final[sort_out[1]].strip().lower():      
                     if(art_data[0].strip().lower()==art_path[sort_out[1]].strip().lower()):
                        path=art_path[sort_out[0]]
                     else:  
                        path=art_data[0].strip()
                     #end f(art_data[0].strip().lower()==art_path[sort_out[1]].strip().lower()):  
                     break
                  #end if(art_data[0].strip().lower()==art_path[sort_out[1]].strip().lower()and   
               #end for art_data in art_data_with_lat_ver:
               
               if not file_found:
                  latest_version=art_version_final[sort_out[1]]
                  path=art_path[sort_out[0]]
               #end   if not file_found:
               
               if none in art_version_from:#if .ada file is new one 
                  old_version= none
                  new_mod = new 
                  old_version_for_diff = latest_version
                  file_type="_new.txt"
               else:#if .ada file is modified one 
                  old_version= art_version_from[sort_out[0]]
                  new_mod = modified 
                  old_version_for_diff= art_version_from[sort_out[0]]
                  file_type="_diff.txt"
               #if none in art_version_from: 
                
               if(old_version != ""):
                  
                  slash_index=art_filename[sort_out[0]].find("/")
                  
                  if(slash_index !=-1):
                     pack= art_filename[sort_out[0]][slash_index+1:]
                  else:
                     pack= art_filename[sort_out[0]]  
                  #end if(slash_index !=-1):
                  
                  consolidate_prep_artifacts_data.append([path,pack,old_version,latest_version,new_mod])
                  found_slash = art_filename[sort_out[0]].find("/")
                  
                  if(found_slash!=-1):
                     filename = art_filename[sort_out[0]][found_slash+1:-6]
                  else:
                     filename = art_filename[sort_out[0]][:-6]
                  #end if(found_slash!=-1):  
                  
                  version_from=old_version_for_diff.replace("/",space)
                  version_final=latest_version.replace("/",space)
                  apex_difference_commands_txt_data.append("difference -previous "+'"'+path+space+art_filename[sort_out[0]]+space+version_from+'"'+" -current "+'"'+path+space+art_filename[sort_out[0]]+space+version_final+'"'+" > "+apex_difference_files_folder_path+"/"+filename+file_type)
                  #if (new_mod== modified): #code to get only modified code packages 
                  #   output_csv_modi_data.append([art_path[sort_out[0]],pack]) #code to get only modified code packages 
               # if(old_version != ""):  
            #if (len(prep_id)!=0):    
         #for file_name in file_names:   
          
      #if subsys in excluded_ch53k_subsystem:
   #for subsys in ch53k_subsystems:   
   
   print "writing output data"
   sca_utilities.write_csv_data(consolidate_prep_artifacts_csv_file_path,consolidate_prep_artifacts_data)
   #sca_utilities.write_csv_data(csv_modi_out_put_path,output_csv_modi_data)
   sh_file=open(apex_difference_commands_sh_file_path,'wb')
   sh_file.write("\n".join(apex_difference_commands_txt_data))
   sh_file.close()
#end def main(prep_artifacts_csv_file_path,       

     
