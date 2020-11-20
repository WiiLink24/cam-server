print('PLEASE CLEAN webpanel.py')
from cam import app
from models import Servlet, FileServlet # Non-existent at the time of writing this

class StatusForm(Form):
    choices = ['OK','Maintaince']
    status = SelectField('Status', choices = choices, validators = [Required()])
app.config['SECRET_KEY'] = 'changemii'
lock_debug = True # Do not set to False until further notice
if lock_debug:
     print('[ERROR] webpanel is imported, but is locked!')
     exit()
@app.route('/wp/status')
def status():
    form = StatusForm()
    return render_template('status.html')


    
