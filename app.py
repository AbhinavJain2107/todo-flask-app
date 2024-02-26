from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///TOdo.db"
db = SQLAlchemy(app)

class TOdo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"

@app.route('/', methods=['GET','POST'])
def hello_world():
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']

        todo = TOdo(title=title, desc=desc)
        db.session.add(todo)
        db.session.commit()
    allTOdo = TOdo.query.all()
    print(allTOdo)
    return render_template('index.html', allTOdo=allTOdo)

@app.route('/update/<int:sno>', methods=['GET','POST'])
def update(sno):
    if request.method=='POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = TOdo.query.get_or_404(sno)
        todo.title = title
        todo.desc = desc
        db.session.add(todo)
        db.session.commit()
        return redirect("/")
    todo = TOdo.query.get_or_404(sno)
    return render_template('update.html', todo = todo)


@app.route('/delete/<int:sno>')
def delete(sno):
    todo = TOdo.query.get_or_404(sno)
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)