from flask import Flask, request, render_template, redirect, url_for
from index import compress_file
from index import decompress_file
from bye import resize_image

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/fileconverter')
def fileconverter():
    return render_template('fileconverter.html')

@app.route('/result', methods=['POST'])
def result():
    input_file=str(request.form['inputFile'])
    output_file=str(request.form['outputFile'])
    format_choice=str(request.form['format'])
    task=str(request.form['compress/decompress'])
    if(task=="compress"):
        result = compress_file(
            f"C:/Users/adity/Pictures/Screenshots/{input_file}",output_file,format_choice
        )
    else:
        result = decompress_file(
            f"C:/Users/adity/Pictures/Screenshots/{input_file}",output_file,format_choice
        )

    return render_template('result.html', result=result)


@app.route('/filecompressor', methods=['GET'])
def filecompressor():
    return render_template('filecompressor.html')

@app.route('/result1', methods=['POST'])
def result1():
    input_file1=str(request.form['inputFile'])
    output_file1=str(request.form['outputFile'])
    scale=float(request.form['scale'])
    percentage=int(request.form['percentage'])
    print(f"C:/Users/adity/Pictures/Screenshots/{input_file1}")
    result1=resize_image(f"C:/Users/adity/Pictures/Screenshots/{input_file1}",output_file1,scale,None,None,percentage)
    return render_template('result1.html', result1=result1)
    
if __name__ == '__main__':
    app.run(debug=True)
