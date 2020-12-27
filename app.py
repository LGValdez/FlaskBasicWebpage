from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)
default_page = redirect('/')

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        html_input_id = 'content'
        task_content = request.form[html_input_id]
        new_task = Todo(content=task_content)
        return_page = default_page
        try:
            db.session.add(new_task)
            db.session.commit()
        except:
            return_page = 'There was an issue adding your task :('

        return return_page

    else:
        db_tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=db_tasks)


@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)
    return_page = default_page
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
    except:
        return_page = 'There was an issue deleting your task :('
    return return_page

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task_to_update = Todo.query.get_or_404(id)
    return_page = default_page
    if request.method == 'POST':
        html_input_id = 'content'
        task_to_update.content = request.form[html_input_id]
        try:
            db.session.commit()
        except:
            return_page = 'There was an issue updating your task :('
    else:
        return_page = render_template('update.html', task=task_to_update)
    return return_page


if __name__ == '__main__':
    app.run(debug=True)
