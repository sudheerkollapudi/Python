
#FILE NAME: check_code_exercised_in_other_apps.py

#AUTHOR: Sudheer Kollapudi



#PURPOSE: This script is used to get code coverage for common code packages, across specified applications.
#         Script scans specified metrics reports (.csv files) to get the common code packages.
#         And it verifies the code for particular function or procedure is same in other apps or not, 
#         by scanning the specified aggregate reports. If code is same then it will produce the updated code coverage
#         by cCalculating exercised lines in other apps.
  



import sca_utilities
import re
import csv
code_coverage="Code Coverage for Unit: "
test_cov_sum="TEST COVERAGE SUMMARY"
no_coverage="No Coverage Data Exists"



def get_coverage_percentage(not_exc_lines_sub1,not_exc_lines_sub2,total_lines):
#---------------------------------------------------------------   
#FUNCTIONAL DESCRIPTION:

#PURPOSE: To calculate(with exercised lines in provided arrays and total lines)code coverage percentage for specified procedure.  

#LIMITATIONS: None

#NOTES: None  

# ALGORITHM AND CODE    
   
   #convert string type ('[1;2;3;4]') to arrya type ([1,2,3,4]).
   not_exc_lines_sub1=eval(not_exc_lines_sub1.replace(';',','))
   not_exc_lines_sub2=eval(not_exc_lines_sub2.replace(';',','))
   
   #calculate code coverage 
   common=list(set(not_exc_lines_sub1).intersection(not_exc_lines_sub2))
   coverage=[((total_lines-float(len(common)))/total_lines)*100,str(common).replace(',',';')]
   #return value
   return coverage

#end def get_coverage_percentage(not_exc_lines_sub1,not_exc_lines_sub2,total_lines):

def get_lines_in_procedure(agg_data,pack,proc_func_name,pro_no):
#---------------------------------------------------------------   
#FUNCTIONAL DESCRIPTION:

#PURPOSE: To get instrumented lines of specified function or procedure. 

#LIMITATIONS: None

#NOTES: None  

# ALGORITHM AND CODE      
   
   #Get proc_func_name if procedure name extended with '()'.
   proc_func_name=proc_func_name.lower()
   pack=code_coverage+pack
   proc_func_name=re.sub(r" ?\(\w+\)", "", proc_func_name)
   combine_line="\n  "+str(pro_no)
   line_data=""
   data_in_lines=''
   
   #Get the data of pecified function or procedure from aggregate report.
   if (agg_data.lower().find(pack.lower()) != -1):
      line_data=agg_data[agg_data.lower().find(pack.lower())+len(pack):]
      line_data=line_data.strip()
      
      #if no coverage found for specified code package then return no coverage
      if line_data.find(no_coverage)== 0:
         line_data=no_coverage 
      else:
         
         #get end line of specified code package
         if(line_data.find(test_cov_sum) != -1):
            line_data=line_data[:line_data.find(test_cov_sum)] 
         #end if(line_data.find(test_cov_sum) != -1):   
         
         #get instrumented lines
         if (line_data.find(combine_line)!= -1):
            line_data=line_data[line_data.find(combine_line):]
            
            #check end of procedure
            if (line_data.lower().find('end '+proc_func_name+";") != -1):
               line_data=line_data[:line_data.lower().find('end '+proc_func_name+";")]
            #end if (line_data.lower().find('end '+proc_func_name+";") != -1):   
            
         else:
            line_data="" 
         #end if (line_data.find(combine_line)!= -1):   
      #end if line_data.find(no_coverage)== 0:      
   else:
      line_data="" 
   #end if (agg_data.lower().find(pack.lower()) != -1):
   
   #to get code for all instrumented lines
   lines=[]   
   if (line_data != ""  and line_data != no_coverage):
      data_in_lines=line_data.split('\n')
      #loop for each line
      for line in data_in_lines:
         #if line is not blank
         if (line.replace(" ","") !="" and line.replace(" ","") !="\n"):
            if len(line.split()) >= 2:
              #get the line data 
              if (re.match('\d',line.split()[0])!= None and 
                   re.match('\d',line.split()[1]) != None):
                  lines.append(line)
                  line_data="next_line"
              #end if (re.match('\d',line.split()[0])!= None and 
              if line.split()[0]==str(pro_no+1):
                 line_data="next_function"
                 break
              #end if line.split()[0]==str(pro_no+1):
             #end if len(line.split()) >= 2:   
         #end if (line.replace(" ","") !="" and line.replace(" ","") !="\n"):   
      #end  for line in data_in_lines:         
   #end if (line_data != ""  and line_data != no_coverage):            
   rer_data=[line_data,lines]    
   #return output          
   return  rer_data   

