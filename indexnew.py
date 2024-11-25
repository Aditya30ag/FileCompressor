import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from tkinter import *
from PIL import Image, ImageTk
import os
import threading
import zipfile
import gzip
import shutil
import py7zr
import time

def browse_input_file():
    file_path = filedialog.askopenfilename()
    input_file_entry.delete(0, tk.END)
    input_file_entry.insert(0, file_path)

def browse_output_file():
    file_path = filedialog.asksaveasfilename()
    output_file_entry.delete(0, tk.END)
    output_file_entry.insert(0, file_path)


#compressor
def zipfilecompresser(input_file,output_file):
    with zipfile.ZipFile(output_file + ".zip", 'w') as zipf:
        # Add the file to the zip
        zipf.write(input_file, os.path.basename(input_file))
        print(f"{input_file} has been zipped into {output_file}.zip")
        result_label.config(text=f"File '{input_file}' compressed to '{output_file}.zip'")

        #code for real time analysis
        output_file=output_file+".zip"
        compersoroutput(output_file)
        
            

def gzipfilecompressor(input_file,output_file):
    with open(input_file, 'rb') as f_in:
        with gzip.open(input_file+ ".gz", 'wb') as f_out:
            
            f_out.writelines(f_in)
    
    result_label.config(text=f"File '{input_file}' compressed to '{output_file}.gz'")

    #code for real time analysis
    output_file=output_file+".gz"
    compersoroutput(output_file)

def py7zrfilecompressor(input_file,output_file):
    with py7zr.SevenZipFile(output_file+".rar", mode='w') as archive:
        archive.writeall(input_file, arcname='.')
    result_label.config(text=f"File '{input_file}' compressed to '{output_file}.rar'")

    #code for real time analysis
    output_file=output_file+".rar"
    compersoroutput(output_file)

def compersoroutput(output_file):
    a=os.path.abspath(output_file)
    size=os.path.getsize(a)/1024
    result_label_size.config(text=f"After compression file size: {size:.4f} KB")


#Decompressor
def zipfiledecompressor(input_file,output_file):
    with zipfile.ZipFile(input_file, 'r') as zipf:
        zipf.extractall(output_file)
        result_label.config(text=f"File '{input_file}' decompressed to '{output_file}.zip'")

    #code for real time analysis
    output_file=output_file
    decompersoroutput(output_file)

