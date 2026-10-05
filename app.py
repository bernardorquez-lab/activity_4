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
@app.route('/works/area/triangle', methods=['GET', 'POST'])
def atriangle():
    result = None
    error = None
    if request.method == 'POST':
        base = request.form.get('base', '')
        height = request.form.get('height', '')
        try:
            base = float(base)
            height = float(height)
            result = 0.5 * base * height
        except ValueError:
            error = "Please enter a number."
    return render_template('triangle.html', result=result, error=error)

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

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def append(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            return
        cur = self.head
        while cur.next:
            cur = cur.next
        cur.next = new_node

    def prepend(self, data):
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node

    def delete(self, data):
        cur = self.head
        prev = None
        while cur:
            if cur.data == data:
                if prev:
                    prev.next = cur.next
                else:
                    self.head = cur.next
                return True
            prev, cur = cur, cur.next
        return False

    def search(self, data):
        cur = self.head
        while cur:
            if cur.data == data:
                return True
            cur = cur.next
        return False

    def to_list(self):
        items, cur = [], self.head
        while cur:
            items.append(cur.data)
            cur = cur.next
        return items

my_list = LinkedList()

@app.route('/works/linkedlist', methods=['GET', 'POST'])
def linkedlist():
    message = None
    if request.method == 'POST':
        action = request.form.get('action')
        value = request.form.get('value', '').strip()
        if not value:
            message = "Please enter a value."
        elif action == 'append':
            my_list.append(value)
            message = f"Added '{value}' to the end."
        elif action == 'prepend':
            my_list.prepend(value)
            message = f"Added '{value}' to the front."
        elif action == 'delete':
            ok = my_list.delete(value)
            message = f"Deleted '{value}'." if ok else f"'{value}' not found."
        elif action == 'search':
            found = my_list.search(value)
            message = f"'{value}' {'is' if found else 'is not'} in the list."
    return render_template('linkedlist.html', items=my_list.to_list(), message=message)

if __name__ == "__main__":
    app.run(debug=True)