#end def get_lines_in_procedure(agg_data,pack,proc_func_name,pro_no):

def get_specific_data(data):
   
#---------------------------------------------------------------   
#FUNCTIONAL DESCRIPTION:

#PURPOSE: To remove extra symbols and '*' at starting of line, 
#         TO check line is line is exercised or not

#LIMITATIONS: None

#NOTES: None  

# ALGORITHM AND CODE   
    
   data=data.strip()
   exerciz=[False]
   #if '*' is found the set exerciz[0] to True
   if (data.split()[2]=="*"):
      exerciz=[True,data[data.find('*')+1:]]
   else:
      #if '*' is not found the set exerciz[0] to False
      l_number = data.split()[1]
      fuc_no=data.split()[0]
      exerciz=[False,data[data[len(fuc_no):].find(l_number)+len(l_number)+len(fuc_no):],l_number]
   #end if (data.split()[2]=="*"):
   
   #return data   
   return exerciz

#end def get_specific_data(data):

def check_two_apps_code(main_arry,sub1_arry,len):
#---------------------------------------------------------------   
#FUNCTIONAL DESCRIPTION:

#PURPOSE: To check code in (main_arry,sub1_arry) specified procedures in different apps is Identical or not.

#LIMITATIONS: None

#NOTES: None  

# ALGORITHM AND CODE  
   
   #Declare variables
   excized=0
   not_excized=0
   not_excized_line_no=''
   code_msg=['nothing']
   
   #loop for each line 
   for line in range(0,len):
      main_data=get_specific_data(main_arry[line])
      sub1_data=get_specific_data(sub1_arry[line])
      
      #check each line data equal or not
      if(main_data[1].replace(" ","").lower()== sub1_data[1].replace(" ","").lower()):
         
         #if equal and line is exercised,then increment the counter  
         if(main_data[0] or sub1_data[0]):
            excized+=1
          #if equal and line is not exercised, then increment the counter   
         else:
            not_excized+=1   
            not_excized_line_no= not_excized_line_no + str(main_data[2])+";"
         #end if(main_data[0] or sub1_data[0]):
      else:
         #if line of code not equal
         code_msg=["not_matching",0]
         break
      #end  if(main_data[1].replace(" ","").lower()== sub1_data[1].replace(" ","").lower()):
   #end  for line in range(0,len):
   
   #if lines are Matching then return updated coverage 
   if (code_msg[0] != 'not_matching'):
      code_msg=['matching',(float(excized)/float(len))*100,'['+not_excized_line_no+']']
   
   #return data   
   return code_msg

#def check_two_apps_code(main_arry,sub1_arry,len):           
         
def get_coverage_by_compa_2apps(match_line,main_agg,
                                sub_agg,main_agg_dic,sub_agg_dic,subsys,ref_subsys):  
#---------------------------------------------------------------   
#FUNCTIONAL DESCRIPTION:

#PURPOSE: Get coverage of particular procedure by comparing procedure 
#         code in specified apps (aggregate reports) 

#LIMITATIONS: None

#NOTES: None  

# ALGORITHM AND CODE     
   
   comon_code_coverage=[]
   match_line[4]=match_line[4].replace(' ',',')
   #if procedure name equal to = then convert it into string'='
   if (match_line[4]== '='):
      match_line[4]='"="'
   #end if (match_line[4]== '='):
   
   #get code in both apps for particular procedure   
   array=main_agg_dic[match_line[2]]
   main_proc_func_no=array.index(match_line[4])
   array=sub_agg_dic[match_line[2]]
   sub_proc_func_no=array.index(match_line[4])
   main_lines_data=get_lines_in_procedure(main_agg,match_line[2],match_line[4],main_proc_func_no+1)
   sub_lines_data=get_lines_in_procedure(sub_agg,match_line[2],match_line[4],sub_proc_func_no+1)
   main_arry=False
   sub_arry=False
   covrage_true =False
      
   #if code for particular procedure found the set main_arry to True
   if(main_lines_data[0] != "" and main_lines_data[0] != no_coverage):
      main_lines=main_lines_data[1]
      main_arry=True
   #end if(main_lines_data[0] != "" and main_lines_data[0] != no_coverage): 
     
   #if code for particular procedure found the set sub_arry to True
   if(sub_lines_data[0] != "" and sub_lines_data[0] != no_coverage): 
      sub_lines=sub_lines_data[1]
      sub_arry=True  
   #end if(sub_lines_data[0] != "" and sub_lines_data[0] != no_coverage): 
   combine_cover=[""]
   
   #if lines of code for particular procedure found in both apps then check for coverage
   if (main_arry and sub_arry):
      combine_cover=check_two_apps_code(main_lines,sub_lines,int(float(match_line[8])))
   elif not main_arry:
      #if lines of code for particular procedure not found for main app
      print match_line[2] + " package doesn't have coverage report in "+ref_subsys+ " aggregate report"
      covrage_true=True
   else:
      #if lines of code for particular procedure not found for sub app
      covrage_true=True
      print match_line[2] + " package doesn't have coverage report in "+subsys+ " aggregate report"      
   #end if (main_arry and sub_arry):
   
   #set coverage value 
   if(combine_cover[0]=='matching'):
      comon_code_coverage=[match_line[0],match_line[2],match_line[4],match_line[6],str("%.2f" %combine_cover[1])+"%",combine_cover[2],subsys]   
   elif(combine_cover[0]=='not_matching' or covrage_true==True):   
      comon_code_coverage=['not_matching']
   #end  if(combine_cover[0]=='matching'):
   
   #Return the value 
   return comon_code_coverage    
        
