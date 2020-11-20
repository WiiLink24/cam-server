print('PLEASE CLEAN webpanel.py')
from cam import app, db
from models import Servlet, FileServlet # Non-existent at the time of writing this
from wtforms import *
from wtforms.validators import *
class StatusForm(Form):
    choices = ['OK','Maintaince']
    status = SelectField('Status', choices = choices, validators = [DataRequired()])
app.config['SECRET_KEY'] = 'changemii'
lock_debug = True # Do not set to False until further notice
if lock_debug:
     print('[ERROR] webpanel is imported, but is locked!')
     exit()
@app.route('/wp/status',methods=['GET','POST'])
def status():
    form = StatusForm()
    status_codes = {'OK':1000,'Maintaince':1040}
    if form.validate_on_submit():
        # Get Servlet
        servlet = Servlet.query.first()
        # Change servlet status code
        servlet.status_code = status_codes[form.status.data]
        # Track servlet
        db.session.add(servlet)
        # Commit tracked data
        db.session.commit()
        
    return render_template('status.html',form=form)


    
