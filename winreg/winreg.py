import tkinter as tk
from tkinter import ttk, Menu, filedialog
import sys
from reghive import RegHive, GUI_Subkey


class HiveTab:
    def __init__(self, main):
        self.keys_tree = ttk.Treeview(main, selectmode='browse')
        self.keys_sb = ttk.Scrollbar(main, orient='vertical', command=self.keys_tree.yview)
        self.values_tree = ttk.Treeview(main)
        self.values_dict = {}
        self.values_sb = ttk.Scrollbar(main, orient='vertical', command=self.values_tree.yview)
        self.keys_tree.configure(yscrollcommand=self.keys_sb.set)
        self.values_tree.configure(yscrollcommand=self.values_sb.set)
        self.keys_tree["columns"]=("one","two","three")
        self.keys_tree.column("#0", width=100, minwidth=100, stretch=tk.YES)
        self.keys_tree.column("one", width=100, minwidth=100, stretch=tk.YES)
        self.keys_tree.column("two", width=100, minwidth=100, stretch=tk.YES)
        self.keys_tree.column("three", width=100, minwidth=100, stretch=tk.YES)
        self.keys_tree.heading("#0",text="Key Name",anchor=tk.W)
        self.keys_tree.heading("one", text="# Values",anchor=tk.W)
        self.keys_tree.heading("two", text="# SubKeys",anchor=tk.W)
        self.keys_tree.heading("three", text="Last Write TimeStamp",anchor=tk.W)
        self.values_tree["columns"]=("one","two","three")
        self.values_tree.column("#0", width=100, minwidth=100, stretch=tk.YES)
        self.values_tree.column("one", width=100, minwidth=100, stretch=tk.YES)
        self.values_tree.column("two", width=100, minwidth=100, stretch=tk.YES)
        self.values_tree.column("three", width=100, minwidth=100, stretch=tk.YES)
        self.values_tree.heading("#0",text="Value Name",anchor=tk.W)
        self.values_tree.heading("one", text="Value Type",anchor=tk.W)
        self.values_tree.heading("two", text="Data",anchor=tk.W)
        self.values_tree.heading("three", text="Corrupted",anchor=tk.W)
        
        def selectItem(a):
            curItem = self.keys_tree.focus()
            key_path = self.keys_tree.item(curItem)['values'][-1]
            subkey_values = self.values_dict[key_path]
            self.values_tree.delete(*self.values_tree.get_children())
            for row in subkey_values:
                self.values_tree.insert('', 'end', iid=None, text=row.name, values=(row.value_type, row.value, row.is_corrupted))

        self.keys_tree.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        self.keys_tree.bind('<ButtonRelease-1>', selectItem)
        self.keys_sb.pack(side=tk.LEFT, fill=tk.Y)
        self.values_tree.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        self.values_sb.pack(side=tk.LEFT, fill=tk.Y)


window = tk.Tk()
window.title('WinReg Explorer')
window.geometry("950x400")
TabControl = ttk.Notebook(window)

def create_menu():
    
    def _open_file():
        filename =  filedialog.askopenfilename(initialdir = "~",title = "Select file",)
        hive = RegHive(filename)
        tab_frame = ttk.Frame(TabControl)
        TabControl.add(tab_frame, text=f'{filename.split("/")[-1]}')
        tab = HiveTab(tab_frame)
        for subkey in hive.recurse_subkeys(as_json=True):
            tab.keys_tree.insert(subkey.parent_path, 0 if subkey.parent_path == '' else 'end', subkey.path, text=subkey.subkey_name, values=(subkey.values_count, subkey.subkey_count, subkey.timestamp[:-13], subkey.path))
            tab.values_dict[subkey.path] = subkey.values
            
    def _quit():
        window.quit()
        window.destroy()
        sys.exit()
    
    menu_bar = Menu(window)
    file_menu = Menu(menu_bar, tearoff=False)
    file_menu.add_command(label="Load Hive", command=_open_file)
    file_menu.add_separator()
    file_menu.add_command(label='Exit', command=_quit)
    
    menu_bar.add_cascade(menu=file_menu, label="File")
    window.config(menu=menu_bar)


create_menu()
TabControl.pack(expand = 1, fill ="both") 
window.mainloop()