from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/works')
def works():
    return render_template('works.html')

@app.route('/works/uppercase', methods=['GET', 'POST'])
def uppercase():
    result = None

    if request.method == 'POST':
        input_string = request.form.get('inputString', '')
        result = input_string.upper()

    return render_template('touppercase.html', result=result)

@app.route('/works/area/circle', methods=['GET', 'POST'])
def acircle():
    result = None
    error = None

    if request.method == 'POST':
        radius = request.form.get('radius', '')

        try:
            radius = float(radius)
            result = radius * 3.14 * radius
        except ValueError:
            error = "Please enter a number."

    return render_template('circle.html', result=result, error=error)

# @app.route('/areaOfcirle', methods=['GET', 'POST'])
# def areaOfcirle():
#     result = None
#     name=request.get('name','')
#     print(name)
#     if request.method == 'POST':
#         input_string = request.form.get('inputradius', '')
#         result = int(input_string) * int(input_string) * 3.14
#     return render_template('areaCircle.html', result=result)

@app.route('/works/area/rectangle', methods=['GET', 'POST'])
def arectangle():
    result = None
    error = None

    if request.method == 'POST':
        length = request.form.get('length', '')
        width = request.form.get('width', '')

        try:
            length = float(length)
            width = float(width)
            result = length * width
        except ValueError:
            error = "Please enter a number."

    return render_template('rectangle.html', result=result, error=error)

@app.route('/contact')
def contact():
    return render_template('contact.html')

if __name__ == "__main__":
    app.run(debug=True)
