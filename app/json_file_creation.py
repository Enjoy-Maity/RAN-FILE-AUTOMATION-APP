import json
import pandas as pd
from tkinter import messagebox
#import time
from threading import *
# from iteration_utilities import everseen
# from queue import Queue

# queue=Queue()

class ThreadWithReturnValue(Thread):
    def __init__(self,group=None,target=None,name=None,args=(),kwargs={},Verbose=None):
        Thread.__init__(self,group,target,name,args,kwargs)
        self._return=None
    
    def run(self):
        if self._target is not None:
            self._return=self._target(*self._args,**self._kwargs)
    
    def join(self,*args):
        Thread.join(self,*args)
        return self._return
        

def cell_tg_creation(cell_name_list,cell_tg_dict,new_modified_file_reader,cell_fdn_dict,cell_source_bsc_dict):
    for cell in cell_name_list:
        for i in range(0,len(new_modified_file_reader)):
            if (new_modified_file_reader[i].__contains__("FDN")) or (new_modified_file_reader[i].__contains__("fdn")):
                if (new_modified_file_reader[i+1].__contains__("Tg")) or (new_modified_file_reader[i+1].__contains__("tg")):
                    if (new_modified_file_reader[i].split(":")[1].__contains__(cell)) and (new_modified_file_reader[i].split(":")[1].__contains__(cell_source_bsc_dict[cell])):
                        if cell not in cell_tg_dict.keys():
                            # cell_tg_dict[cell]=set()
                            # cell_fdn_dict[cell] = set()
                            # cell_tg_dict[cell].add(new_modified_file_reader[i+1].split(":")[1])
                            # cell_fdn_dict[cell].add(new_modified_file_reader[i].split(":")[1])
                            cell_tg_dict[cell] = str(new_modified_file_reader[i+1].split(":")[1])
                            cell_fdn_dict[cell] = str(new_modified_file_reader[i].split(":")[1])
                        # else:
                        #     cell_tg_dict[cell].add(new_modified_file_reader[i+1].split(":")[1])
                        #     cell_fdn_dict[cell].add(new_modified_file_reader[i].split(":")[1])
                i+=1
            else:
                continue
    
    result=[]
    result.extend((cell_tg_dict,cell_fdn_dict))

    return result

