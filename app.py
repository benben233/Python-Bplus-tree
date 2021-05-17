from flask import Flask, render_template, request
from bplustree import BPlusTree

app = Flask(__name__)
bplustree = BPlusTree()

app.config['Save_Path'] = './partfile.txt'


@app.route('/')
def initialization():
    with open(app.config['Save_Path'], 'rb') as reader:
        bplustree.readfile(reader)

    return render_template('index.html', data=display_the_next_10_parts(bplustree.leftmost_leaf()),
                           output=bplustree.output())


@app.route("/transaction", methods=["POST"])
def transaction():
    button = request.form['submit_button']
    key = str(request.form["key"])
    print(button, key)

    if button == 'query':
        leaf = bplustree.find(key)
        if key not in leaf.keys:
            return render_template('index.html', key=key, error=key + ' is not found',
                                   data=display_the_next_10_parts(leaf, key), output=bplustree.output())
        else:
            return render_template('index.html', key=key, value=leaf[key], success='found ' + key,
                                   data=display_the_next_10_parts(leaf, key), output=bplustree.output())

    elif button == 'insert':
        value = request.form['value']
        flag, leaf = bplustree.insert(key, value)
        if flag is False:
            return render_template('index.html', key=key, value=value, error='Already have same ID',
                                   data=display_the_next_10_parts(leaf, key), output=bplustree.output())
        else:
            return render_template('index.html', key=key, value=value, success=key + ' is inserted',
                                   data=display_the_next_10_parts(leaf, key), output=bplustree.output())

    elif button == 'change':
        value = request.form['value']
        flag, leaf = bplustree.change(key, value)
        if flag is False:
            return render_template('index.html', key=key, value=value, error=key + ' is not found',
                                   data=display_the_next_10_parts(leaf, key), output=bplustree.output())
        else:
            return render_template('index.html', key=key, value=value,
                                   success='the Description of ' + key + ' is changed',
                                   data=display_the_next_10_parts(leaf, key), output=bplustree.output())

    elif button == 'delete':
        leaf = bplustree.find(key)
        if key not in leaf.keys:
            return render_template('index.html', key=key, error=key + ' is not found',
                                   data=display_the_next_10_parts(leaf, key), output=bplustree.output())
        else:
            bplustree.delete(key, leaf)
            leaf = bplustree.find(key)
            return render_template('index.html', key=key, success='delete ' + key,
                                   data=display_the_next_10_parts(leaf), output=bplustree.output())

    else:
        raise


def display_the_next_10_parts(leaf, key=None):
    if key is None:
        if len(leaf.keys) == 0:
            return None

        i = 0
    else:
        if key in leaf.keys:
            i = leaf.keys.index(key)
        else:
            i = leaf.index(key)

    data = []
    count = 0
    while count < 10:
        for i in range(i, len(leaf.keys)):
            data += [[leaf.keys[i], leaf.values[i]]]
            count += 1
        if leaf.next is None:
            break
        else:
            leaf = leaf.next
            i = 0

    return data


@app.route('/uploader', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        button = request.form['submit_button']
        if button == 'upload':
            f = request.files['file']
            bplustree.readfile(f)

            return render_template('index.html', data=display_the_next_10_parts(bplustree.leftmost_leaf()),
                                   success='File Loaded', output=bplustree.output())

        elif button == 'save':
            keys = []
            values = []
            leaf = bplustree.leftmost_leaf()
            while leaf is not None:
                keys += leaf.keys
                values += leaf.values
                leaf = leaf.next
            with open(app.config['Save_Path'], 'w') as writer:
                for i, key in enumerate(keys):
                    writer.write(key + '        ' + values[i])
            return render_template('index.html', data=display_the_next_10_parts(bplustree.leftmost_leaf()),
                                   success='File Saved', output=bplustree.output())


if __name__ == '__main__':
    app.run()
