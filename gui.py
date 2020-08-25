import os
from tkinter import *
import tkinter as tk
from tkinter import messagebox, Tk, Frame
import tkinter.filedialog as fd
import subprocess
from datetime import datetime


from PIL import ImageTk, Image


import config
from code_reviewer import CodeReviewer


class Window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)        
        self.master = master

        path = r'data\logo.jpg'
        img_raw = Image.open(path)
        img_raw = img_raw.resize((300, 300), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(img_raw)
        panel = tk.Label(master, image = img, bg='black')
        panel.pack(side = "top", fill = "both", expand = "yes")

        root.wm_title("Code Reviewer")
        root.geometry("350x600")
        self.configure(bg='black')
        self.pack(fill=BOTH, expand=1)

        btn_analyze_project = Button(self, text="analyze project", command=self.analyze_project, bg='white')
        btn_analyze_project.place(relx=0.5, rely=0.3, anchor=CENTER)

        btn_parse_json_report = Button(self, text="show reports", command=self.open_reports, bg='white')
        btn_parse_json_report.place(relx=0.5, rely=0.6, anchor=CENTER)
        root.mainloop()


    def analyze_project(self):
        path_uipath_projects = rf'{os.environ["HOMEPATH"]}\Documents\UiPath'
        path_project = fd.askopenfilename(
            title='select project.json',
            initialdir=path_uipath_projects,
            filetypes=[('project', 'project.json')]
            )
        if path_project:
            d = datetime.now()
            report_name = f'report_{d.strftime("%Y%m%d_%H%M%S")}.xlsx'
            path_report = os.path.join(config.path_reports, report_name)
            cr = CodeReviewer(path_project_json=path_project,
                              path_report=path_report)
            cr.review()
            messagebox.showinfo(message='done')
    
    def open_reports(self):
        subprocess.Popen(rf'explorer {config.path_reports}')


if __name__ == '__main__':
    root = Tk()
    app = Window(root)


