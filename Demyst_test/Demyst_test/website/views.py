from website.all_functions import get_account_statement , get_preAssessment,get_decision_engine
from flask import session ,Blueprint, render_template, request, flash, jsonify ,redirect, url_for
from flask_login import login_required, current_user
from .models import Loan
from . import db
import json

views = Blueprint('views', __name__)


@views.route('', methods=['GET', 'POST'])
@login_required
def home():
    
    loan_user = Loan.query.get(current_user.id)
    if loan_user:
        data ={}
        data["decison"] = True
        data["account"] = loan_user.account_number
        data["buisness"] = loan_user.buisness_name
        return render_template("submit.html", user=current_user, data =  data)   

    if request.method == 'POST':                      
        account =  request.form.get('account')
        buisness = request.form.get('buisness')
        provider = request.form.get('provider')
        loan = request.form.get('Loan')
        sheet =  get_account_statement(account , buisness)
        data =  {"account": int(account), "buisness": buisness, "provider": provider, "loan":int(loan) ,"sheet":sheet}
        session["data"] = json.dumps(data)
        return redirect(url_for('views.review'))
    
    return render_template("home.html", user=current_user)
       
    
@views.route('/review', methods=['GET', 'POST'])
@login_required
def review():
    data = session.get("data", None)
    data = json.loads(data)
    
    if data and request.method == "GET":
        return render_template("review.html", user=current_user , data = data)
    
    if data and request.method == 'POST':
        profit , preAssessment = get_preAssessment(data["sheet"], data["loan"])
        data["profit"] = profit
        data["preAssessment"] = preAssessment
        data["year"] = 1990
        data["decision"]  =  get_decision_engine(data["account"] , data["buisness"],data["profit"], data["preAssessment"])
        session["data"] = data        
        return redirect(url_for('views.submit'))
    
    return  redirect(url_for('views.home'))

@views.route('/submit', methods=['GET', 'POST'])
@login_required
def submit():
    data =  session.get("data", None)
    if data:
        new_loan = Loan(account_number = data["account"], profit = data["profit"], buisness_name = data["buisness"]  , approved = data["decision"] , user_id = current_user.id)
        db.session.add(new_loan)
        db.session.commit()
        flash('Added to database', category='success')
        session.clear()
        return render_template("submit.html", user=current_user, data =  data)
    return  redirect(url_for('views.home')) 

