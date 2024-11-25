
import os
import zipfile
import gzip
import py7zr
import shutil
import time
import threading

#compressor
def zipfilecompresser(input_file,output_file):
    with zipfile.ZipFile(output_file + ".zip", 'w') as zipf:
        # Add the file to the zip
        zipf.write(input_file, os.path.basename(input_file))
        print(f"{input_file} has been zipped into {output_file}.zip")
        print(f"File '{input_file}' compressed to '{output_file}.zip'")

        #code for real time analysis
        output_file=output_file+".zip"
        return output_file
        
            

def gzipfilecompressor(input_file,output_file):
    with open(input_file, 'rb') as f_in:
        with gzip.open(input_file+ ".gz", 'wb') as f_out:
            
            f_out.writelines(f_in)
    
    print(f"File '{input_file}' compressed to '{output_file}.gz'")

    #code for real time analysis
    output_file=output_file+".gz"
    return output_file

def py7zrfilecompressor(input_file,output_file):
    with py7zr.SevenZipFile(output_file+".rar", mode='w') as archive:
        archive.writeall(input_file, arcname='.')
    print(f"File '{input_file}' compressed to '{output_file}.rar'")

    #code for real time analysis
    output_file=output_file+".rar"
    return output_file

def compersoroutput(output_file):
    a=os.path.abspath(output_file)
    size=os.path.getsize(a)/1024
    return f"{size:.4f}"


#Decompressor
def zipfiledecompressor(input_file,output_file):
    with zipfile.ZipFile(input_file, 'r') as zipf:
        zipf.extractall(output_file)

    #code for real time analysis
    output_file=output_file
    return output_file

def gzipfiledecompressor(input_file,output_file):
    with open(input_file, 'rb') as f_in:
        with gzip.open(output_file, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)

    #code for real time analysis
    output_file=output_file
    return output_file

def py7zrfiledecompressor(input_file,output_file):
    with py7zr.SevenZipFile(input_file, 'r') as archive:
        archive.extractall(path=output_file)

    #code for real time analysis
    output_file=output_file
    return output_file


def decompersoroutput(output_file):
    a=os.path.abspath(output_file)
    size=os.path.getsize(a)/1024
    return f"{size:.4f}"



def printsize(input_file):
    a=os.path.getsize(input_file)/1024
    return a

def compress_file(input_file,output_file,format_choice):

    try:
        if not input_file or not output_file:
            print("error")
            raise ValueError("Please provide both input and output file paths.")
        if not os.path.exists(input_file):
            raise ValueError(f"Input File {input_file} not found")
        
        start_time = time.time()
        if format_choice=="GZIP":
            output_file=input_file
            gzipfilecompressor(input_file,output_file)
            a=gzipfilecompressor(input_file,output_file)
            
        elif format_choice=="ZIP":
            zipfilecompresser(input_file,output_file)
            a=zipfilecompresser(input_file,output_file)
            
        elif format_choice=="RAR":
            py7zrfilecompressor(input_file,output_file)
            a=py7zrfilecompressor(input_file,output_file)
            
        else:
            return "Invalid format selection."


        elapsed_time = time.time() - start_time
        return input_file,output_file,format_choice,f"{printsize(input_file):.4f} KB",f"{compersoroutput(a)} KB",f"{elapsed_time:.4f} sec","Compress"

    except Exception as e:
        return f"An error occurred: {e}"

def compress_file_async():
    threading.Thread(target=compress_file).start()

def decompress_file(input_file,output_file,format_choice):

    try:
        if not input_file or not output_file:
            print("error")
            raise ValueError("Please provide both input and output file paths.")
        if not os.path.exists(input_file):
            raise ValueError(f"Input File {input_file} not found")
        
        start_time = time.time()

        if format_choice=="GZIP":
            gzipfiledecompressor(input_file,output_file)
            a=gzipfiledecompressor(input_file,output_file)
        elif format_choice=="ZIP":
            zipfiledecompressor(input_file,output_file)
            a=zipfiledecompressor(input_file,output_file)
        elif format_choice=="RAR":
            py7zrfiledecompressor(input_file,output_file)
            a=py7zrfiledecompressor(input_file,output_file)
        else:
            return "Invalid format selection."
        
        elapsed_time = time.time() - start_time
        
        return input_file,output_file,format_choice,f"{printsize(input_file):.4f} KB",f"{decompersoroutput(a)} KB",f"{elapsed_time:.4f} sec","Decompress"

    except Exception as e:
        return f"An error occurred: {e}"

def decompress_file_async():
    threading.Thread(target=decompress_file).start()

# input_file="C:/Users/adity/Pictures/logo512.png"
# output_file="hello"
# format_choice="ZIP"
# compress_file(input_file,output_file,format_choice)
