import sqlite3
from tkinter import *
from tkinter import messagebox
from db import Database
import webbrowser as wb

import requests
from bs4 import BeautifulSoup


db = Database('meets.db')
selected_item = 0
btn_color = 'white'

# def check_s_time():
#     pass


# def check_e_time():
#     pass


# def check_link():
#     pass


def error_message():
    print(meet_name_text.get())
    print(meet_link_text.get())
    print(start_date_text.get())
    print(end_date_text.get())
    if(meet_name_text.get() == '' or start_date_text.get() == '' or end_date_text == '' or meet_link_text.get() == ''):
        messagebox.showerror('Required Fields', 'Please insert all fields')
        return 1
    return 0


def fetch_data():
    data_list.delete(0,END)
    for row in db.fetch():
        # row_with_spaces = []
        # for entity in row:
        #     row_with_spaces.append(entity)
        #     row_with_spaces.append('')
        # print(row_with_spaces)
        
        data_list.insert(END, row)


def add_meet():
    if error_message():
        return
    try:
        db.insert(meet_name_text.get(),start_date_text.get(),end_date_text.get(), meet_link_text.get())
    except sqlite3.IntegrityError:
        messagebox.showerror('Meeting name exists!','Meeting name should be unique.')
    fetch_data()


def update_data():
    if error_message() == 1:
        return
    db.update(selected_item[0],meet_name_text.get(), start_date_text.get(), end_date_text.get(), meet_link_text.get())
    fetch_data()


def select_item(event):
    try:
        global selected_item
        index = data_list.curselection()[0]
        selected_item = data_list.get(index)
        print(selected_item)
        # insert selected data into fields
        meet_name_entry.delete(0,END)
        meet_name_entry.insert(END,selected_item[1])
        start_date_entry.delete(0,END)
        start_date_entry.insert(END,selected_item[2])
        end_date_entry.delete(0,END)
        end_date_entry.insert(END,selected_item[3])
        meet_link_entry.delete(0,END)
        meet_link_entry.insert(END,selected_item[4])
        
    except IndexError:
        pass


def delete_data():
    if error_message():
        return
    db.remove(selected_item[0])
    fetch_data()


def clear_data():
    meet_name_entry.delete(0,END)
    start_date_entry.delete(0,END)
    end_date_entry.delete(0,END)
    meet_link_entry.delete(0,END)


Title = 'Meetey V1.0'
# Create window object
app = Tk()

# Meet name
meet_name_text = StringVar()
meet_name_label = Label(app, text='Meet Name', font=('bold',14), pady=20)
meet_name_label.grid(row=0, column=0, sticky=W)
meet_name_label.configure(bg='#121417',fg='white')
meet_name_entry = Entry(app, textvariable=meet_name_text)
meet_name_entry.grid(row=0, column=1)

# Start date
start_date_text = StringVar()
start_date_label = Label(app, text='Start date', font=('bold',14), pady=20)
start_date_label.configure(bg='#121417',fg='white')
start_date_label.grid(row=2, column=0, sticky=W)
start_date_entry = Entry(app, textvariable=start_date_text)
start_date_entry.grid(row=2, column=1)

# End date
end_date_text = StringVar()
end_date_label = Label(app, text='End Date', font=('bold',14), pady=20)
end_date_label.configure(bg='#121417',fg='white')
end_date_label.grid(row=3, column=0, sticky=W)
end_date_entry = Entry(app, textvariable=end_date_text)
end_date_entry.grid(row=3, column=1)

# Meet Link
meet_link_text = StringVar()
meet_link_label = Label(app, text='Meet Link', font=('bold',14), pady=20)
meet_link_label.grid(row=1, column=0, sticky=W)
meet_link_label.configure(bg='#121417',fg='white')
meet_link_entry = Entry(app, textvariable=meet_link_text)
meet_link_entry.grid(row=1, column=1)

# ListBox
data_list = Listbox(app,height=10,width=60)
data_list.grid(row=5, column=0, columnspan=4,rowspan=6, padx=10,pady=10)
data_list.configure(bg='#232d3b',fg='white',highlightbackground='green',borderwidth=0,font = ('Courier New', 16))

# ScrollBar
scroll_bar = Scrollbar(app,orient=VERTICAL)
scroll_bar.grid(row=5,column=4)
scroll_bar.configure(bg='green')

# set scroll to listbox
data_list.configure(yscrollcommand=scroll_bar.set)
scroll_bar.configure(command=data_list.yview)

# bind select
data_list.bind('<<ListboxSelect>>',select_item)

# Buttons
add_meet_btn = Button(app,text='Add Meet', width=12, pady=10,command=add_meet)
add_meet_btn.grid(row=4,column=0)
add_meet_btn.configure(bg='#121417',fg=btn_color,highlightbackground='green',borderwidth=.05)
update_btn = Button(app,text='Update', width=12, pady=10, command=update_data)
update_btn.grid(row=4,column=1)
update_btn.configure(bg='#121417',fg=btn_color,highlightbackground='green',borderwidth=.05)
remove_btn = Button(app,text='Delete', width=12, pady=10, command=delete_data)
remove_btn.grid(row=4,column=2)
remove_btn.configure(bg='#121417',fg=btn_color,highlightbackground='green',borderwidth=.05)
clear_btn = Button(app,text='Clear Fields', width=12, pady=10, command=clear_data)
clear_btn.grid(row=0,column=2)
clear_btn.configure(bg='#121417',fg=btn_color,highlightbackground='green',borderwidth=.05)

# Check inputs Buttons
# link_check_btn = Button(app,text='Sync Link', width=12, pady=10, command=check_link)
# link_check_btn.grid(row=1,column=2)
# link_check_btn.configure(bg='#121417',fg=btn_color,highlightbackground='green',borderwidth=.05)
# s_time_check_btn = Button(app,text='Sync Start Date', width=12, pady=10, command=check_s_time)
# s_time_check_btn.grid(row=2,column=2)
# s_time_check_btn.configure(bg='#121417',fg=btn_color,highlightbackground='green',borderwidth=.05)
# e_time_check_btn = Button(app,text='Sync End End Date', width=12, pady=10, command=check_e_time)
# e_time_check_btn.grid(row=3,column=2)
# e_time_check_btn.configure(width=0,bg='#121417',fg=btn_color,highlightbackground='green',borderwidth=.05)



# App Main
app.title(Title)
app.geometry('830x600')
app.configure(bg='#121417')
fetch_data()




# Start program
app.mainloop()