#end def get_coverage_by_compa_2apps(match_in_one,main_agg,

def Check_Code_In_Other_Apps(aggregate_reports_html_file_paths,#(Input)
                             metrics_reports_csv_file_paths,#(Input)
                             app_names,#(Input)
                             common_coverage_report_csv_file_path):#(Output)
#---------------------------------------------------------------   
#FUNCTIONAL DESCRIPTION:

#PURPOSE: This function is used to get code coverage for common code packages, across specified applications.
#         function scans specified metrics reports (.csv files) to get the common code packages.
#         And it verifies the code for particular function or procedure is same in other apps or not, 
#         by scanning the specified aggregate reports. If code is same then it will produce the updated code coverage
#         by cCalculating exercised lines in other apps.

#aggregate_reports_html_file_paths: Which contains aggregate reports path for specified apps 

#metrics_reports_csv_file_paths: Which contains metrics reports path for specified apps 

#app_names:which contains names of all apps

#common_coverage_report_csv_file_path:output csv file containing coverage for common code packages across all apps.

#LIMITATIONS: None

#NOTES: Provide The app data which needs to be compare with other apps data in index zero of following input arrays.
#        aggregate_reports_html_file_paths
#        metrics_reports_csv_file_paths
#        app_names
#        aggregate_reports_html_file_paths,metrics_reports_csv_file_paths,app_names are expected to be parallel lists.

