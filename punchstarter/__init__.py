from flask import Flask, render_template, redirect, url_for, request, abort 
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.script import Manager
import datetime
import cloudinary.uploader


app = Flask(__name__)
app.config.from_object('punchstarter.default_settings')
manager = Manager(app)


db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)


from models import *

@app.route("/")
def hello():
#Sorting projects by date created desc
	projects = db.session.query(Project).order_by(Project.time_created.desc()
		).limit(15)
	return render_template("index.html", projects=projects)

@app.route("/projects/create",methods=['GET','POST'])
def create():
#Creating a new project
	if request.method == "GET":
	    return render_template("create.html")
	if request.method == "POST":
#Handle The Form Submission
 		now = datetime.datetime.now()
    	time_end = request.form.get("funding_end_date")
    	time_end = datetime.datetime.strptime(time_end, "%Y-%m-%d")
#Upload The Cover Photo
    	cover_photo = request.files['cover_photo']
    	uploaded_image = cloudinary.uploader.upload(
    		cover_photo,
    		crop='limit',
    		width=680,
    		height=580)
    	image_filename = uploaded_image["public_id"]
    	new_project= Project(
    		member_id=1,
    		name=request.form.get("project_name"),
    		short_description=request.form.get("short_description"),
    		long_description=request.form.get("long_description"),
    		goal_amount=request.form.get("funding_goal"),
    		image_filename=image_filename,
    		time_start=now,
    		time_end=time_end,
    		time_created=now)
    	db.session.add(new_project)
    	db.session.commit()
    	return redirect(url_for('project_detail', project_id=new_project.id))

@app.route("/projects/<int:project_id>/")
def project_detail(project_id):
#Displaying all projects details
	project = db.session.query(Project).get(project_id)
	if project is None:
		abort(404)
	return render_template("project_detail.html", project=project)


@app.route("/projects/<int:project_id>/pledge/", methods=['GET', 'POST'])
def pledge(project_id):
#How pledge works is handled here
	if request.method == "GET":
		project = db.session.query(Project).get(project_id)
		if project is None:
			abort(404)
		return render_template("pledge.html", project=project)
	if request.method == "POST":
		guest_pledgor = db.session.query(Member).filter_by(id=1).one()
		new_pledge = Pledge(
			amount=request.form.get("amount"),
			time_created=datetime.datetime.now(),
			project_id=project.id,
			member_id=guest_pledgor.id)

		db.session.add(new_pledge)
		db.session.commit()
		return redirect(url_for('project_detail'), project_id=project_id)

@app.route('/search/')
def search():
#Search For Projects Is Handled Here
	query = request.args.get("q") or ""
	projects = db.session.query(Project).filter(
		Project.name.ilike('% ' + query + '%') |
		Project.long_description.ilike('% ' + query + '%') |
		Project.short_description.ilike('% ' + query + '%')

		).all()
	project_count = len(projects)
	return render_template('search.html',
		query_text=query,
		projects=projects,
		project_count=project_count)
