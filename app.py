from flask import Flask, render_template, request, redirect, url_for
import re

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

class Queue:
    def __init__(self):
        self.items = []

    def enqueue(self, data):
        self.items.append(data)

    def dequeue(self):
        if self.is_empty():
            return None
        return self.items.pop(0)

    def is_empty(self):
        return len(self.items) == 0

    def to_list(self):
        return self.items.copy()


my_queue = Queue()

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

def convert_to_postfix(expression):
    priority = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}
    output = []
    stack = []
    tokens = re.findall(r'\d+(?:\.\d+)?|[A-Za-z]+|[()+\-*/^]', expression)

    if ''.join(tokens) != re.sub(r'\s+', '', expression):
        raise ValueError("Invalid expression.")

    if not tokens:
        raise ValueError("Please enter an expression.")

    for token in tokens:
        if token.isalnum() or token.replace('.', '', 1).isdigit():
            output.append(token)

        elif token == '(':
            stack.append(token)

        elif token == ')':
            while stack and stack[-1] != '(':
                output.append(stack.pop())

            if not stack:
                raise ValueError("Invalid parentheses.")

            stack.pop()

        elif token in priority:
            while stack and stack[-1] in priority and (
                priority[stack[-1]] > priority[token]
                or (priority[stack[-1]] == priority[token] and token != '^')
            ):
                output.append(stack.pop())

            stack.append(token)

    if '(' in stack:
        raise ValueError("Invalid parentheses.")

    while stack:
        output.append(stack.pop())

    return ' '.join(output)


@app.route('/works/infix-postfix', methods=['GET', 'POST'])
def infix_postfix():
    postfix = ""
    expression = ""
    error = ""

    if request.method == 'POST':
        expression = request.form.get('expression', '').strip()

        if not expression:
            error = "Please enter an expression."
        else:
            try:
                postfix = convert_to_postfix(expression)
            except ValueError as e:
                error = str(e)

    return render_template(
        'infix_postfix.html',
        expression=expression,
        postfix=postfix,
        error=error
    )


@app.route('/works/queue', methods=['GET', 'POST'])
def queue():
    message = None

    if request.method == 'POST':
        action = request.form.get('action')
        value = request.form.get('value', '').strip()

        if action == 'ENQUEUE':
            if not value:
                message = "Please enter a value."
            else:
                my_queue.enqueue(value)
                message = f"Added '{value}' to the queue."

        elif action == 'DEQUEUE':
            removed = my_queue.dequeue()

            if removed is None:
                message = "The queue is empty."
            else:
                message = f"Removed '{removed}' from the queue."

    return render_template(
        'queue.html',
        items=my_queue.to_list(),
        message=message
    )


def bubble_sort(nums):
    nums = nums.copy()

    for i in range(len(nums)):
        for j in range(len(nums) - i - 1):
            if nums[j] > nums[j + 1]:
                nums[j], nums[j + 1] = nums[j + 1], nums[j]

    return nums


def selection_sort(nums):
    nums = nums.copy()

    for i in range(len(nums)):
        small = i

        for j in range(i + 1, len(nums)):
            if nums[j] < nums[small]:
                small = j

        nums[i], nums[small] = nums[small], nums[i]

    return nums


def insertion_sort(nums):
    nums = nums.copy()

    for i in range(1, len(nums)):
        current = nums[i]
        j = i - 1

        while j >= 0 and nums[j] > current:
            nums[j + 1] = nums[j]
            j -= 1

        nums[j + 1] = current

    return nums


def merge_sort(nums):
    if len(nums) <= 1:
        return nums

    middle = len(nums) // 2
    left = merge_sort(nums[:middle])
    right = merge_sort(nums[middle:])

    result = []

    while left and right:
        if left[0] <= right[0]:
            result.append(left.pop(0))
        else:
            result.append(right.pop(0))

    return result + left + right


def quick_sort(nums):
    if len(nums) <= 1:
        return nums

    pivot = nums[-1]
    left = [x for x in nums[:-1] if x <= pivot]
    right = [x for x in nums[:-1] if x > pivot]

    return quick_sort(left) + [pivot] + quick_sort(right)


@app.route('/works/sorting', methods=['GET', 'POST'])
def sorting():
    numbers = ''
    result = ''
    algorithm = 'bubble'
    error = ''

    if request.method == 'POST':
        numbers = request.form.get('numbers', '').strip()
        algorithm = request.form.get('algorithm', 'bubble')

        try:
            nums = [int(x.strip()) for x in numbers.split(',')]

            if not numbers:
                raise ValueError

            if algorithm == 'bubble':
                result = bubble_sort(nums)
            elif algorithm == 'selection':
                result = selection_sort(nums)
            elif algorithm == 'insertion':
                result = insertion_sort(nums)
            elif algorithm == 'merge':
                result = merge_sort(nums)
            elif algorithm == 'quick':
                result = quick_sort(nums)
            else:
                raise ValueError

        except ValueError:
            error = "Please enter valid numbers separated by commas."

    return render_template(
        'sorting.html',
        numbers=numbers,
        result=result,
        algorithm=algorithm,
        error=error
    )


if __name__ == "__main__":
    app.run(debug=True)