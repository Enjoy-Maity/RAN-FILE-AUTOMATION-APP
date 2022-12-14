import re
import shutil
import pandas as pd
import xlsxwriter
from datetime import date
import os 
from tkinter import messagebox


def task(prelogfile,postlogfile,planned_cells,tf_file_name):
    try:
        
        tday=date.today().strftime("%d-%m-%Y")
        file=open(prelogfile,"r")
        pre_reader=file.readlines()
        modified_pre_reader=[] #n
        for line in pre_reader:
            modified_pre_reader.append(line.strip())

        del pre_reader

        file2=open(planned_cells,"r")
        planned_cells_reader=file2.readlines()
        modified_planned_cells_reader=[]

        for line in planned_cells_reader:
            modified_planned_cells_reader.append(line.strip())


        file3=open(tf_file_name,"r")
        tf_file_reader=file3.readlines()
        modified_tf_file_reader=[]

        for line in tf_file_reader:
            modified_tf_file_reader.append(line.strip())

        for k in range(0,len(modified_tf_file_reader)):
            if len(re.findall("\AEND",modified_tf_file_reader[k])):
                break

        for i in range(0,len(modified_pre_reader)):
            if len(re.findall("\AEND",modified_pre_reader[i])):
                break

        pre_stg_dict=dict()     # dictionary cell-input/sector:stg
        pre_stg_rxstg_dict=dict()
        pre_chgr_dict=dict()    # dictionary cell-input/sector:chgr
        pre_stg_rsite=dict()    # dictionary cell_input/sector:rsite
        tf_offset_dict=dict()   # dictionary stg/tf:offset
        pre_stg_sector=[]
        global tmp;tmp=0
        for j in range(i, len(modified_pre_reader)):
            line=modified_pre_reader[j].split()
            if len(re.findall("\ARXSTG",modified_pre_reader[j]))>0:
                if line[1] in modified_planned_cells_reader:
                    tmp=int(line[0][6:])
                    pre_stg_rxstg_dict[tmp]=line[0]
                    pre_stg_dict[int(line[0][6:])]=line[1]
                    pre_chgr_dict[int(line[0][6:])]=list() 
                    pre_chgr_dict[int(line[0][6:])].append(line[2])
            
            elif len(line)>0 and modified_pre_reader[j].split()[0] in list(pre_stg_dict.values()):
                pre_chgr_dict[tmp].append(line[1])

        
        ################################# Creating Dictionary for Rsite ###############################################
        for j in range(0,i+1):
            line=modified_pre_reader[j].split()
            if len(re.findall("\ARXSTG",modified_pre_reader[j]))>0 and int(line[0][6:]) in list(pre_stg_dict.keys()):
                pre_stg_rsite[int(line[0][6:])]=line[2]
                pre_stg_sector.append(line[1])

                    
        ############################### Removing Cells with no chgr ###################################################
        pre_chgr_dict_keys=list(pre_chgr_dict.keys())
        rejected_cell_chgr=[]
        for j in range(0, len(pre_chgr_dict_keys)):
            if len(pre_chgr_dict[pre_chgr_dict_keys[j]])==0:
                del pre_chgr_dict[pre_chgr_dict_keys[j]]
                del pre_stg_dict[pre_chgr_dict_keys[j]]
                del pre_stg_rsite[pre_chgr_dict_keys[j]]
                rejected_cell_chgr.append(pre_chgr_dict_keys[j])
        
        tg_no_list=[]
        for j in pre_stg_dict.keys():
            tg_no_list.append(j)
        

         ################################# Creating Dictionary for tf_offset and tf softsync ###########################################
        
        for j in range(0,k+1):
            line=modified_tf_file_reader[j].split()
            if len(re.findall("\ARXSTF",modified_tf_file_reader[j]))>0:
                temp=int(line[0][6:])
                if temp in tg_no_list:
                    tf_offset_dict[temp]=line[1]

        tf_softsync_dict=dict()
        tf_aligntype_dict=dict()
        for j in range(k,len(modified_tf_file_reader)):
            if len(re.findall("\ARXSTG",modified_tf_file_reader[j]))>0:
                line=modified_tf_file_reader[j].split()
                if int(line[0][6:]) in pre_stg_dict.keys():
                    tf_softsync_dict[int(line[0][6:])]=line[1]
                    if line[1]=="ON":
                        tf_aligntype_dict[int(line[0][6:])]=line[2]
                    else:
                        tf_aligntype_dict[int(line[0][6:])]=" "


        tg_list=list(pre_stg_dict.keys())         # getting the list of all the prelog tg
        tg_list_rxstg=list(pre_stg_rxstg_dict.values())
        rsite_list=list(pre_stg_rsite.values())     # getting the list of all the prelog rsite
        cell_input_list=list(pre_stg_dict.values())   # getting the list of all cell-input/sectors

        for j in range(0,len(tg_list_rxstg)):
            tg_list_rxstg[j]=tg_list_rxstg[j].lower()


        file=open(postlogfile,"r")
        post_reader=file.readlines()
        modified_post_reader=[]

        for line in post_reader:
            modified_post_reader.append(line.strip())


        post_tg=[]

        for i in range(0,len(modified_post_reader)):
            if len(re.findall("\ARXSTG",modified_post_reader[i]))>0 or len(re.findall("\ARXOTG",modified_post_reader[i]))>0:
                line=modified_post_reader[i].split()
                post_tg.append(int(line[0][6:]))

        new_tg=[]   # new tg to be filld in the coloumn for new tg

        i=0
        size=len(tg_list)

        while (len(new_tg)<size):
            if i not in post_tg and i<=8190:
                new_tg.append(i)
            i=i+1

        cell_input=[]
        chgr=[]
        rsite=[]
        newtg=[]
        oldtg=[]
        new_tg_defination_in_destination_bsc=[]
        chgr_allocation_in_destination_bsc=[]
        tg_deblock_iu_destination_bsc_rxesi=[]
        tg_deblock_iu_destination_bsc_rxble=[]
        cell_active_in_destination_bsc=[]
        cell_halte_in_source_bsc=[]
        tg_block_source_bsc_rxbli=[]
        tg_block_source_bsc_rxese=[]
        offset=[]
        softsync=[]
        aligntype=[]
        tf_offset=[]
        softsync_dt=[]
        sector=[]
        
        pre_chgr_list=list(pre_chgr_dict.values())
        for j in range(0,len(pre_chgr_list)):
            for k in range(0,len(pre_chgr_list[j])):
                if tg_list[j] in tf_offset_dict:
                    offset.append(tf_offset_dict[tg_list[j]])
                        
                    aligntype.append(tf_aligntype_dict[tg_list[j]])
                    softsync.append(tf_softsync_dict[tg_list[j]])
                    cell_input.append(cell_input_list[j])
                    chgr.append(int(pre_chgr_list[j][k]))
                    rsite.append(rsite_list[j])
                    newtg.append(new_tg[j])
                    oldtg.append(int(tg_list[j]))
                    sector.append(pre_stg_sector[j])
                    if k==0:
                       
                        temp1=f"rxmoi:mo=rxstg-{new_tg[j]},Sector={pre_stg_sector[j]},RSITE={rsite_list[j]};"
                        new_tg_defination_in_destination_bsc.append(temp1)
                        
                        temp2=f"rxesi:mo=rxstg-{new_tg[j]};"
                        tg_deblock_iu_destination_bsc_rxesi.append(temp2)

                        temp3=f"rxble:mo=rxstg-{new_tg[j]};"
                        tg_deblock_iu_destination_bsc_rxble.append(temp3)

                        if len(tf_softsync_dict[tg_list[j]].strip()) ==2:
                            temp4=f"RXMSC:MO=RXSTF-{new_tg[j]},FSOFFSET={int(tf_offset_dict[tg_list[j]])};"
                            temp5=f"rxtsi:mo=RXSTG-{(new_tg[j])},ALIGNTYPE={tf_aligntype_dict[tg_list[j]]};"
                        elif len(tf_softsync_dict[tg_list[j]].strip()) ==3:
                            temp4=""
                            temp5=""
                        
                        tf_offset.append(temp4)
                        softsync_dt.append(temp5)
                    else:
                        temp1=""
                        new_tg_defination_in_destination_bsc.append(temp1)

                        temp2=""
                        tg_deblock_iu_destination_bsc_rxesi.append(temp2)

                        temp3=""
                        tg_deblock_iu_destination_bsc_rxble.append(temp3)
                        
                        temp4=""
                        tf_offset.append(temp4)

                        temp5=""
                        softsync_dt.append(temp5)
                    
                    chgr_var=str(pre_chgr_list[j][k])
                    if len(chgr_var)==0:
                        chgr_var="NA"
                    temp2=f"rxtci:mo=rxstg-{new_tg[j]},cell={cell_input_list[j]},chgr={chgr_var};"
                    chgr_allocation_in_destination_bsc.append(temp2)

                    temp3=f"rlstc:cell={cell_input_list[j]},chgr={chgr_var},state=active;"
                    cell_active_in_destination_bsc.append(temp3)

                    temp4=f"rlstc:cell={cell_input_list[j]},chgr={chgr_var},state=halted;"
                    cell_halte_in_source_bsc.append(temp4)
                    
                    temp5=f"rxbli:mo={tg_list_rxstg[j]};"
                    tg_block_source_bsc_rxbli.append(temp5)

                    temp6=f"rxese:mo={tg_list_rxstg[j]};"
                    tg_block_source_bsc_rxese.append(temp6)
                
                else: 
                    rejected_cell_chgr.append(cell_input_list[j])

        pd.set_option('display.max_columns', None)
        dataframe_dictionary={"CELL_INPUT":cell_input,"CHGR":chgr,"RSITE":rsite,"Sector":sector,"NEW TG":newtg,"OLD TG":oldtg,"OFFSET":offset,"Softsync":softsync,"NEW_TG_defination_in_destination_bsc":new_tg_defination_in_destination_bsc,"chgr_allocation in destination bsc":chgr_allocation_in_destination_bsc,"tg deblock iu destination bsc (rxesi)":tg_deblock_iu_destination_bsc_rxesi,"tg deblock iu destination bsc (rxble)":tg_deblock_iu_destination_bsc_rxble,"cell active in destination bsc":cell_active_in_destination_bsc,"cell halte in source bsc":cell_halte_in_source_bsc,"TG block in source BSC (rxbli)":tg_block_source_bsc_rxbli,"TG block in source BSC (rxese)":tg_block_source_bsc_rxese,"TF_OFFSET":tf_offset,"SoftSync_DT":softsync_dt}
        df=pd.DataFrame(dataframe_dictionary)

        # print("\nlength of cell input: ",len(cell_input))
        # print("\nlength of chgr: ",len(chgr))
        # print("\nlength of rsite: ",len(rsite))
        # print("\nlength of newtg: ",len(newtg))
        # print("\nlength of oldtg: ",len(oldtg))
        # print("\nlength of new_tg_defination_in_destination_bsc: ",len(new_tg_defination_in_destination_bsc))
        # print("\nlength of chgr_allocation_in_destination_bsc: ",len(chgr_allocation_in_destination_bsc))
        # print("\nlength of tg_deblock_iu_destination_bsc_rxesi: ",len(tg_deblock_iu_destination_bsc_rxesi))
        # print("\nlength of tg_deblock_iu_destination_bsc_rxble: ",len(tg_deblock_iu_destination_bsc_rxble))
        # print("\nlength of cell_active_in_destination_bsc: ",len(cell_active_in_destination_bsc))
        # print("\nlength of cell_halte_in_source_bsc: ",len(cell_halte_in_source_bsc))
        # print("\nlength of tg_block_source_bsc_rxbli: ",len(tg_block_source_bsc_rxbli))
        # print("\nlength of tg_block_source_bsc_rxese: ",len(tg_block_source_bsc_rxese))

        # print("\n length of rsite_list: ",len(rsite))
        #print(df.head())
        workbook=rf'C:\RAN_Automations\RAN_IP_Site_Migration_Tool\IP_mig_dt-excel_file\IP_mig_dt_{date.today().strftime("%d-%m-%Y")}.xlsx'
        writer=pd.ExcelWriter(workbook,engine='xlsxwriter')
        df.to_excel(writer,sheet_name='Sheet 1',index=False)
        workbook=writer.book
        worksheet=writer.sheets['Sheet 1']

        red_headers=[1,2,3,5,6,7,8,14,15,16]
        green_headers=[4,9,10,11,12,13,17,18]

        format_red=workbook.add_format({'bold':True,'fg_color':'#ff1a1a','font_color':'#000000','border':1})
        format_green=workbook.add_format({'bold':True,'fg_color':'#00ff55','font_color':'#000000','border':1})
        header_format=workbook.add_format({'bold':True,'font_color':'#000000','border':1})

        for col_num, value in enumerate(df.columns.values):
            if col_num in red_headers:
                worksheet.write(0, col_num, value, format_red)
            elif col_num in green_headers:
                worksheet.write(0, col_num, value, format_green)
            else:
                worksheet.write(0, col_num, value, header_format)

            column_len = df[value].astype(str).str.len().max()
            column_len = max(column_len, len(value)) + 3
            worksheet.set_column(col_num, col_num, column_len)

        # for i in red_headers:
        #     worksheet.conditional_format(i,{'type':'no_blanks','format':format2})

        # for i in green_headers:
        #     worksheet.conditional_format(i,{'type':'no_blanks','format':format1})

        writer.save()
        writer.close()

        messagebox.showinfo("   File creation was successful",f'C:\RAN_Automations\RAN_IP_Site_Migration_Tool\IP_mig_dt-excel_file\IP_mig_dt_{date.today().strftime("%d-%m-%Y")}.xlsx was successfully created')

        



        ############################################################################################################
        ########################    C:\RAN_Automations\RAN_IP_Site_Migration_Tool\Date\Report_dt_{date.today().strftime("%d-%m-%Y")}.xlsx #################
        ############################################################################################################

        report_dict={"CELL_INPUT":cell_input,"CHGR":chgr,"Sector":sector,"RSITE":rsite,"NEW TG":newtg,"OLD TG":oldtg}
        report_df=pd.DataFrame(report_dict)

        workbook=rf'C:\RAN_Automations\RAN_IP_Site_Migration_Tool\Date\Report_dt_{date.today().strftime("%d-%m-%Y")}.xlsx'
        writer=pd.ExcelWriter(workbook,engine='xlsxwriter')
        report_df.to_excel(writer,sheet_name='Sheet 1',index=False)
        workbook=writer.book
        worksheet=writer.sheets['Sheet 1']

        red_headers=[1,2,3,5]
        green_headers=[4]

        format_red=workbook.add_format({'bold':True,'fg_color':'#ff1a1a','font_color':'#000000','border':1})
        format_green=workbook.add_format({'bold':True,'fg_color':'#00ff55','font_color':'#000000','border':1})
        header_format=workbook.add_format({'bold':True,'font_color':'#000000','border':1})

        for col_num, value in enumerate(report_df.columns.values):
            if col_num in red_headers:
                worksheet.write(0, col_num, value, format_red)
            elif col_num in green_headers:
                worksheet.write(0, col_num, value, format_green)
            else:
                worksheet.write(0, col_num, value, header_format)

            column_len = report_df[value].astype(str).str.len().max()
            column_len = max(column_len, len(value)) + 3
            worksheet.set_column(col_num, col_num, column_len)

        # for i in red_headers:
        #     worksheet.conditional_format(i,{'type':'no_blanks','format':format2})

        # for i in green_headers:
        #     worksheet.conditional_format(i,{'type':'no_blanks','format':format1})

        messagebox.showinfo("   File creation was successful",rf'C:\RAN_Automations\RAN_IP_Site_Migration_Tool\Date\Report_dt_{date.today().strftime("%d-%m-%Y")}.xlsx was successfully created')
            

        writer.save()
        writer.close()


        ##################################################################################################################################################
        ##############   C:\RAN_Automations\RAN_IP_Site_Migration_Tool\Destination\New_TG_Defination_in_destination_bsc-{}".format(date.today().strftime("%d-%m-%Y")) ###########################
        ##################################################################################################################################################

        fil=rf"C:\RAN_Automations\RAN_IP_Site_Migration_Tool\Destination\New_TG_Defination_in_destination_bsc-{tday}.txt"
        file=open(fil,'w')
        my_str=""
        for line in new_tg_defination_in_destination_bsc:
            my_str+=line+"\n"
        
        file.write(my_str)
        
        messagebox.showinfo("   File creation was successful",rf'C:\RAN_Automations\RAN_IP_Site_Migration_Tool\Destination\New_TG_Defination_in_destination_bsc-{date.today().strftime("%d-%m-%Y")}.txt was successfully created')
        

        ##################################################################################################################################################
        ##############   C:\RAN_Automations\RAN_IP_Site_Migration_Tool\Destination\CHGR_allocation_in_destination_bsc-{}.format(date.today().strftime("%d-%m-%Y")) ##############################
        ##################################################################################################################################################
        
        my_str=""
        for line in chgr_allocation_in_destination_bsc:
            my_str+=line+"\n"

        fil=rf"C:\RAN_Automations\RAN_IP_Site_Migration_Tool\Destination\CHGR_allocation_in_destination_bsc-{tday}.txt"

        file=open(fil,'w')
        file.write(my_str)

        messagebox.showinfo("   File creation was successful",rf'C:\RAN_Automations\RAN_IP_Site_Migration_Tool\Destination\CHGR_allocation_in_destination_bsc-{date.today().strftime("%d-%m-%Y")}.txt was successfully created')



        ##################################################################################################################################################
        ##############   C:\RAN_Automations\RAN_IP_Site_Migration_Tool\Destination\Tg_deblock_in_destination_bsc-{}.format(date.today().strftime("%d-%m-%Y")) ###################################
        ##################################################################################################################################################

        fil=rf"C:\RAN_Automations\RAN_IP_Site_Migration_Tool\Destination\Tg_deblock_in_destination_bsc-{tday}.txt"
        file=open(fil,"w")
        my_str=""

        for j in range(0,len(tg_deblock_iu_destination_bsc_rxesi)):
            line=tg_deblock_iu_destination_bsc_rxesi[j]
            line2=tg_deblock_iu_destination_bsc_rxble[j]
            my_str+=line+"\n"+line2+"\n"
        

        file.write(my_str)

        messagebox.showinfo("   File creation was successful",rf'C:\RAN_Automations\RAN_IP_Site_Migration_Tool\Destination\Tg_deblock_in_destination_bsc-{date.today().strftime("%d-%m-%Y")}.txt was successfully created')

        tday=date.today().strftime("%d-%m-%Y")
        
        ##################################################################################################################################################
        ##############   C:\RAN_Automations\RAN_IP_Site_Migration_Tool\Destination\Cell_active_destination_bsc-{}.format(date.today().strftime("%d-%m-%Y")) #####################################
        ##################################################################################################################################################

        fil=rf"C:\RAN_Automations\RAN_IP_Site_Migration_Tool\Destination\Cell_active_destination_bsc-{tday}.txt"
        my_str=""
        for line in cell_active_in_destination_bsc:
            my_str+=line+"\n"

        file=open(fil,'w')
        file.write(my_str)

        messagebox.showinfo("   File creation was successful",rf'C:\RAN_Automations\RAN_IP_Site_Migration_Tool\Destination\Cell_active_destination_bsc-{date.today().strftime("%d-%m-%Y")}.txt was successfully created')

        ##################################################################################################################################################
        ##############   C:\RAN_Automations\RAN_IP_Site_Migration_Tool\Destination\Cell_halte_in_source_bsc-{}.format(date.today().strftime("%d-%m-%Y")) ########################################
        ##################################################################################################################################################

        fil=rf"C:\RAN_Automations\RAN_IP_Site_Migration_Tool\Source\Cell_halte_in_source_bsc-{tday}.txt"
        my_str=""
        for line in cell_halte_in_source_bsc:
            my_str+=line+"\n"

        file=open(fil,'w')
        file.write(my_str)

        messagebox.showinfo("   File creation was successful",rf'C:\RAN_Automations\RAN_IP_Site_Migration_Tool\Source\Cell_halte_in_source_bsc-{date.today().strftime("%d-%m-%Y")}.txt was successfully created')

        ##################################################################################################################################################
        ##############   C:\RAN_Automations\RAN_IP_Site_Migration_Tool\Source\Tg_block_in_source_bsc-{}.format(date.today().strftime("%d-%m-%Y")) ###############################################
        ##################################################################################################################################################
        
        fil=rf"C:\RAN_Automations\RAN_IP_Site_Migration_Tool\Source\Tg_block_in_source_bsc-{tday}.txt"
        file=open(fil,"w")
        my_str=""

        for j in range(0,len(tg_block_source_bsc_rxbli)):
            line=tg_block_source_bsc_rxbli[j]
            line2=tg_block_source_bsc_rxese[j]
            my_str+=line+"\n"+line2+"\n"
        

        file.write(my_str)

        messagebox.showinfo("   File creation was successful",rf'C:\RAN_Automations\RAN_IP_Site_Migration_Tool\RAN_IP_Site_Migration_Tool\Source\Tg_block_in_source_bsc-{date.today().strftime("%d-%m-%Y")}.txt was successfully created')

        ##################################################################################################################################################
        ##############   C:\RAN_Automations\RAN_IP_Site_Migration_Tool\Destination\Softsync_dt-{}.format(date.today().strftime("%d-%m-%Y")) #####################################################
        ##################################################################################################################################################
        fil=rf"C:\RAN_Automations\RAN_IP_Site_Migration_Tool\Destination\Softsync_dt-{tday}.txt"
        my_str=""
        for j in range(0,len(softsync_dt)):
            line=tf_offset[j]
            line2=softsync_dt[j]
            if line==" ":
                continue
            else:
                my_str+=line+"\n"+line2+"\n"
        
        file=open(fil,"w")
        file.write(my_str)
        messagebox.showinfo("   File creation was successful",rf'C:\RAN_Automations\RAN_IP_Site_Migration_Tool\Destination\Softsync_dt-{date.today().strftime("%d-%m-%Y")}.txt was successfully created')

        file.close()
        file2.close()
        file3.close()

        if len(set(rejected_cell_chgr))>0:
            messagebox.showwarning("    Set of cells which was not included in scripts",list(set(rejected_cell_chgr)).sort())
        
        if len(rejected_cell_chgr)>0:
            messagebox.showwarning("    Cells for which we can't create commands",list(set(rejected_cell_chgr)))
            messagebox.showinfo("   File to see the rejected cells",r"C:\RAN_Automations\RAN_IP_Site_Migration_Tool\Error_cells.txt")
            my_str=""
            for text in list(set(rejected_cell_chgr)):
                my_str+=text+"\n"
            file=open(rf"C:\RAN_Automations\RAN_IP_Site_Migration_Tool\Error_cells_{date.today().strftime('%d-%m-%Y')}.txt","w")
            file.write(my_str)
        messagebox.showinfo("   Successful execution","All the files were successfully created")

    except Exception as e:
        messagebox.showerror("  Exception Occurred",e)
        