import tkinter as tk
from tkinter import messagebox as msgbox
from tkinter import ttk
from tkinter import filedialog
from controller import Controller
import time,datetime

class Application(tk.Frame):

    def __init__(self, master, controller):
        master.geometry("+300+200")
        master.title("Humanity\'s most fundamental relationship is with what we eat.")
        self.controller = controller
        self.master = master
        super().__init__(master)
        self.pack(padx=5,pady=5)
        self.create_gui()
        self.update_rstrts_list_gui({})
    
    def create_gui(self):
        fm_1 = tk.Frame(self)
        fm_1.grid(row=0,column=0,stick=tk.NS)

        self.search_fm = tk.LabelFrame(fm_1, text="search")
        self.search_fm.pack(fill=tk.BOTH,padx=2)
        self.create_search_gui()

        self.operation_fm = tk.LabelFrame(fm_1, text="operation")
        self.operation_fm.pack(fill=tk.BOTH,padx=2)
        self.create_operation_gui()

        self.rstrts_list_fm = tk.LabelFrame(self, text="restaurants list")
        self.rstrts_list_fm.grid(row=0,column=1,sticky=tk.NSEW,padx=2)
        self.create_rstrts_list_gui()

        fm_3 = tk.Frame(self)
        fm_3.grid(row=0,column=2,stick=tk.NSEW)

        self.rstrt_info_fm = tk.LabelFrame(fm_3, width=500, height=138, text="basic info")
        self.rstrt_info_fm.grid(row=0,column=0,sticky=tk.NSEW,padx=2)
        self.rstrt_info_fm.grid_propagate(False)
        self.create_rstrt_info_gui()

        self.rstrt_address_fm = tk.LabelFrame(fm_3, width=500, height=139, text="address")
        self.rstrt_address_fm.grid(row=1,column=0,sticky=tk.NSEW,padx=2)
        self.rstrt_address_fm.grid_propagate(False)
        self.create_rstrt_address_gui()

        self.rstrt_grades_fm = tk.LabelFrame(fm_3,width=500,text="grades")
        self.rstrt_grades_fm.grid(row=2,column=0,sticky=tk.NSEW,padx=2)
        self.create_rstrt_grades_gui()
    
    def create_search_gui(self):
        master = self.search_fm
        label_names = ["Name", "Borough", "Street", "zipcode"]
        for row, name in enumerate(label_names):
            tk.Label(master, text=name).grid(row=row,column=0)
        
        self.search_views_list = list()
        for i in range(4):
            ety = tk.Entry(master, width=13)
            ety.grid(row=i,column=1,sticky=tk.EW)
            ety.bind("<Return>", self.search)
            self.search_views_list.append(ety)

        search_btn = tk.Button(master, text="search",command=self.search)
        search_btn.grid(row=4,column=0,columnspan=2)

    def create_operation_gui(self):
        master = self.operation_fm

        tk.Button(master,text="new restaurant",command=self.new_rstrt).pack(fill=tk.X)
        tk.Button(master,text="import .json",command=self.import_rstrt).pack(fill=tk.X)
        tk.Frame(master,height=10).pack()
        tk.Button(master,text="delete selected",command=self.del_rstrt).pack(fill=tk.X)
        tk.Button(master,text="delete all",command=self.del_all_rstrts).pack(fill=tk.X)

    def create_rstrts_list_gui(self):
        master = self.rstrts_list_fm

        tree = ttk.Treeview(master,height=30,columns=list(range(2)),show="headings")
        self.rstrts_list_tree = tree

        tree.column(0,width=100,anchor='center')
        tree.column(1,width=300,anchor='center')
        
        tree.heading(0,text='distance')
        tree.heading(1,text='restaurant')

        tree.bind("<ButtonRelease-1>", self.update_cur_rstrt)

        vbar = ttk.Scrollbar(master,orient=tk.VERTICAL,command=tree.yview)
        tree.configure(yscrollcommand=vbar.set)        
        tree.grid(row=0,column=0,sticky=tk.NSEW,pady=2)
        vbar.grid(row=0,column=1,sticky=tk.NS)
    
    def update_rstrts_list_gui(self,condition):
        self.controller.update_rstrts(condition)
        self.refresh_rstrts_list_gui()
        self.update_cur_rstrt()
    
    def refresh_rstrts_list_gui(self):
        tree = self.rstrts_list_tree
        rstrts = self.controller.filtered_rstrts

        for item in tree.get_children():
            tree.delete(item)
        
        for rstrt in rstrts:
            tree.insert('',tk.END,values=("%.2fkm"%(rstrt['dist']),rstrt['name']))
        

    def create_rstrt_info_gui(self):
        master = self.rstrt_info_fm
        self.rstrt_info_views = list()

        texts = ["id:", "name:", "cuisine:", "borough:"]
        for text in texts:
            self.rstrt_info_views.append(tk.Label(master,text=text))
            ety = tk.Entry(master,width=48)
            ety.bind("<FocusOut>",self.edit_rstrt_info)
            ety.bind("<Return>",self.edit_rstrt_info)
            self.rstrt_info_views.append(ety)

    def show_rstrt_info_gui(self):
        rstrt = self.controller.cur_rstrt
        views = self.rstrt_info_views
        for i in range(4):
            views[i*2].grid(row=i,column=0,sticky=tk.E)
        
        keys = ["restaurant_id", "name", "cuisine", "borough"]
        views[1].config(state=tk.NORMAL)
        for i, key in enumerate(keys):
            views[i*2+1].delete(0,tk.END)
            views[i*2+1].insert(0, rstrt[key])
            views[i*2+1].grid(row=i,column=1,sticky=tk.W)
        views[1].config(state=tk.DISABLED)

    def forget_rstrt_info_gui(self):
        for slave in self.rstrt_info_fm.grid_slaves():
            self.rstrt_info_views.append(slave)
            slave.grid_forget()
        
    def update_rstrt_info_gui(self):
        rstrt = self.controller.cur_rstrt
        if rstrt is None:
            self.forget_rstrt_info_gui()
        else:
            self.show_rstrt_info_gui()
        
    def create_rstrt_address_gui(self):
        master = self.rstrt_address_fm
        self.rstrt_address_views = list()
        texts = ["building:", "street:", "zipcode:", "coord:"]
        for text in texts:
            self.rstrt_address_views.append(tk.Label(master,text=text))
            ety = tk.Entry(master, width=48)
            ety.bind("<FocusOut>",self.edit_rstrt_address)
            ety.bind("<Return>",self.edit_rstrt_address)
            self.rstrt_address_views.append(ety)
        
        coord_fm = tk.Frame(master)
        self.rstrt_address_views[-1] = coord_fm
        for _ in range(2):
            ety = tk.Entry(coord_fm,width=23)
            ety.bind("<FocusOut>",self.edit_rstrt_coord)
            ety.bind("<Return>",self.edit_rstrt_coord)
            self.rstrt_address_views.append(ety)

    def show_rstrt_address_gui(self):
        rstrt = self.controller.cur_rstrt
        views = self.rstrt_address_views
        
        for i in range(4):
            views[i*2].grid(row=i,column=0,sticky=tk.E)
        
        keys = ['building', 'street', 'zipcode']
        for i, key in enumerate(keys):
            views[i*2+1].delete(0,tk.END)
            views[i*2+1].insert(0, rstrt['address'][key])
            views[i*2+1].grid(row=i,column=1,sticky=tk.W)
        views[7].grid(row=3,column=1,sticky=tk.W)

        coord = rstrt['address']['coord']
        for i in range(2):
            views[i+8].delete(0, tk.END)
            if coord and coord[i]:
                views[i+8].insert(0, "%.5f%c" % ( abs(coord[i]),(('E','N')[i], ('W','S')[i])[coord[i]<0] ) )
            views[i+8].grid(row=0,column=i,sticky=tk.W)

    def forget_rstrt_address_gui(self):
        for slave in self.rstrt_address_fm.grid_slaves():
            self.rstrt_address_views.append(slave)
            slave.grid_forget()

    def update_rstrt_address_gui(self):
        rstrt = self.controller.cur_rstrt
        if rstrt is None:
            self.forget_rstrt_address_gui()
        else:
            self.show_rstrt_address_gui()
    
    def create_rstrt_grades_gui(self):
        master = self.rstrt_grades_fm
        tree = ttk.Treeview(master,height=13,columns=list(range(3)),show="headings")
        self.rstrt_grades_tree = tree

        tree.column(0,width=100,anchor='center')
        tree.column(1,width=100,anchor='center')
        tree.column(2,width=300,anchor='center')
        
        tree.heading(0,text='grade')
        tree.heading(1,text='score')
        tree.heading(2,text='date')

        vbar = ttk.Scrollbar(master,orient=tk.VERTICAL,command=tree.yview)
        tree.configure(yscrollcommand=vbar.set)        
        tree.grid(row=0,column=0,sticky=tk.NSEW,pady=2)
        vbar.grid(row=0,column=1,sticky=tk.NS)

        btn_fm = tk.Frame(master)
        btn_fm.grid(row=1,column=0,columnspan=2)

        tk.Button(btn_fm,text=" + ",command=self.add_grade).grid(row=0,column=0)
        tk.Button(btn_fm,text=" - ",command=self.del_grade).grid(row=0,column=1)
        
    def update_rstrt_grades_gui(self):
        tree = self.rstrt_grades_tree
        rstrt = self.controller.cur_rstrt

        for item in tree.get_children():
            tree.delete(item)
        
        if rstrt is None:
            return

        for grade in rstrt['grades']:
            time_array = time.localtime(int(grade['date'])/1000)
            format_time = time.strftime("%Y-%m-%d %H:%M:%S", time_array)
            tree.insert('',tk.END,values=(grade['grade'],grade['score'],format_time))

    def update_cur_rstrt(self,event=None):
        index = None
        if self.rstrts_list_tree.selection():
            index = self.rstrts_list_tree.index(self.rstrts_list_tree.selection()[0])
        self.controller.update_cur_rstrt(index)
        self.update_rstrt_info_gui()
        self.update_rstrt_address_gui()
        self.update_rstrt_grades_gui()

    def search(self, event=None):
        views = self.search_views_list
        keys = ['name', 'borough', 'street', 'zipcode']
        condition = dict()
        for i in range(4):
            condition[keys[i]] = views[i].get().strip()
        self.update_rstrts_list_gui(condition)

    def import_rstrt(self):
        files_names = filedialog.askopenfilenames(filetypes=[("json file", "*.json")])
        if not files_names:
            return
        for fn in files_names:
            self.controller.add_rstrts_from_json(fn)
        self.update_rstrts_list_gui({})

    def del_rstrt(self):
        if self.rstrts_list_tree.selection() is None:
            return
        self.controller.del_rstrt()
        self.rstrts_list_tree.delete(self.rstrts_list_tree.selection()[0])
        self.update_cur_rstrt()
        
    
    def new_rstrt(self):
        self.controller.new_rstrt()
        tree = self.rstrts_list_tree
        tree.insert('',0,values=('99999.99km','untitled'))
        tree.selection_set(tree.get_children()[0])
        self.update_cur_rstrt()
        

    def edit_rstrt_info(self,event=None):
        views = self.rstrt_info_views
        
        keys = ["name", "cuisine", "borough"]
        docs = dict()
        for i in range(3):
            docs[keys[i]] = views[i*2+3].get()
        self.controller.edit_info(docs)
        tree = self.rstrts_list_tree
        item = tree.get_children()[self.controller.cur_index]
        tree.set(item, column=1, value=views[3].get())
        
    
    def edit_rstrt_address(self,event=None):
        views = self.rstrt_address_views
        keys = ['building', 'street', 'zipcode']
        docs = dict()
        for i in range(3):
            docs[keys[i]] = views[i*2+1].get()
        
    
    def edit_rstrt_coord(self,event=None):
        try:
            views = self.rstrt_address_views
            lng = views[8].get()
            lng_var = None
            if not lng == "":
                if lng[-1] == 'E' or lng[-1] == 'e':
                    lng_var = 1
                elif lng[-1] == 'W' or lng[-1] == 'w':
                    lng_var = -1
                else:
                    raise Exception("Last symbol should be E or W or e or w not",lng[-1])
                lng_var *= float(lng[:-1])

            lat = views[9].get()
            lat_var = None
            if not lat == "":
                if lat[-1] == 'N' or lat[-1] == 'n':
                    lat_var = 1
                elif lat[-1] == 'S' or lat[-1] == 's':
                    lat_var = -1
                else:
                    raise Exception("Last symbol should be S or N or s or n not",lng[-1])
                lat_var *= float(lat[:-1])
            self.controller.edit_coord(lng_var, lat_var)

            tree = self.rstrts_list_tree
            item = tree.get_children()[self.controller.cur_index]
            rstrt = self.controller.filtered_rstrts[self.controller.cur_index]
            tree.set(item, column=0, value="%.2fkm"%(rstrt['dist']))
        except Exception as e:
            msgbox.showerror('error',e)
        

    def del_all_rstrts(self):
        if msgbox.askyesno('Sure?', 'Do you want to delete all information'):
            self.controller.del_all()
            self.search()

    def add_grade(self):
        if self.controller.cur_rstrt is None:
            return
        AddGradeGui(self)
        self.update_rstrt_grades_gui()

    def del_grade(self):
        tree = self.rstrt_grades_tree
        if len(tree.selection()) == 0 or self.controller.cur_rstrt is None:
            return
        item = tree.selection()[0]
        index = tree.index(item)
        self.controller.del_grade(index)
        self.rstrts_list_tree.delete(item)
        self.update_rstrt_grades_gui()










