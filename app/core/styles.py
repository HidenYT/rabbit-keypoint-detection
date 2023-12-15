from tkinter import ttk

ttk.Style().configure("default.TButton", padding=10, font=('Helvetica', 10))

ttk.Style().configure("navbar.TButton", padding=10, font=('Helvetica', 10), relief="!pressed")

ttk.Style().configure("default.TLabel", font=('Helvetica', 10), padding=10)

ttk.Style().configure("skeleton_table_cell.TEntry", padding=10)

selected_skeleton_table_cell = ttk.Style()
selected_skeleton_table_cell.element_create("plain.field", "from", "clam")
selected_skeleton_table_cell.layout("selected_skeleton_table_cell.TEntry",
                   [('Entry.plain.field', {'children': [(
                       'Entry.background', {'children': [(
                           'Entry.padding', {'children': [(
                               'Entry.textarea', {'sticky': 'nswe'})],
                      'sticky': 'nswe'})], 'sticky': 'nswe'})],
                      'border':'2', 'sticky': 'nswe'})])
selected_skeleton_table_cell.configure("selected_skeleton_table_cell.TEntry", 
                 fieldbackground="#b9eaeb",
                 padding=10,)

skeleton_table_cell_font = ('Helvetica', 10)