from flask import Flask, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///test.db'
db = SQLAlchemy(app)


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        name = request.form['book-name']
        publisher_name = request.form['publisher-name']
        publisher_age = int(request.form['publisher-age'])
        publish_date = datetime.strptime(request.form['publish-date'], '%Y-%m-%d').date()
        book_type = request.form.getlist('book-type')
        book_type = ', '.join(book_type)

        new_book = Book(name=name, publisher_name=publisher_name, publisher_age=publisher_age, publish_date=publish_date, book_type=book_type)
        db.session.add(new_book)
        db.session.commit()
        return redirect('/booklist')
    else:
        return render_template('index.html')

@app.route('/booklist')
def booklist():
    books = Book.query.order_by(Book.publish_date).all()
    return render_template('booklist.html', books=books)

@app.route('/delete/<int:id>')
def delete(id):
    book_to_delete = Book.query.get(id)
    db.session.delete(book_to_delete)
    db.session.commit()
    return redirect('/booklist')

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    book = Book.query.get_or_404(id)
    if request.method == 'POST':
        book.name = request.form['book-name']
        book.publisher_name = request.form['publisher-name']
        book.publisher_age = request.form['publisher-age']
        publish_date_str = request.form['publish-date']
        publish_date = datetime.strptime(publish_date_str, '%Y-%m-%d').date()
        book.publish_date = publish_date
        book.book_type = request.form['book-type']
        db.session.commit()
        return redirect('/booklist')
    else:
        return render_template('update.html', book=book)
    
@app.route('/report')
def report():
    books = Book.query.order_by(Book.id)
    return render_template('report.html', books=books)



class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    publisher_name = db.Column(db.String(200), nullable=False)
    publisher_age = db.Column(db.Integer, nullable=False)
    publish_date = db.Column(db.Date, nullable=False)
    book_type = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return '<Book %r>' % self.name