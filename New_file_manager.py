
import tkinter as tk
import os
from tkinter.messagebox import showinfo
import string

def drives():
    '''
    This function returns a list of drives available in a system
    '''
    try:
        drive = string.ascii_uppercase
        valid_drive =[]
        for each_drive in drive:
            if os.path.exists(each_drive+ ":\\"):
                valid_drive.append(each_drive+":\\")
    except Exception as e:
        print("The error encountered in drives function is ",e)
    finally:
        return valid_drive

def search_file(filename):
    '''
    This function searches for a file name in all the drives of the computer.
    
    Argument ti be passes in a steing, which is a part of the file name or the file extension,
    eg. Passing "*.text" as an argument will return all the files with "test"
        in the file name.
        Passing "*.docx" will return all the files with docx extension.
    
    This is a generator function and returns the result set having the directory
    and file as a generator
    '''
    # default seach for extension as False
    search_ext = False
    filename = filename.casefold()

    # search will be done based on extension if the user has entered *.ext
    # where ext can be any extention like txt,docx,mp3,xlsx etc
    if filename.startswith('*.'):
        extension = filename.replace('*.','')
        search_ext = True

    # set all the drives present on desktop into a list
    all_drives = drives()

    for drive in all_drives:
        for path, dirs, files in os.walk(drive):
            for file in files:
                if (search_ext and file.casefold().endswith(extension)) or ((not search_ext) and filename in file.casefold()):
                    yield(path+"\\"+file)


def merge_files(search_results,ext):
    '''
    This function wil merge the files with supplied extension
    feom the search results. it will weite the contents to a new
    file'merged file' in the current working dir

    Arguments-
        search_results - a generator function with the search results
        ext            - extension of the files to be merges. It supports the below mentioned extensions
                         .txt

    '''
    lst =[]
    f =open("merged file.txt", 'w')
    for i in search_results:
        if i.casefold().endswith('.'+ext):
            src = open(i,'r')
            f.write(src.read())
            src.close()
            lst.append(i)
    f.close
    return lst

def validate_contents():
    '''
    This function checks if user has entered data on the search window.
    If the user has entered the data then call search_file
    to search for file in all the drives.

    The search results are displayed on the search window.
    '''
    search = searchtext.get()
    T.configure(state = 'normal')
    T.delete('1.0',tk.END)
    T.configure(state = 'disabled')
    if search.strip() != "":
        search = search_file(search.strip())
        num = 0
        for i in search:
            T.configure(state = 'normal')
            T.insert(tk.END, i + "\n")
            T.configure(state="disabled")
            num += 1
        showinfo("Search results","Total number of files found : "+str(num))
    else:
        showinfo("Search results","Enter a file to be searched")

def validate_merge():
    '''
    This function checks if the user has enterd data in the search window.
    If the user has entered the data then call merge_files
    to seach for file in all the drives. All the .txt files will be merged to 'merged files.txt'

    
    The merged source files will be displayed in a pop-up window.
    '''

    search = searchtext.get()
    if search.strip() != '':
        files = ''
        files_merged = merge_files(search_file(search.strip()),'txt')
        for i in files_merged:
            files += i + "\n"
        if files == '':
            files = "No .txt files were found for merging"
            showinfo("The below files were merged to merged files.txt",files)
        else:
            showinfo("Merge results", "Enter the file name to be searched and merged")


window = tk.Tk()
# to rename the title of window
window.title("Desktop Search")
# Label the seach entry field
tk.Label(window, text = "Enter file to be searched").grid(row = 0)
searchtext =tk.Entry(window,width = 150)
searchtext.grid(row = 0, column = 1)
tk.Label(window,text = "Search results----->").grid(row = 1)
tk.Button(window, text = "Search", command=validate_contents).grid(row = 0, column = 2)
T = tk.Text(window, height = 25, width = 150)
T.grid(row = 1, column = 1)
T.configure(state= "disabled")

tk.Button(window, text = "Merge .txt files from search results", fg = "blue", command = validate_merge).grid(row =2, column = 1)
tk.Button(window, text = "QUIT", fg = "red", command=window.destroy).grid(row = 3, column = 2)

tk.mainloop()





