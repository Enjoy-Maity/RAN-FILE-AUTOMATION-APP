from ast import Delete
from tkinter import * 
from tkinter import messagebox
from PIL import ImageTk,Image
from tkinter import filedialog
import tkinter.ttk as ttk
from turtle import bgcolor
import RAN_IP_Site_Migration_Script_Tool
import json_file_creation
import os
import sys

class App:
    def __init__(self,main_win):
        self.main_win=main_win
        self.main_win.title("   RAN Automation Scripts Tool")
        self.main_win.resizable(0,0)
        self.main_win.geometry("770x432")
        self.style=ttk.Style()
        self.main_win.bind("<Escape>",self.quit)
        self.style.theme_use("vista")
        self.style.theme_settings("vista",{
            "TButton" : {
                "configure":{"padding":2},
    
                }
            }
        )


        self.current_file=__file__
        self.current_folder=self.current_file[0:len(self.current_file)-7]

        self.main_win_bg=ImageTk.PhotoImage(Image.open(self.current_folder+"images\MicrosoftTeams-image.png"))
        self.main_win_canvas=Canvas(self.main_win,width=770,height=432,bd=0, highlightthickness=0, relief='ridge')
        self.main_win.iconbitmap(self.current_folder+"images\ericsson-blue-icon-logo.ico")
        self.main_win_canvas.grid(row=0,column=0,columnspan=4,sticky=NW)

        self.options=["Select a task to start                           ","1. RAN IP Site Migration Script Tool","2. Json File Creation Script Tool         "]
        self.main_win_drop_down_var=StringVar()
        self.main_win_drop_down_var.set("Select a task to start")
        self.main_win_drop_down=ttk.OptionMenu(self.main_win,self.main_win_drop_down_var,*self.options)

        self.main_win_btn=ttk.Button(self.main_win,text="Submit",command=lambda:self.submit(1))
        self.main_win_btn.bind("<Return>",self.submit)
        self.main_win_canvas.create_image(0,0,image=self.main_win_bg,anchor='nw')
        self.main_win_canvas.create_window(560,300,anchor="se",window=self.main_win_drop_down)
        self.main_win_canvas.create_window(650,302,anchor="se",window=self.main_win_btn)

        self.main_win.mainloop()

    def submit(self,event):
        self.my_str=str(self.main_win_drop_down_var.get())
        if self.my_str=="1. RAN IP Site Migration Script Tool":
            self.Ran_IP_Site_Migration_Script_Tool()
        
        elif self.my_str=="2. Json File Creation Script Tool         ":
            self.json_file_creation_script()
    
    def json_file_creation_script(self):
        self.master1=Toplevel(self.main_win)
        self.main_win.withdraw()
        self.master1.title("    Json File Creation Script Tool")
        self.master1.config(bg="#00008B")
        self.master1.bind("<Escape>",self.quit_json_file_creation_tool)
        self.master1.iconbitmap(self.current_folder+"images\ericsson-blue-icon-logo.ico")
        self.master1.geometry("750x510")
        self.master1.resizable(0,0)

        file_dir=["c:\\RAN\\JSON"]
        if not os.path.exists("c:\\RAN"):
             os.mkdir("c:\\RAN")
        
        for j in range(0,len(file_dir)):
            if os.path.exists(file_dir[j]):
                for file_name in os.listdir(file_dir[j]):
                    file=file_dir[j]+"\\"+file_name
                    if os.path.isfile(file):
                        os.remove(file)
            else:
                os.mkdir(file_dir[j])

        ####################################### JSON Excel File Extraction  ######################################################
        
        self.json_excel_file=""
        self.json_excel_text=ttk.Entry(self.master1,width=50)
        self.json_excel_label=ttk.Label(self.master1,text="Excel File For Json Creation",font=("Roboto 12 bold"),foreground="#FFFFFF",background="#00008B")
        self.json_excel_btn= ttk.Button(self.master1,text="Browse",command=self.get_json_excel)
        Label(self.master1,background="#00008B").grid(row=0,column=0,pady=10)

        self.json_excel_text.grid(row=1,column=2,padx=20,ipadx=10)
        self.json_excel_label.grid(row=1,column=0,padx=10,ipadx=10,columnspan=2)
        self.json_excel_btn.grid(row=1,column=3)
        Label(self.master1,background="#00008B").grid(row=2,column=0,pady=10)

        
        ###################################### JSON Text File Extraction #########################################################

        self.json_bsc_text_file=""
        self.json_bsc_text=ttk.Entry(self.master1,width=50)
        self.json_bsc_label=ttk.Label(self.master1,text="Base Stations ENM Cell Dump",font=("Roboto 12 bold"),foreground="#FFFFFF",background="#00008B")
        self.json_bsc_btn= ttk.Button(self.master1,text="Browse",command=self.get_json_bsc_cell_dump)
        Label(self.master1,background="#00008B").grid(row=3,column=0,pady=10)

        self.json_bsc_text.grid(row=4,column=2,padx=20,ipadx=10)
        self.json_bsc_label.grid(row=4,column=0,padx=10,ipadx=10,columnspan=2)
        self.json_bsc_btn.grid(row=4,column=3)
        Label(self.master1,background="#00008B").grid(row=5,column=0,pady=10)

        ############################## Button For Execution ##########################
        
        start_execution=ttk.Button(self.master1,text="Prepare JSON Script",command=self.start_json_file_creation)
        start_execution.grid(row=17,column=0,columnspan=3,pady=20,ipadx=50,padx=10,sticky=W+E)
        Label(self.master1,background="#00008B").grid(row=6,column=0,pady=30)

        exit_btn=ttk.Button(self.master1,text="Exit",command=lambda:self.quit_json_file_creation_tool(1))
        exit_btn.grid(row=17, column=3,sticky=E)




        #####################################  JSON Drafted By  ##################################################################
        Label(self.master1,background="#00008B").grid(row=6,column=0,pady=80)
        self.drafted_by_label_0=ttk.Label(self.master1,text="              Drafted By:",font=("Roboto 15 bold"),anchor=CENTER,foreground="#ffffff",background="#00008B")
        self.drafted_by_label_1=ttk.Label(self.master1,text=" Rohit Singla R | Saurabh S. | Enjoy Maity",font=("Roboto 12"),anchor=CENTER,foreground="#ffffff",background="#00008B")
        
        #Label(self.master,pady=7,foreground="#ffffff",background="#00008B").grid(row=9)
        self.drafted_by_label_0.grid(row=19,column=1)
        self.drafted_by_label_1.grid(row=19,column=2,columnspan=2,padx=20,ipadx=20,sticky=E)

        
        self.master1.mainloop()
        if self.master1.state()!="normal":
            sys.exit(0)
        
    def Ran_IP_Site_Migration_Script_Tool(self):
        self.master=Toplevel(self.main_win)
        self.main_win.withdraw()
        self.master.title("    RAN IP Site Migration Script Tool")
        self.master.config(bg="#00008B")
        self.master.bind("<Escape>",self.quit_RAN_IP_Site_Migration_Tool)
        self.master.iconbitmap(self.current_folder+"images\ericsson-blue-icon-logo.ico")
        self.master.geometry("720x510")
        self.master.resizable(0,0)     # cannot resize the window
    
        
        file_dir=["c:\\RAN\\Date","c:\\RAN\\Destination","c:\\RAN\\Source","c:\\RAN\\IP_mig_dt-excel_file"]
        if not os.path.exists("c:\\RAN"):
             os.mkdir("c:\\RAN")
        
        for j in range(0,len(file_dir)):
            if os.path.exists(file_dir[j]):
                for file_name in os.listdir(file_dir[j]):
                    file=file_dir[j]+"\\"+file_name
                    if os.path.isfile(file):
                        os.remove(file)
            else:
                os.mkdir(file_dir[j])

        ################# Planned Cell input #######################################

        self.planned_cells=""

        self.list_of_planned_cells_Label=ttk.Label(self.master,text="List of Planned Cells",font=("Roboto 12 bold"),foreground="#FFFFFF",background="#00008B")
        self.list_of_planned_cells_Entry=ttk.Entry(self.master,width=50)
        self.list_of_planned_cells_Browse=ttk.Button(self.master,text="Browse",command=self.list_of_planned_cells_get)

        self.list_of_planned_cells_Entry.grid(row=0,column=2,padx=20,ipadx=10)
        self.list_of_planned_cells_Label.grid(row=0,column=0,padx=10,pady=40,ipadx=10,columnspan=2)
        self.list_of_planned_cells_Browse.grid(row=0,column=3)

        ##################### Pre File #############################################

        self.file_name=" "
        self.pre_log_fetch_entry=ttk.Entry(self.master,width=50)

        
        self.pre_log_fetch_label_1=ttk.Label(self.master,text="Source BSC Logs File",font="Roboto 12 bold",background="#00008B",foreground="#ffffff")
        self.pre_log_fetch_label_2=ttk.Label(self.master,text="Info: Logs of:rxmop:moty=rxstg;|rxtcp:moty=rxstg;",font=("Roboto 9"),background="#00008B",foreground="#ffffff")

        
        
        self.pre_log_fetch_button=ttk.Button(self.master,text="Browse",command=self.pre_log_fetch)
        

        self.pre_log_fetch_label_1.grid(row=1,column=0,padx=10,ipadx=10,columnspan=2)
        self.pre_log_fetch_label_2.grid(row=2,column=2,padx=20,ipadx=10,columnspan=2)
        self.pre_log_fetch_entry.grid(row=1,column=2,padx=20,ipadx=10)
        self.pre_log_fetch_button.grid(row=1,column=3)

        ##################### Post File #############################################

        self.file_name_post=" "

        self.post_log_fetch_entry=ttk.Entry(self.master,width=50)

        self.post_log_fetch_label_1=ttk.Label(self.master,text="Destination BSC Logs File",font="Roboto 12 bold",foreground="#ffffff",background="#00008B")
        self.post_log_fetch_label_2=ttk.Label(self.master,text="Info: Logs of: rxmop:moty=rxstg;|rxmop:moty=rxotg;",font=("Roboto 9"),foreground="#ffffff",background="#00008B")

        self.post_log_fetch_button=ttk.Button(self.master,text="Browse",command=self.post_log_fetch)

        self.post_log_fetch_label_1.grid(row=4,column=0,padx=15,ipadx=10,columnspan=2)
        Label(self.master,background="#00008B").grid(row=3,pady=10)
        self.post_log_fetch_label_2.grid(row=5,column=2,padx=20,ipadx=10,columnspan=2)
        self.post_log_fetch_entry.grid(row=4,column=2,padx=20,ipadx=10)
        self.post_log_fetch_button.grid(row=4,column=3)

        ############################ TF fetch ########################################

        Label(self.master,background="#00008B").grid(row=9,column=0)

        self.tf_file_name=" "

        self.tf_fetch_entry=ttk.Entry(self.master,width=50)

        self.tf_fetch_label_1=ttk.Label(self.master,text="Source BSC TF Logs",font="Roboto 12 bold",foreground="#ffffff",background="#00008B")
        self.tf_fetch_label_2=ttk.Label(self.master,text="Info: rxmop:moty=rxstf | rxtsp:moty=rxstg;",font=("Roboto 9"),foreground="#ffffff",background="#00008B")

        self.tf_fetch_button=ttk.Button(self.master,text="Browse",command=self.tf_fetch)

        self.tf_fetch_label_1.grid(row=10,column=0,padx=15,ipadx=10,columnspan=2)
        Label(self.master,background="#00008B").grid(row=12,pady=10)
        self.tf_fetch_label_2.grid(row=11,column=2,padx=20,ipadx=10,columnspan=2)
        self.tf_fetch_entry.grid(row=10,column=2,padx=20,ipadx=10)
        self.tf_fetch_button.grid(row=10,column=3)

        ############################## Button For Execution ##########################
        
        start_execution=ttk.Button(self.master,text="Prepare Scripts",command=self.startwork)
        start_execution.grid(row=17,column=0,columnspan=3,pady=40,ipadx=50,padx=10,sticky=W+E)

        exit_btn=ttk.Button(self.master,text="Exit",command=lambda:self.quit_RAN_IP_Site_Migration_Tool(1))
        exit_btn.grid(row=17, column=3,sticky=E)

        ################# Drafted by ##################################
        Label(self.master,background="#00008B").grid(row=18,column=0)
        self.drafted_by_label_0=ttk.Label(self.master,text="              Drafted By:",font=("Roboto 15 bold"),anchor=CENTER,foreground="#ffffff",background="#00008B")
        self.drafted_by_label_1=ttk.Label(self.master,text=" Rohit Singla R | Saurabh S. | Enjoy Maity",font=("Roboto 12"),anchor=CENTER,foreground="#ffffff",background="#00008B")
        
        #Label(self.master,pady=7,foreground="#ffffff",background="#00008B").grid(row=9)
        self.drafted_by_label_0.grid(row=19,column=1)
        self.drafted_by_label_1.grid(row=19,column=2,columnspan=2,padx=20,ipadx=20,sticky=E)
        
        self.master.mainloop()
    
    def pre_log_fetch(self):
        self.pre_log_fetch_entry.delete(0,END)
        self.my_string=filedialog.askopenfilename(initialdir="C:\\",title=" Choose the prelogs file",filetypes=(("Text files","*.txt"),("All Files","*.*")))
        self.file_name=self.my_string
        self.pre_log_fetch_entry.insert(0,self.file_name)
    
    def post_log_fetch(self):
        self.post_log_fetch_entry.delete(0,END)
        self.my_string=filedialog.askopenfilename(initialdir="C:\\",title=" Choose the postlogs file",filetypes=(("Text files","*.txt"),("All Files","*.*")))
        self.file_name_post=self.my_string
        self.post_log_fetch_entry.insert(0,self.file_name_post)
    
    def tf_fetch(self):
        self.tf_fetch_entry.delete(0,END)   # Deletes the entry on the entry
        self.my_string=filedialog.askopenfilename(initialdir="C:\\",title=" Choose the postlogs file",filetypes=(("Text files","*.txt"),("All Files","*.*")))
        self.tf_file_name=self.my_string
        self.tf_fetch_entry.insert(0,self.tf_file_name)
    
    def startwork(self):
        RAN_IP_Site_Migration_Script_Tool.task(self.file_name,self.file_name_post,self.planned_cells,self.tf_file_name)
    
    def list_of_planned_cells_get(self):
        self.list_of_planned_cells_Entry.delete(0,END)
        self.my_string=filedialog.askopenfilename(initialdir="C:\RAN",title=" Choose the Planned Cell txt",filetypes=(("Text Files","*.txt"),("All Files","*.*")))
        self.list_of_planned_cells_Entry.insert(0,self.my_string)
        self.planned_cells=self.my_string
    
    def get_json_excel(self):
        self.json_excel_text.delete(0,END)
        self.my_string=filedialog.askopenfilename(initialdir="C:\RAN",title=" Choose the Excel File to Get New Lac",filetypes=(("Excel files (.xlsx)","*.xlsx"),("Excel files (.xls)","*.xls"),("All Files","*.*")))
        self.json_excel_text.insert(0,self.my_string)
        self.json_excel_file=self.my_string
    
    def get_json_bsc_cell_dump(self):
        self.json_bsc_text.delete(0,END)
        self.my_string=filedialog.askopenfilename(initialdir="C:\RAN",title=" Choose the BSC Cell Dump File ",filetypes=(("Text files (.txt)","*.txt"),("All Files","*.*")))
        self.json_bsc_text.insert(0,self.my_string)
        self.json_bsc_text_file=self.my_string

    def start_json_file_creation(self):
        json_file_creation.task(self.json_excel_file,self.json_bsc_text_file)

    def quit_json_file_creation_tool(self,event):
        self.master1.destroy()
        self.main_win.deiconify()

    def quit_RAN_IP_Site_Migration_Tool(self,event):
        self.master.destroy()
        self.main_win.deiconify()

    def quit(self,event):
        self.main_win.destroy()
        self.main_win.protocol("WM_DELETE_WINDOW",self.destroy_everything)

    def destroy_everything(self):
        if self.main_win.state()!='normal':
            sys.exit(0)

    

def main():
    root=Tk()
    try:
        
        app=App(root)
        
    
    except Exception as e:
         messagebox.showerror("  Exception Occured",e)

if __name__=="__main__":
    main()