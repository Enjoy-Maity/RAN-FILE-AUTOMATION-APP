import re
import shutil
import pandas as pd
import xlsxwriter
from datetime import date
import os 
from tkinter import messagebox


def task(prelogfile,postlogfile,planned_cells):
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
        
        modified_planned_cells_reader=list(set(modified_planned_cells_reader))
        

        for i in range(0,len(modified_pre_reader)):
            if len(re.findall("\AEND",modified_pre_reader[i])):
                break

        pre_stg_dict=dict()     # dictionary cell-input/sector:stg
        pre_chgr_dict=dict()    # dictionary cell-input/sector:chgr
        pre_stg_rsite=dict()    # dictionary cell_input/sector:rsite
        for j in range(i, len(modified_pre_reader)):
            line=modified_pre_reader[j].split()
            if len(re.findall("\ARXSTG",modified_pre_reader[j]))>0:
                if line[1] in modified_planned_cells_reader:
                    pre_stg_dict[line[1]]=line[0]
                    pre_chgr_dict[line[1]]=list() 
                    pre_chgr_dict[line[1]].append(line[2])
            
            elif len(line)>0 and modified_pre_reader[j].split()[0] in pre_chgr_dict:
                pre_chgr_dict[line[0]].append(line[1])
        for j in range(0,i+1):
            line=modified_pre_reader[j].split()
            if len(re.findall("\ARXSTG",modified_pre_reader[j]))>0 and line[1] in pre_chgr_dict:
                pre_stg_rsite[line[1]]=line[2]

        tg_list=list(pre_stg_dict.values())         # getting the list of all the prelog tg
        rsite_list=list(pre_stg_rsite.values())     # getting the list of all the prelog rsite
        cell_input_list=list(pre_stg_dict.keys())   # getting the list of all cell-input/sectors

        for j in range(0,len(tg_list)):
            tg_list[j]=tg_list[j].lower()


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



        pre_chgr_list=list(pre_chgr_dict.values())
        for j in range(0,len(pre_chgr_list)):
            for k in range(0,len(pre_chgr_list[j])):
                cell_input.append(cell_input_list[j])
                chgr.append(pre_chgr_list[j][k])
                rsite.append(rsite_list[j])
                newtg.append(new_tg[j])
                oldtg.append(int(tg_list[j][6:]))
                if k==0:
                    temp1=f"rxmoi:mo=rxstg-{new_tg[j]},Sector={cell_input_list[j][0:6]}_{cell_input_list[j][6:]},RSITE={rsite_list[j]};"
                    new_tg_defination_in_destination_bsc.append(temp1)
                    
                    temp2=f"rxesi:mo=rxstg-{new_tg[j]};"
                    tg_deblock_iu_destination_bsc_rxesi.append(temp2)

                    temp3=f"rxble:mo=rxstg-{new_tg[j]};"
                    tg_deblock_iu_destination_bsc_rxble.append(temp3)

                else:
                    temp1=""
                    new_tg_defination_in_destination_bsc.append(temp1)

                    temp2=""
                    tg_deblock_iu_destination_bsc_rxesi.append(temp2)

                    temp3=""
                    tg_deblock_iu_destination_bsc_rxble.append(temp3)
                
                temp2=f"rxtci:mo=rxstg-{new_tg[j]},cell={cell_input_list[j]},chgr={pre_chgr_list[j][k]};"
                chgr_allocation_in_destination_bsc.append(temp2)

                temp3=f"rlstc:cell={cell_input_list[j]},chgr={pre_chgr_list[j][k]},state=active;"
                cell_active_in_destination_bsc.append(temp3)

                temp4=f"rlstc:cell={cell_input_list[j]},chgr={pre_chgr_list[j][k]},state=halted;"
                cell_halte_in_source_bsc.append(temp4)
                
                temp5=f"rxbli:mo={tg_list[j]};"
                tg_block_source_bsc_rxbli.append(temp5)

                temp6=f"rxese:mo={tg_list[j]};"
                tg_block_source_bsc_rxese.append(temp6)

        pd.set_option('display.max_columns', None)
        dataframe_dictionary={"CELL_INPUT":cell_input,"CHGR":chgr,"RSITE":rsite,"NEW TG":newtg,"OLD TG":oldtg,"NEW_TG_defination_in_destination_bsc":new_tg_defination_in_destination_bsc,"chgr_allocation in destination bsc":chgr_allocation_in_destination_bsc,"tg deblock iu destination bsc (rxesi)":tg_deblock_iu_destination_bsc_rxesi,"tg deblock iu destination bsc (rxble)":tg_deblock_iu_destination_bsc_rxble,"cell active in destination bsc":cell_active_in_destination_bsc,"cell halte in source bsc":cell_halte_in_source_bsc,"TG block in source BSC (rxbli)":tg_block_source_bsc_rxbli,"TG block in source BSC (rxese)":tg_block_source_bsc_rxese}
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
        workbook=rf'C:\RAN\IP_mig_dt-excel_file\IP_mig_dt_{date.today().strftime("%d-%m-%Y")}.xlsx'
        writer=pd.ExcelWriter(workbook,engine='xlsxwriter')
        df.to_excel(writer,sheet_name='Sheet 1',index=False)
        workbook=writer.book
        worksheet=writer.sheets['Sheet 1']

        red_headers=[1,2,4,10,11,12]
        green_headers=[3,5,6,7,8,9]

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

        messagebox.showinfo("   File creation was successful",f'C:\RAN\IP_mig_dt-excel_file\IP_mig_dt_{date.today().strftime("%d-%m-%Y")}.xlsx was successfully created')

        



        ############################################################################################################
        ########################    C:\RAN\Date\Report_dt_{date.today().strftime("%d-%m-%Y")}.xlsx #################
        ############################################################################################################

        report_dict={"CELL_INPUT":cell_input,"CHGR":chgr,"RSITE":rsite,"NEW TG":newtg,"OLD TG":oldtg}
        report_df=pd.DataFrame(report_dict)

        workbook=rf'C:\RAN\Date\Report_dt_{date.today().strftime("%d-%m-%Y")}.xlsx'
        writer=pd.ExcelWriter(workbook,engine='xlsxwriter')
        report_df.to_excel(writer,sheet_name='Sheet 1',index=False)
        workbook=writer.book
        worksheet=writer.sheets['Sheet 1']

        red_headers=[1,2,4]
        green_headers=[3]

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

        messagebox.showinfo("   File creation was successful",rf'C:\RAN\Date\Report_dt_{date.today().strftime("%d-%m-%Y")}.xlsx was successfully created')
            

        writer.save()
        writer.close()


        ##################################################################################################################################################
        ##############   C:\RAN\Destination\New_TG_Defination_in_destination_bsc-{}".format(date.today().strftime("%d-%m-%Y")) ###########################
        ##################################################################################################################################################

        fil=rf"C:\RAN\Destination\New_TG_Defination_in_destination_bsc-{tday}.txt"
        file=open(fil,'w')
        my_str=""
        for line in new_tg_defination_in_destination_bsc:
            my_str+=line+"\n"
        
        file.write(my_str)
        
        messagebox.showinfo("   File creation was successful",rf'C:\RAN\Destination\New_TG_Defination_in_destination_bsc-{date.today().strftime("%d-%m-%Y")}.txt was successfully created')
        

        ##################################################################################################################################################
        ##############   C:\RAN\Destination\CHGR_allocation_in_destination_bsc-{}.format(date.today().strftime("%d-%m-%Y")) ##############################
        ##################################################################################################################################################
        
        my_str=""
        for line in chgr_allocation_in_destination_bsc:
            my_str+=line+"\n"

        fil=rf"C:\RAN\Destination\CHGR_allocation_in_destination_bsc-{tday}.txt"

        file=open(fil,'w')
        file.write(my_str)

        messagebox.showinfo("   File creation was successful",rf'C:\RAN\Destination\CHGR_allocation_in_destination_bsc-{date.today().strftime("%d-%m-%Y")}.txt was successfully created')



        ##################################################################################################################################################
        ##############   C:\RAN\Destination\Tg_deblock_in_destination_bsc-{}.format(date.today().strftime("%d-%m-%Y")) ###################################
        ##################################################################################################################################################

        fil=rf"C:\RAN\Destination\Tg_deblock_in_destination_bsc-{tday}.txt"
        file=open(fil,"w")
        my_str=""

        for j in range(0,len(tg_deblock_iu_destination_bsc_rxesi)):
            line=tg_deblock_iu_destination_bsc_rxesi[j]
            line2=tg_deblock_iu_destination_bsc_rxble[j]
            my_str+=line+"\n"+line2+"\n\n"
        

        file.write(my_str)

        messagebox.showinfo("   File creation was successful",rf'C:\RAN\Destination\Tg_deblock_in_destination_bsc-{date.today().strftime("%d-%m-%Y")}.txt was successfully created')

        tday=date.today().strftime("%d-%m-%Y")
        
        ##################################################################################################################################################
        ##############   C:\RAN\Destination\Cell_active_destination_bsc-{}.format(date.today().strftime("%d-%m-%Y")) #####################################
        ##################################################################################################################################################

        fil=rf"C:\RAN\Destination\Cell_active_destination_bsc-{tday}.txt"
        my_str=""
        for line in cell_active_in_destination_bsc:
            my_str+=line+"\n"

        file=open(fil,'w')
        file.write(my_str)

        messagebox.showinfo("   File creation was successful",rf'C:\RAN\Destination\Cell_active_destination_bsc-{date.today().strftime("%d-%m-%Y")}.txt was successfully created')

        ##################################################################################################################################################
        ##############   C:\RAN\Destination\Cell_halte_in_source_bsc-{}.format(date.today().strftime("%d-%m-%Y")) ########################################
        ##################################################################################################################################################

        fil=rf"C:\RAN\Source    \Cell_halte_in_source_bsc-{tday}.txt"
        my_str=""
        for line in cell_halte_in_source_bsc:
            my_str+=line+"\n"

        file=open(fil,'w')
        file.write(my_str)

        messagebox.showinfo("   File creation was successful",rf'C:\RAN\Source\Cell_halte_in_source_bsc-{date.today().strftime("%d-%m-%Y")}.txt was successfully created')

        ##################################################################################################################################################
        ##############   C:\RAN\Source\Tg_block_in_source_bsc-{}.format(date.today().strftime("%d-%m-%Y")) ##################################################
        ##################################################################################################################################################
        
        fil=rf"C:\RAN\Source\Tg_block_in_source_bsc-{tday}.txt"
        file=open(fil,"w")
        my_str=""

        for j in range(0,len(tg_block_source_bsc_rxbli)):
            line=tg_block_source_bsc_rxbli[j]
            line2=tg_block_source_bsc_rxese[j]
            my_str+=line+"\n"+line2+"\n\n"
        

        file.write(my_str)

        messagebox.showinfo("   File creation was successful",rf'C:\RAN\Source\Tg_block_in_source_bsc-{date.today().strftime("%d-%m-%Y")}.txt was successfully created')



        file.close()

        messagebox.showinfo("   Successful execution","All the files were successfully created")

    except Exception as e:
        messagebox.showerror("  Exception Occurred",e)
        