from flask import Flask, request, Response
from flask_sqlalchemy import SQLAlchemy

from validators import check_if_data_is_correct
from edit_data_functions import serialize_data_in_every_object, prepare_response_obj, \
    sort_by_date_and_change_to_proper_date_format

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users_reports.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class UsersReports(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    last_report = db.Column(db.Text, nullable=True)

    def __init__(self, last_report):
        self.last_report = last_report


def create_report(req):
    if req.content_type != "application/json":
        return Response("400 Bad Request", status=400)

    if check_if_data_is_correct(req.json) is False:
        return Response("400 Bad Request", status=400)

    data = serialize_data_in_every_object(req.json)
    data = prepare_response_obj(data)
    data = sort_by_date_and_change_to_proper_date_format(data)
    return {"Response": data}


@app.route("/report", methods=['POST'])
def report():
    return create_report(request)


@app.route("/customer-report", methods=['POST'])
def create_reports_with_user_id():
    user = request.json["user_id"]
    del request.json['user_id']
    created_report = create_report(request)
    found_user = UsersReports.query.filter_by(_id=user).first()
    if found_user is None:
        new_user_report = UsersReports(str(created_report))
        db.session.add(new_user_report)
        db.session.commit()
    elif found_user:
        found_user.last_report = str(created_report)
        db.session.commit()
    else:
        return Response("400 Bad Request", status=400)
    return created_report


@app.route("/customer-report/<customer_id>", methods=['GET'])
def get_reports_with_user_id(customer_id):
    found_user = UsersReports.query.filter_by(_id=customer_id).first()
    if found_user:
        return eval(found_user.last_report)
    elif found_user is None:
        return Response("404 Not Found", status=404)
    else:
        return Response("400 Bad Request", status=400)


if __name__ == "__main__":
    app.run(debug=True)
