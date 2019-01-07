from flask import Flask, render_template, url_for, redirect, request
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField ,SubmitField
from wtforms.validators import DataRequired 
from flask_sqlalchemy import SQLAlchemy
from flask import Flask



app = Flask(__name__ ,static_folder='static')


app.config['SECRET_KEY']='f7838bfc44ecec42b34dd48f5e626999'

# DATABASE CREATION
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///todo.db'
db = SQLAlchemy(app)



class List(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    items = db.Column(db.String(120),nullable=False)
   
    

    def __repr__(self):
        return f"List('{self.items}')"

#form creation 

class TodoForms(FlaskForm):
    item = StringField('item', validators=[DataRequired()])
   
    submit = SubmitField('add')





@app.route('/', methods=['GET','POST'])
def home():

    form = TodoForms()
    if form.validate_on_submit():
        task = List(items=form.item.data)
        db.session.add(task)
        db.session.commit()
        return redirect(url_for('home'))

    collections = List.query.all()

    
    return render_template('todo.html', form=form, collections=collections)


@app.route('/list/<int:list_id>', methods=['GET','POST'])
def list(list_id):
    itemize= List.query.get_or_404(list_id)
    form = TodoForms()
    if request.method == "GET":
        form.item.data = itemize.items

    else:
        if form.validate_on_submit:
            itemize.items = form.item.data 
            db.session.commit()
            return redirect(url_for('home'))

    

    return render_template('list.html', itemize=itemize, form=form)


@app.route('/list/<int:list_id>/delete',methods=["POST"])
def delete_list(list_id):
    itemize = List.query.get_or_404(list_id)
    db.session.delete(itemize)
    db.session.commit()
    return redirect(url_for('home'))



if __name__=='__main__': 
    app.run(debug=True) 