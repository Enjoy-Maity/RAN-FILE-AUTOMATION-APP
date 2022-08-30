from tkinter import * 
from tkinter import messagebox
from tkinter import filedialog
import tkinter.ttk as ttk
from turtle import bgcolor
import task
import os
import shutil
class App:
    def __init__(self,master):
        self.master=master
        self.master.title("    RAN IP Site Migration Script Tool")
        self.master.config(bg="#2905a1")
        current_file=__file__
        current_folder=current_file[0:len(current_file)-7]
        self.master.bind("<Escape>",self.quit)
        self.master.iconbitmap(current_folder+"images\ericsson-logo.ico")
        self.master.geometry("690x400")
        self.master.resizable(0,0)     # cannot resize the window
    
        self.style=ttk.Style()

        self.style.theme_use("vista")
        self.style.theme_settings("vista",{
            "TButton" : {
                "configure":{"padding":2},
    
                }
            }
        )

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

        self.list_of_planned_cells_Label=ttk.Label(self.master,text="List of planned cells",font=("Arial 10 bold"),foreground="#FFFFFF",background="#2905a1")
        self.list_of_planned_cells_Entry=ttk.Entry(self.master,width=50)
        self.list_of_planned_cells_Browse=ttk.Button(self.master,text="Browse",command=self.list_of_planned_cells_get)

        self.list_of_planned_cells_Entry.grid(row=0,column=2,padx=20,ipadx=10)
        self.list_of_planned_cells_Label.grid(row=0,column=0,padx=10,pady=40,ipadx=10,columnspan=2)
        self.list_of_planned_cells_Browse.grid(row=0,column=3)

        ##################### Pre File #############################################

        self.file_name=" "
        self.pre_log_fetch_entry=ttk.Entry(self.master,width=50)

        
        self.pre_log_fetch_label_1=ttk.Label(self.master,text="Source BSC Log File",font="Arial 10 bold",background="#2905a1",foreground="#ffffff")
        self.pre_log_fetch_label_2=ttk.Label(self.master,text="Info: Logs of:rxmop:moty=rxstg;|rxtcp:moty=rxstg;",background="#2905a1",foreground="#ffffff")

        
        
        self.pre_log_fetch_button=ttk.Button(self.master,text="Browse",command=self.pre_log_fetch)
        

        self.pre_log_fetch_label_1.grid(row=1,column=0,padx=10,ipadx=10,columnspan=2)
        self.pre_log_fetch_label_2.grid(row=2,column=2,padx=20,ipadx=10,columnspan=2)
        self.pre_log_fetch_entry.grid(row=1,column=2,padx=20,ipadx=10)
        self.pre_log_fetch_button.grid(row=1,column=3)

        ##################### Post File #############################################

        self.file_name_post=" "

        self.post_log_fetch_entry=ttk.Entry(self.master,width=50)

        self.post_log_fetch_label_1=ttk.Label(self.master,text="Destination BSC logs File",font="Arial 10 bold",foreground="#ffffff",background="#2905a1")
        self.post_log_fetch_label_2=ttk.Label(self.master,text="Info: Logs of: rxmop:moty=rxstg;|rxmop:moty=rxotg",foreground="#ffffff",background="#2905a1")

        self.post_log_fetch_button=ttk.Button(self.master,text="Browse",command=self.post_log_fetch)

        self.post_log_fetch_label_1.grid(row=4,column=0,padx=15,ipadx=10,columnspan=2)
        Label(self.master,background="#2905a1").grid(row=3,pady=10)
        self.post_log_fetch_label_2.grid(row=5,column=2,padx=20,ipadx=10,columnspan=2)
        self.post_log_fetch_entry.grid(row=4,column=2,padx=20,ipadx=10)
        self.post_log_fetch_button.grid(row=4,column=3)

        ################ Button For Execution ##########################
        start_execution=ttk.Button(self.master,text="Prepare Scripts",command=self.startwork)
        start_execution.grid(row=6,column=0,columnspan=3,pady=40,ipadx=50,padx=10,sticky=W+E)

        exit_btn=ttk.Button(self.master,text="Exit",command=lambda:self.quit(0))
        exit_btn.grid(row=6, column=3,sticky=E)

        ################# Drafted by ##################################
        self.drafted_by_label_0=ttk.Label(self.master,text="        Drafted By:-",font=("Arial 10 bold"),anchor=CENTER,foreground="#ffffff",background="#2905a1")
        self.drafted_by_label_1=ttk.Label(self.master,text="        Rohit Singla R,  Saurabh S.,  Enjoy Maity",font=("Arial 10"),anchor=CENTER,foreground="#ffffff",background="#2905a1")
        # self.drafted_by_label_2=ttk.Label(self.master,text="    Saurabh S.",font=("Arial 10"),anchor=CENTER,foreground="#ffffff",background="#2905a1")
        # self.drafted_by_label_3=ttk.Label(self.master,text="Enjoy Maity",font=("Arial 10"),anchor=CENTER,foreground="#ffffff",background="#2905a1")
        
        Label(self.master,pady=7,foreground="#ffffff",background="#2905a1").grid(row=9)
        self.drafted_by_label_0.grid(row=10,column=1)
        self.drafted_by_label_1.grid(row=10,column=2,columnspan=2,padx=20,ipadx=20,sticky=E)
        # self.drafted_by_label_2.grid(row=10,column=2,padx=5,sticky=E+W)
        # self.drafted_by_label_3.grid(row=10,column=3,padx=5,sticky=W)
    
    def pre_log_fetch(self):
        self.my_string=filedialog.askopenfilename(initialdir="C:\\",title=" Choose the prelogs file",filetypes=(("Text files","*.txt"),("All Files","*.*")))
        self.file_name=self.my_string
        self.pre_log_fetch_entry.insert(0,self.file_name)
    
    def post_log_fetch(self):
        self.my_string=filedialog.askopenfilename(initialdir="C:\\",title=" Choose the postlogs file",filetypes=(("Text files","*.txt"),("All Files","*.*")))
        self.file_name_post=self.my_string
        self.post_log_fetch_entry.insert(0,self.file_name_post)
    
    def startwork(self):
        task.task(self.file_name,self.file_name_post,self.planned_cells)
    
    def list_of_planned_cells_get(self):
        self.my_string=filedialog.askopenfilename(initialdir="C:\RAN",title=" Choose the planned cell txt",filetypes=(("Text Files","*.txt"),("All Files","*.*")))
        self.list_of_planned_cells_Entry.insert(0,self.my_string)
        self.planned_cells=self.my_string

    def quit(self,event):
        self.master.destroy()

    

def main():
    root=Tk()
    # try:
        
    #     app=App(root)
        
    
    # except Exception as e:
    #      messagebox.showerror("  Exception Occured",e)
    app=App(root)
    root.mainloop()

if __name__=="__main__":
    main()