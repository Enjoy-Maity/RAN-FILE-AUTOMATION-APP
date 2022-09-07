import json
import pandas as pd
from tkinter import messagebox
import re

def task(json_excel_file,json_bsc_text_file):
    try:
        workbook=pd.ExcelFile(json_excel_file)
        sheets=workbook.sheet_names
        
        sheet_name=""
        for sheet in sheets:
            # To check if New Lac column exists in the sheets in workbook
            if 'newlac' in pd.read_excel(workbook,sheet) :
                sheet_name=sheet
        
        excel_file=pd.read_excel(workbook,sheet_name)
        cell_list_dict=dict()
        newlac_dict=dict()

        unique_destination_bscs=excel_file["Destination BSC"].unique()

        for j in range(0,len(excel_file)):
            if excel_file.iloc[j]["Destination BSC"] not in cell_list_dict:
                cell_list_dict[excel_file.iloc[j]["Destination BSC"]]=list()
                cell_list_dict[excel_file.iloc[j]["Destination BSC"]].append(excel_file.iloc[j]["Cell Name"])
            else:
                cell_list_dict[excel_file.iloc[j]["Destination BSC"]].append(excel_file.iloc[j]["Cell Name"])
        
        for j in range(0,len(excel_file)):
            newlac_dict[excel_file.iloc[j]["Cell Name"]]=excel_file.iloc[j]["newlac"]

        for bsc in unique_destination_bscs:        
            cell_list_dict[bsc]=list(set(cell_list_dict[bsc]))
        


        file=open(json_bsc_text_file,"r")
        file_reader=file.readlines()
        modified_file_reader=[]

        for line in file_reader:
            modified_file_reader.append(line.strip())
        
        for bsc in unique_destination_bscs:
            rejected_cells=[]
            basestations=[]
            cells=[]
            for j in range(0,len(modified_file_reader)):
                if len(modified_file_reader[j])==0:
                    continue
                else:
                    if len(re.findall("\AFDN",modified_file_reader[j]))>0:
                        if modified_file_reader[j].split(":")[1].split(",")[7].split("=")[1] in cell_list_dict[bsc]:
                            
                            if len(re.findall("\Aconnected",modified_file_reader[j+1]))>0:
                                dict1=dict()
                                dict2=dict()

                                if len(modified_file_reader[j+1].split(":")[1])>6:
                                    dict2["fdn"]=modified_file_reader[j+1].split(":")[1]
                                    dict1["candidateFdn"]=modified_file_reader[j].split(":")[1][0:-15]
                                    dict1["newLac"]=str(newlac_dict[modified_file_reader[j].split(":")[1].split(",")[7].split("=")[1]])
                                    cells.append(dict1)
                                    basestations.append(dict2)
                                
                                elif len(modified_file_reader[j+2].split(":")[1])>6:
                                    dict1["candidateFdn"]=modified_file_reader[j].split(":")[1][0:-15]
                                    dict1["newLac"]=str(newlac_dict[modified_file_reader[j].split(":")[1].split(",")[7].split("=")[1]])
                                    cells.append(dict1)
                                    dict2["fdn"]=modified_file_reader[j+2].split(":")[1]
                                    basestations.append(dict2)
                                
                                else:
                                    rejected_cells.append(modified_file_reader[j].split(":")[1].split(",")[7].split("=")[1])

                    j=j+2
                                
            
                    
            dict_main={"baseStations":basestations,"cells":cells,"targetNetworkController":f"NetworkElement={bsc}","technologyType": "GSM"}
            with open(rf"C:\RAN\JSON\json_file_for_dest_bsc_{bsc}.json","w") as f:
                json.dump(dict_main,f,indent=4)
            

            
            if len(rejected_cells)>0:
                messagebox.showwarning("    Rejected Cells",list(set(rejected_cells)))
                messagebox.showinfo("   File to see the rejected cells",rf"C:\RAN\JSON\rejected_cells_dest_bsc_{bsc}.txt")
                file1=open(rf"C:\RAN\JSON\rejected_cells_dest_bsc_{bsc}.txt","w")
                mystr=""
                for cell in rejected_cells:
                    mystr+=cell+"\n"
                file1.write(mystr)

                file1.close()
            messagebox.showinfo("   File Creation was Successful",rf"C:\RAN\JSON\json_file_for_dest_bsc_{bsc}.json  was successfully created. ")
            
            

        file.close()
        
    
    except Exception as e:
        messagebox.showerror("  Exception Occured",e)


#task(r"C:\Users\emaienj\Downloads\Enjoy_JASON\Enjoy_JASON\SAMPLE_input_JSON.xlsx",r"C:\Users\emaienj\Downloads\Enjoy_JASON\Enjoy_JASON\ENM_TG_CELL_DUMP_CLI.txt")