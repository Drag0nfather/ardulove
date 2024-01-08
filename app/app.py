import os
import random

from flask import Flask, render_template, redirect, url_for, send_from_directory, request, flash
from flask_ckeditor import CKEditor, CKEditorField, upload_fail, upload_success

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired

application = Flask(__name__)
ckeditor = CKEditor(application)

application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
application.config['SECRET_KEY'] = 'your_secret_key'
application.config['UPLOAD_FOLDER'] = 'app/static/images'
application.config['CKEDITOR_FILE_UPLOADER'] = '/upload'
application.config['CKEDITOR_ENABLE_CSRF'] = True

csrf = CSRFProtect(application)
db = SQLAlchemy(application)
migrate = Migrate(application, db)


class Instruction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(100), nullable=False)
    marketplace_link = db.Column(db.String(100), nullable=False)


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(100), nullable=False)
    article = db.Column(db.Text, nullable=False)


class ProjectForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    image = StringField('Image', validators=[DataRequired()])
    article = CKEditorField('Article', validators=[DataRequired()])

    class Meta:
        csrf = True


# Роуты для отображения страниц
@application.route('/')
def index():
    return render_template('index.html')

@application.route('/instructions')
def instructions():
    instructions = Instruction.query.all()
    return render_template('instructions.html', instructions=instructions)

@application.route('/products')
def products():
    products = Product.query.all()
    return render_template('products.html', products=products)


@application.route('/projects')
def projects():
    projects = Project.query.all()
    return render_template('projects/projects.html', projects=projects)


@application.route('/project/<int:project_id>')
def project_detail(project_id):
    project = Project.query.get_or_404(project_id)
    return render_template('projects/project_detail.html', project=project)


@application.route('/create_project', methods=['GET', 'POST'])
def create_project():
    form = ProjectForm()

    if form.validate_on_submit():
        # Handle file upload
        image = form.image.data
        if image:
            image_path = os.path.join(application.config['UPLOAD_FOLDER'], image.filename)
            image.save(image_path)
        else:
            image_path = None

        # Create a new Project instance and save it to the database
        project = Project(
            title=form.title.data,
            description=form.description.data,
            image=image.filename,
            article=form.article.data
        )

        db.session.add(project)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('projects/create_project.html', form=form)


@application.route('/files/<path:filename>')
def uploaded_files(filename):
    path = 'static/images'
    return send_from_directory(path, filename)


@application.route('/upload', methods=['POST'])
def upload():
    f = request.files.get('upload')
    extension = f.filename.split('.')[-1].lower()
    if extension not in ['jpg', 'gif', 'png', 'jpeg']:
        return upload_fail(message='Image only!')
    target_directory = 'app/static/images'
    if not os.path.exists(target_directory):
        os.makedirs(target_directory)
    random_num = random.randint(1000000000000, 10000000000000)
    filename = str(random_num) + '-' + f.filename
    f.save(os.path.join(target_directory, filename))
    url = url_for('uploaded_files', filename=filename)
    return upload_success(url, filename=filename)


if __name__ == '__main__':
    application.run(debug=True)