# ALGORITHM AND CODE      
   
   #get 3 apps metrics reports data 
   main_metri=sca_utilities.get_file_data_in_lines(metrics_reports_csv_file_paths[0])
   sub1_metri=sca_utilities.get_file_data_in_lines(metrics_reports_csv_file_paths[1])
   sub2_metri=sca_utilities.get_file_data_in_lines(metrics_reports_csv_file_paths[2])
   
   match_in_both=[]
   match_in_sub1=[]
   match_in_sub2=[]
   
   i=0
   #to check common code packages in 3 apps
   for main_line in main_metri:
      #skip firat row
      if i ==1:
         
         main_line=main_line.split(',')
         sub1_found=False
         sub2_found=False
         main_line[8]=main_line[8].replace('\n','')
         
         #exclude code packages which are 100% exercised (and also exclude rows which contains TOTALS and GRANDTOTALS)
         if main_line[6]!= '100%' and main_line[3]!= 'TOTALS' and main_line[3]!= 'GRANDTOTALS':
            # check for common code package in sub app1
            for sub1_line in sub1_metri:
               sub1_line=sub1_line.split(',')
               #if common code package found then, set sub1_found to TRUE
               if (main_line[0]==sub1_line[0]and main_line[2]==sub1_line[2] and
                   main_line[4]==sub1_line[4]and main_line[8]==sub1_line[8].replace('\n','')):
                  sub1_found=True
                  break
               #end  if (main_line[0]==sub1_line[0]and main_line[2]==sub1_line[2] and
            #end for sub1_line in sub1_metri:
            
            # check for common code package in sub app2       
            for sub2_line in sub2_metri:
               sub2_line=sub2_line.split(',')
                #if common code package found then, set sub2_found to TRUE
               if (main_line[0]==sub2_line[0]and main_line[2]==sub2_line[2] and
                   main_line[4]==sub2_line[4]and main_line[8]==sub2_line[8].replace('\n','')):
                  sub2_found=True
                  break
               #end if (main_line[0]==sub2_line[0]and main_line[2]==sub2_line[2] and
            #end for sub2_line in sub2_metri:
            
            #set match_in_both,match_in_sub1,match_in_sub2 to True
            #according to code package found in other apps
            if sub1_found==True and sub2_found==True:
               match_in_both.append(main_line)
            elif sub1_found==True and sub2_found==False:
               match_in_sub1.append(main_line) 
            elif sub1_found==False and sub2_found==True:
               match_in_sub2.append(main_line)    
           #end  if sub1_found==True and sub2_found==True:      
      i=1
   #end for main_line in main_metri:
   
   #get 3 apps packages and procedures dictionary
   main_agg_dic=sca_utilities.get_packages_and_procedures_present_in_html_path(aggregate_reports_html_file_paths[0])
   sub1_agg_dic=sca_utilities.get_packages_and_procedures_present_in_html_path(aggregate_reports_html_file_paths[1])
   sub2_agg_dic=sca_utilities.get_packages_and_procedures_present_in_html_path(aggregate_reports_html_file_paths[2])
   
   #get # apps aggregate data in a string    
   main_agg=sca_utilities.convert_html_to_text(aggregate_reports_html_file_paths[0])
   sub1_agg=sca_utilities.convert_html_to_text(aggregate_reports_html_file_paths[1])
   sub2_agg=sca_utilities.get_file_data_as_string(aggregate_reports_html_file_paths[2])
   
   #heading of output file  
   new_cove=[['Subsystem','Filename','Subprogram','previous cover % statement','Cover % Statement','Not Exercised', 'Match With']]
   
   #if code packages found in apps
   if(len(match_in_both) !=0):
       #Loop for all code packaes which are common in both app
       for matched_data in match_in_both:
          #get coverage data by compare code of main app and sub1 app
          sub1_covr=get_coverage_by_compa_2apps(matched_data,main_agg,sub1_agg,
                                    main_agg_dic,sub1_agg_dic,app_names[1],app_names[0])
           #get coverage data by compare code of main app and sub2 app
          sub2_covr=get_coverage_by_compa_2apps(matched_data,main_agg,sub2_agg,
                                    main_agg_dic,sub2_agg_dic,app_names[2],app_names[0])
          #check coverafe data
          if (sub1_covr[0]!='not_matching' and sub2_covr[0]!='not_matching' ):
             both_cove=get_coverage_percentage(sub1_covr[5],sub2_covr[5],total_lines)
             sub1_covr[4]=str("%.2f" %both_cove[0])+"%"
             sub1_covr[5]= both_cove[1]
             sub1_covr[6]= app_names[1]+','+app_names[2]
             new_cove.append(sub1_covr)
          elif(sub1_covr[0]!='not_matching'):
             new_cove.append(sub1_covr)
          elif(sub2_covr[0]!='not_matching'):   
             new_cove.append(sub2_covr)
          #end if (sub1_covr[0]!='not_matching' and sub2_covr[0]!='not_matching' ):   
   #end if(len(match_in_both) !=0):
   
   #if code packages found in sub1 app only       
   if(len(match_in_sub1) !=0):
      #loop for code packages found in sub1 app only       
      for matched_data in match_in_sub1:
         #get coverage data by compare code of main app and sub1 app
         sub1_covr=get_coverage_by_compa_2apps(matched_data,main_agg,sub1_agg,
                           main_agg_dic,sub1_agg_dic,app_names[1],app_names[0])
         #append coverage data of common procedure if procedure data same in both apps
         if(sub1_covr[0]!='not_matching'):
            new_cove.append(sub1_covr)
         #end if(sub1_covr[0]!='not_matching'):
       #end for matched_data in match_in_sub1:     
   #end if(len(match_in_sub1) !=0):
   
   #if code packages found in sub2 app only                
   if(len(match_in_sub2) !=0):
       #loop for code packages found in sub2 app only       
      for matched_data in match_in_sub2:
         #get coverage data by compare code of main app and sub2 app
         sub2_covr=get_coverage_by_compa_2apps(matched_data,main_agg,sub2_agg,
                                 main_agg_dic,sub2_agg_dic,app_names[2],app_names[0])
         #append coverage data of common procedure if procedure data same in both apps
         if(sub2_covr[0]!='not_matching'):
            new_cove.append(sub2_covr)
         #end if(sub2_covr[0]!='not_matching'):
      #end  for matched_data in match_in_sub2:   
   #end  if(len(match_in_sub2) !=0):
      
   print "Writing output"   
   common_cov_file=sca_utilities.write_csv_data(common_coverage_report_csv_file_path,new_cove) 
   
#end def Check_Code_In_Other_Apps(aggregate_reports_html_file_paths,#(Input)