def task(json_excel_file,json_text_file):
    # json_excel_file=argument_list[0]
    # json_text_file=argument_list[1]
    # flag=argument_list[2]
    file=open(json_text_file,"r")
    reader=file.readlines()
    modified_file_reader=list()
    # begin=time.time()
    for line in reader:
        if len(line.strip())>0:
            if line.strip().__contains__(": null"):
                continue
            else:
                modified_file_reader.append(line.strip())
    
    
    modified_file_reader.remove(modified_file_reader[len(modified_file_reader)-1])
    # for i in (modified_file_reader):
    #     if str(i).__contains__(": null"):
    #         modified_file_reader.remove(i)
    
    # for i in modified_file_reader:
    #     if str(i).__contains__(": null"):
    #         modified_file_reader.remove(i)
    new_modified_file_reader=[]

    for line in modified_file_reader:
        if ((line.split(":")[1].strip()).__contains__(",ChannelGroup=")) or ((line.split(":")[1].strip()).__contains__(",channelgroup=")):
            k=line.split(":")[1].strip().split(",")
            tmp=line.split(":")[0].strip()
            for l in k:
                if (l.__contains__("ChannelGroup=")) or (l.__contains__("channelgroup=")):
                    k.remove(l)
            tmp+=':'+','.join(k)
            new_modified_file_reader.append(tmp)
        else:
            k=line.split(":")[1].strip()
            tmp=line.split(":")[0].strip()+":"+k
            new_modified_file_reader.append(tmp)
    del modified_file_reader
    
    cell_fdn_dict={}

    
    
    
    # for line in modified_file_reader:
    #     # try:
    #         if (len(line)>0):
    #             #print(line)
    #             if len(line.split(":")[1])<8:
    #                 modified_file_reader.remove(line)
    #     # except:
    #     #     continue

    workbook=pd.ExcelFile(json_excel_file)
    sheets=workbook.sheet_names
    
    sheet_name=""
    for sheet in sheets:
        # To check if New Lac column exists in the sheets in workbook
        if 'newlac' in pd.read_excel(workbook,sheet) :
            sheet_name=sheet
    
    excel_file=pd.read_excel(workbook,sheet_name)
    excel_file.fillna(-1,inplace = True)
    cell_newlac_dict=dict()
    cell_source_bsc_dict=dict()
    unique_destination_bsc=list(excel_file['Destination BSC'].unique())
    dest_bsc_cell_dict=dict()
    for i in range(0,len(excel_file)):
            cell_newlac_dict[excel_file.iloc[i]['Cell Name']]= excel_file.iloc[i]['newlac']
            cell_source_bsc_dict[excel_file.iloc[i]['Cell Name']]=excel_file.iloc[i]['Source BSC']
            if excel_file.iloc[i]['Destination BSC'] not in dest_bsc_cell_dict:
                dest_bsc_cell_dict[excel_file.iloc[i]['Destination BSC']]=set()
                dest_bsc_cell_dict[excel_file.iloc[i]['Destination BSC']].add(excel_file.iloc[i]['Cell Name'])
            else:
                dest_bsc_cell_dict[excel_file.iloc[i]['Destination BSC']].add(excel_file.iloc[i]['Cell Name'])
    
    cell_name_list=[]
    for bsc in unique_destination_bsc:
            dest_bsc_cell_dict[bsc]=list(dest_bsc_cell_dict[bsc])
            dest_bsc_cell_dict[bsc].sort()
            cell_name_list.extend(dest_bsc_cell_dict[bsc])
            # print(dest_bsc_cell_dict[bsc])
            #print(len(dest_bsc_cell_dict[bsc]))
    
    cell_tg_dict={}


    t=ThreadWithReturnValue(target=cell_tg_creation,args=(cell_name_list,cell_tg_dict,new_modified_file_reader,cell_fdn_dict,cell_source_bsc_dict))
    t.daemon=True
    t.start()
    result=t.join()
    #print(f"\n\n{result}\n\n")
    cell_tg_dict=result[0]
    cell_fdn_dict=result[1]

    # mystr = ''
    # for key in cell_tg_dict.keys():
    #     list1 = list(cell_tg_dict[key])
    #     for i in range(0,len(cell_tg_dict[key])):
    #         mystr = f"{mystr}\nkey : {key}\nvalue : {list1[i]}\n\n"
    # with open(r"C:\RAN_Automations\cell_tg_list.txt","w") as f:
    #     f.write(mystr)
    
    # mystr = ''
    # for key in tg_fdn_dict.keys():
    #     mystr = f"{mystr}\nkey : {key}\nvalue : {tg_fdn_dict[key]}\n\n"
    
    # with open(r"C:\RAN_Automations\tg_fdn_list.txt","w") as f :
    #     f.write(mystr)
    
    # for cell in list(cell_tg_dict.keys()):
    #     cell_tg_dict[cell]=list(cell_tg_dict[cell])
    #     cell_fdn_dict[cell]=list(cell_fdn_dict[cell])
    #     cell_tg_dict[cell].sort()
    #print(type(cell_newlac_dict['3SECDW1']))
    for bsc in unique_destination_bsc:
        rejected_cells=[]
        basestations=[]
        cells=[]
        for cell in dest_bsc_cell_dict[bsc]:
            dict1={}
            dict2={}
            if cell in list(cell_tg_dict.keys()):
                # match (len(cell_tg_dict[cell])):
                #     case 1:
                dict1['fdn']=cell_tg_dict[cell]
                dict2['candidateFdn']=cell_fdn_dict[cell]
                if (cell_newlac_dict[cell]) > 0:
                    dict2['newLac'] = str(int(float(cell_newlac_dict[cell])))
                    basestations.append(dict1)
                    cells.append(dict2)
                else:
                    basestations.append(dict1)
                    cells.append(dict2)
                    
                    # case _:
                    #     for i in range(0,len(cell_tg_dict[cell])):
                    #         dict1['fdn']=cell_tg_dict[cell][i]
                    #         dict2['candidateFdn']=cell_fdn_dict[cell][i]
                    #         dict2['newLac']=cell_newlac_dict[cell]
                    #         basestations.append(dict1)
                    #         cells.append(dict2)
            else:
                rejected_cells.append(cell)
        
        rejected_cells.sort()
        if len(rejected_cells)>0:
                messagebox.showwarning("    Rejected Cells",rejected_cells)
                f=open(rf"C:\RAN_Automations\JSON\rejected_cells_dest_bsc_{bsc}.txt","w")
                mystr=""
                for cell in rejected_cells:
                    mystr+=cell+"\n"
                f.write(mystr)
                messagebox.showinfo("   File to see the rejected cells",rf"C:\RAN_Automations\JSON\rejected_cells_dest_bsc_{bsc}.txt")
                f.close()
        basestations = [dict(tuple) for tuple in {tuple(sorted(dict.items())) for dict in basestations}]
        cells = [dict(tuple) for tuple in {tuple(sorted(dict.items())) for dict in cells}]
        dict_main={"baseStations":basestations,"cells":cells,"targetNetworkController":f"NetworkElement={bsc}","technologyType": "GSM"}
        with open(rf"C:\RAN_Automations\JSON\json_file_for_dest_bsc_{bsc}.json","w") as f:
            json.dump(dict_main,f,indent=4)
        messagebox.showinfo("   File Creation was Successful",rf"C:\RAN_Automations\JSON\json_file_for_dest_bsc_{bsc}.json  was successfully created. ")
        
    # end=time.time()
    # print(f"\n\n{end-begin}s\n\n")
    
    
    file.close()
    # flag=1
    # return flag
        
    
    # except Exception as e:
       
    #     messagebox.showerror("  Exception Occured",e)

    

task(r"C:\Users\emaienj\Downloads\Enjoy_JASON\Enjoy_JASON\SAMPLE_input_JSON.xlsx",r"C:\Users\emaienj\Downloads\Enjoy_JASON\Enjoy_JASON\ENM_TG_CELL_DUMP_CLI.txt")