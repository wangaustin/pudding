#!/usr/bin/env python

import os
import shutil

from tkinter import *
from tkinter import filedialog

# ----------------------------------
# FUNCTION: ask directory
# ----------------------------------
def browse_file():
	label_file_explorer = filedialog.askdirectory()
	label_file_list.config(fg="blue")
	folder_path.set(label_file_explorer)
	file_list.set("桌面新的文件夹即将被命名为：“" + ent_new_folder_name.get() + "”\n" + "如果一切就绪就可以按“移动照片到桌面”。")


# ----------------------------------
# FUNCTION: create folder
# ----------------------------------
def create_folder(new_folder_name):
	dir_target = '/Users/may/Desktop/'
	# todo: this only works for MacOS, but that's sufficient for now
	desktop = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop')
	dir_target = os.path.join(desktop, ent_new_folder_name.get())

	# ERROR! Folder already exists
	if os.path.isdir(dir_target):
		file_list.set("“" + new_folder_name + "”已经在桌面了，请输入个新的名字！")
		label_file_list.config(fg="red")
	# no error, create new folder
	else:
		os.mkdir(dir_target)

		# create subfolders
		if checkbox_separate.get() == 1:
			os.mkdir(os.path.join(dir_target, "视频"))
			os.mkdir(os.path.join(dir_target, "照片"))

		file_list.set("已在桌面创建新的文件夹“" + new_folder_name + "”")

	# now move the files to target directory
	move_files(dir_target)


# ----------------------------------
# FUNCTION: move files
# ----------------------------------
def move_files(dir_target):
	mp4 = []
	jpg = []
	heic = []
	mov = []
	png = []

	all_formats = [mp4, jpg, heic, mov, png]

	# find .mp4
	for file in os.listdir(folder_path.get()):
		if file.lower().endswith(".mp4"):
			mp4.append(file)
		if file.lower().endswith(".jpg"):
			jpg.append(file)
		if file.lower().endswith(".heic"):
			heic.append(file)
		if file.lower().endswith(".mov"):
			mov.append(file)
		if file.lower().endswith(".png"):
			mov.append(file)

	dir_source = folder_path.get()
	append_video = "视频"
	append_photo = "照片"

	# iterate through lists
	for current_format in all_formats:
		for file in current_format:
			# if separating photos and videos
			if checkbox_separate.get() == 0:
				shutil.move(os.path.join(dir_source, file), dir_target)
			else:
				if current_format == mp4 or current_format == mov:
					source_path = os.path.join(dir_source, file)
					target_path = os.path.join(dir_target, append_video, file)

					shutil.move(source_path, target_path)
				else:
					source_path = os.path.join(dir_source, file)
					target_path = os.path.join(dir_target, append_photo, file)
					shutil.move(source_path, target_path)



# ----------------------------------
# Root frame UI
# ----------------------------------

# root
root = Tk()
root.title("小布丁")
root.minsize(200, 200)

# greeting
greeting = Label(
	root,
	justify="center",
	text="欢迎！这是Austin为爹地妈咪写的程序😘\n这个工具会帮助你把一个文件夹里的所有照片和视频移动到桌面的一个新的文件夹之中。\n"
)
greeting.grid(row=0, column=0, padx=50, sticky="w")

folder_path = StringVar()

# 浏览button
button_explore = Button(root, text="浏览", command=browse_file)
button_explore.grid(row=1, column=0, sticky="n")

label_file_explorer = Label(root, textvariable=folder_path, width = 100, height = 2, fg = "blue")
label_file_explorer.grid(row=3, column=0, sticky="w")

file_list = StringVar()
label_file_list = Label(root, textvariable=file_list, width = 100, height = 4, fg = "blue")
label_file_list.grid(row=4, column=0, sticky="w")

# input box
ent_new_folder_name = Entry(root, width=40)
ent_new_folder_name.grid(row=1, column=0, sticky="w")

# 移动照片button
button_confirm = Button(
	root,
	text="移动照片到桌面",
	height=2,
	command=lambda:create_folder(ent_new_folder_name.get())
)
button_confirm.grid(row=5, column=0, pady=10, padx= 10, sticky="w")


# 是否分开照片和视频
checkbox_separate = IntVar(value=1)

checkbox_button = Checkbutton(
    master=root,
    text="是否分开照片和视频",
    variable = checkbox_separate,
    offvalue=0,
    onvalue=1,
    height=2,
    width=20
)
checkbox_button.grid(row=2, column=0, pady=2, sticky="w")


root.mainloop()