def gzipfiledecompressor(input_file,output_file):
    with open(input_file, 'rb') as f_in:
        with gzip.open(output_file, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
    
    result_label.config(text=f"File '{input_file}' decompressed to '{output_file}'")

    #code for real time analysis
    output_file=output_file
    decompersoroutput(output_file)

def py7zrfiledecompressor(input_file,output_file):
    with py7zr.SevenZipFile(input_file, 'r') as archive:
        archive.extractall(path=output_file)

    result_label.config(text=f"File '{input_file}' decompressed to '{output_file}'")

    #code for real time analysis
    output_file=output_file
    decompersoroutput(output_file)


def decompersoroutput(output_file):
    a=os.path.abspath(output_file)
    size=os.path.getsize(a)/1024
    result_label_size.config(text=f"After decompress file size: {size:.4f} KB")



def printsize(input_file):
    a=os.path.getsize(input_file)/1024
    return a

def compress_file():
    input_file=input_file_entry.get()
    output_file=output_file_entry.get()
    format_choice=format_var.get()

    try:
        if not input_file or not output_file:
            print("error")
            raise ValueError("Please provide both input and output file paths.")
        if not os.path.exists(input_file):
            raise ValueError(f"Input File {input_file} not found")
        
        result_label_size_before.config(text=f"Before compression file size:{printsize(input_file):.4f} KB")
        start_time = time.time()
        
        if format_choice=="GZIP":
            output_file=input_file
            gzipfilecompressor(input_file,output_file)
        elif format_choice=="ZIP":
            zipfilecompresser(input_file,output_file)
        elif format_choice=="RAR":
            py7zrfilecompressor(input_file,output_file)
        else:
            result_label.config(text="Invalid format selection.")
        
        print(input_file)

        elapsed_time = time.time() - start_time
        result_label_time.config(text=f"The time taken to compressor the  file :{elapsed_time:.4f} sec")

        if delete_source_var.get():
            os.remove(input_file)
            messagebox.showinfo("Info", f"Source file {input_file} deleted after compression")


    except Exception as e:
        result_label.config(text=f"An error occurred: {e}")

def compress_file_async():
    threading.Thread(target=compress_file).start()

def decompress_file():
    input_file=input_file_entry.get()
    output_file=output_file_entry.get()
    format_choice=format_var.get()

    try:
        if not input_file or not output_file:
            print("error")
            raise ValueError("Please provide both input and output file paths.")
        if not os.path.exists(input_file):
            raise ValueError(f"Input File {input_file} not found")
        
        result_label_size_before.config(text=f"Before decompress file size:{printsize(input_file):.4f} KB")
        start_time = time.time()

        if format_choice=="GZIP":
            gzipfiledecompressor(input_file,output_file)
        elif format_choice=="ZIP":
            zipfiledecompressor(input_file,output_file)
        elif format_choice=="RAR":
            py7zrfiledecompressor(input_file,output_file)
        else:
            result_label.config(text="Invalid format selection.")
        
        elapsed_time = time.time() - start_time
        result_label_time.config(text=f"The time taken to decompress the  file :{elapsed_time:.4f} sec")
        if delete_source_var.get():
            os.remove(input_file)
            messagebox.showinfo("Info", f"Source file {input_file} deleted after compression")

    except Exception as e:
        result_label.config(text=f"An error occurred: {e}")

def decompress_file_async():
    threading.Thread(target=decompress_file).start()


def toggle_dark_mode():
    if dark_mode_var.get():
        app.config(bg="black")
        for widget in app.winfo_children():
            if isinstance(widget, (tk.Button, tk.Label, tk.Entry)):
                widget.config(bg="gray20", fg="white")  # Dark mode colors
            elif isinstance(widget, tk.OptionMenu):
                widget.config(bg="gray20", fg="white")  # Dark mode colors
            elif isinstance(widget, tk.Checkbutton):
                widget.config(bg="black", fg="white")  # Dark mode colors
    else:
        app.config(bg="SystemButtonFace")
        for widget in app.winfo_children():
            if isinstance(widget, (tk.Button, tk.Label, tk.Entry)):
                widget.config(bg="SystemButtonFace", fg="black")  # Light mode colors
            elif isinstance(widget, tk.OptionMenu):
                widget.config(bg="SystemButtonFace", fg="black")  # Light mode colors
            elif isinstance(widget, tk.Checkbutton):
                widget.config(bg="SystemButtonFace", fg="black")  # Light mode colors



# Create the main application window
app = tk.Tk()
app.title("FileCompressor")
app.minsize(800,480)
app.maxsize(800,480)

delete_source_var = tk.BooleanVar()
dark_mode_var = tk.BooleanVar()

# Load the background image using Pillow
background_image = Image.open("C:/Users/adity/Pictures/Screenshots/projectimg.png")  # Use your image path
background_photo = ImageTk.PhotoImage(background_image)
# Create a label for the background image
background_label = tk.Label(app, image=background_photo)
background_label.place(relwidth=1, relheight=1)  # Fill the entire window

dark_mode_button = tk.Checkbutton(app, text="Dark Mode", var=dark_mode_var, command=toggle_dark_mode)
dark_mode_button.place(x=700, y=20)


delete_source_checkbox = tk.Checkbutton(app, text="Delete source file after operation", var=delete_source_var)
delete_source_checkbox.place(x=100, y=230)


input_file_label = tk.Label(app, text="Input File:",background="#EDEAEF",padx=50,pady=10,font=("Arial",12,"bold"),relief="groove")
input_file_label.pack()
input_file_entry = tk.Entry(app,font=("Cursive",8),relief="flat",background="#312130",foreground="white")
input_file_entry.pack()

input_file_button = tk.Button(app, text="Browse",font=("Arial", 8),bg="#E8E8E8",fg="black",padx=4,pady=4,command=browse_input_file)
input_file_button.pack()

input_file_label.place(x=100, y=70)
input_file_entry.place(x=358, y=80)
input_file_button.place(x=576, y=78)

output_file_label = tk.Label(app, text="Output File:",background="#EDEAEF",padx=45,pady=9,font=("Arial",12,"bold"),relief="groove")
output_file_label.pack()
output_file_entry = tk.Entry(app,background="#312130",foreground="white")
output_file_entry.pack()
output_file_button = tk.Button(app, text="Browse",font=("Arial", 8),bg="#E8E8E8",fg="black",padx=4,pady=4,command=browse_output_file)
output_file_button.pack()

output_file_label.place(x=100, y=170)
output_file_entry.place(x=358, y=179)
output_file_button.place(x=576, y=177)


compress_button = tk.Button(app, text="Compress",padx=4,command=compress_file_async,background="#EDEAEF")
compress_button.pack()

decompress_button = tk.Button(app, text="Decompress",padx=3,background="#EDEAEF",command=decompress_file_async)
decompress_button.pack()

compress_button.place(x=280, y=370)
decompress_button.place(x=480, y=370)


format_var = tk.StringVar()
format_var.set("GZIP")
format_label = tk.Label(app, text="Select Compression/Decompression Format:")
format_label.pack()
format_menu = tk.OptionMenu(app, format_var, "GZIP", "ZIP", "RAR")
format_menu.pack()

format_label.place(x=300, y=320)
format_menu.place(x=380, y=270)

result_label = tk.Label(app, text="")
result_label.pack(side="left")

result_label.place(x=150,y=400)


result_label_size_before = tk.Label(app, text="")
result_label_size_before.pack(side="left")

result_label_size_before.place(x=150,y=420)



result_label_size = tk.Label(app, text="")
result_label_size.pack(side="left")

result_label_size.place(x=355,y=420)



result_label_time = tk.Label(app, text="")
result_label_time.pack(side="left")

result_label_time.place(x=150,y=440)

# Run the application
app.mainloop()

