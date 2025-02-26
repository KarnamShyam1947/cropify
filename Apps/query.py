from os import name
from flask import Blueprint, redirect, render_template, request, session, url_for
from Models import AnswerModel, QueryModel, UserModel
from App import db

query = Blueprint("query", __name__)

@query.route("/all-queries")
def all_queries():
    queries = QueryModel.query.all()
    complete_queries = list()

    for query in queries:
        complete_queries.append((query, UserModel.query.filter_by(id=query.userId).first()))

    return render_template("query/all-queries.html", complete_queries=complete_queries)

@query.route("/queries-details")
def query_details():
    qid = request.args.get("qid")
    query = QueryModel.query.filter_by(id=qid).first()
    user = UserModel.query.filter_by(id=query.userId).first()

    return render_template("query/query-details.html", query=query, user=user)

@query.route("/add-replay", methods=['GET', 'POST'])
def add_replay():
    qid = request.args.get("qid")
    title = QueryModel.query.filter_by(id=qid).first()

    if request.method == "POST":
        qid = request.form.get("qid")
        ans = request.form.get("ans")
        name = session['name'] 

        reply = AnswerModel(text=ans, name=name, qid=qid)
        db.session.add(reply)
        db.session.commit()

        return redirect(url_for('query.all_queries'))
    
    return render_template("query/add-replay.html", title=title)
