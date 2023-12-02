from flask import Flask, render_template, redirect, url_for
from flask_ckeditor import CKEditor, CKEditorField

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired

application = Flask(__name__)
ckeditor = CKEditor(application)

application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
application.config['SECRET_KEY'] = 'your_secret_key'
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
    return render_template('projects.html', projects=projects)

@application.route('/project/<int:project_id>')
def project_detail(project_id):
    project = Project.query.get_or_404(project_id)
    return render_template('project_detail.html', project=project)


@application.route('/create_project', methods=['GET', 'POST'])
def create_project():
    form = ProjectForm()

    if form.validate_on_submit():
        project = Project(
            title=form.title.data,
            description=form.description.data,
            image=form.image.data,
            article=form.article.data
        )

        db.session.add(project)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('create_project.html', form=form)


if __name__ == '__main__':
    application.run(debug=True)