class AddGradeGui(tk.Frame):
    def __init__(self,father):
        self.master = tk.Toplevel(father.master)
        self.master.geometry("+350+230")
        self.master.title("Grade")
        super().__init__(self.master,width=100,height=50)
        self.controller = father.controller
        self.father = father
        self.pack()
        self.create_gui()
    
    def create_gui(self):
        master = self
        tk.Label(master,text="Grade:").grid(row=0,column=0)
        self.grade_ety = tk.Entry(master)
        self.grade_ety.grid(row=0,column=1)
        
        tk.Label(master,text="Score:").grid(row=1,column=0)
        self.score_ety = tk.Entry(master)
        self.score_ety.grid(row=1,column=1)

        tk.Button(master,text=" + ",command=self.add).grid(row=2,column=0,columnspan=2)

    def add(self):
        grade = self.grade_ety.get()
        score = self.score_ety.get()
        self.controller.add_grade(grade,score)
        self.father.update_rstrt_grades_gui()
        self.master.destroy()








class LoginGui(tk.Frame):
    
    def __init__(self, master, controller):
        master.geometry("+350+230")
        master.title("Connect to DB")
        self.controller = controller
        self.master = master
        super().__init__(master,width=100,height=50)
        self.pack()
        self.create_gui()
    
    def create_gui(self):
        self.db_fm = tk.LabelFrame(self, text="Database")
        self.db_fm.pack(padx=10,pady=5)
        self.create_db_gui()

        self.coord_fm = tk.LabelFrame(self, text="coord")
        self.coord_fm.pack()
        self.create_coord_gui()

        tk.Button(self, text="Connect or Create", command=self.login).pack(pady=8)

    def create_db_gui(self):
        master = self.db_fm
        tk.Label(master, text="Client").grid(row=0,column=0,sticky=tk.E)
        self.ip_ety = tk.Entry(master,width=22)
        self.ip_ety.insert(0,"mongodb://localhost:27017/")
        self.ip_ety.grid(row=0,column=1)
        tk.Label(master, text="DB name").grid(row=1,column=0,sticky=tk.E)
        self.db_name_ety = tk.Entry(master,width=22)
        self.db_name_ety.insert(0,"restaurants")
        self.db_name_ety.grid(row=1,column=1)

    def create_coord_gui(self):
        master = self.coord_fm
        self.lng_ety = tk.Entry(master)
        self.lng_ety.insert(0,"73.9")
        self.lng_ety.grid(row=0,column=0)

        self.lng_var = tk.IntVar()
        tk.Radiobutton(master,text="E",value=1,variable=self.lng_var).grid(row=0,column=1)
        tk.Radiobutton(master,text="W",value=-1,variable=self.lng_var).grid(row=0,column=2)
        self.lng_var.set(-1)

        self.lat_ety = tk.Entry(master)
        self.lat_ety.insert(0,"40.9")
        self.lat_ety.grid(row=1,column=0)

        self.lat_var = tk.IntVar()
        tk.Radiobutton(master,text="N",value=1,variable=self.lat_var).grid(row=1,column=1)
        tk.Radiobutton(master,text="S",value=-1,variable=self.lat_var).grid(row=1,column=2)
        self.lat_var.set(1)

    def login(self):
        try:
            ip = self.ip_ety.get()
            db_name = self.db_name_ety.get()
            lng = float(self.lng_ety.get())*self.lng_var.get()
            lat = float(self.lat_ety.get())*self.lat_var.get()
            self.controller.cur_coord = (lng, lat)
            self.controller.connect(ip,db_name)
            self.master.destroy()
            Application(tk.Tk(), self.controller)
        except Exception as e:
            msgbox.showerror('error',e)





LoginGui(tk.Tk(), Controller())
tk.mainloop()