import requests
from flask import Blueprint, render_template, request, current_app, redirect, url_for
# from blog.views.users import USERS
from typing import Dict
from sqlalchemy.orm import joinedload
from werkzeug.exceptions import NotFound
from flask_login import login_required, current_user
from sqlalchemy.exc import IntegrityError

from Flask_doc.docs.config import API_URL
from Flask_doc.docs.models.database import db
from Flask_doc.docs.models.docs import Documents
from Flask_doc.docs.forms.document import CreateDocumentForm

documents_app = Blueprint("documents_app", __name__, url_prefix='/documents', static_folder='../static')


@documents_app.route("/", endpoint="list")
def documents_list():
    documents = Documents.query.filter_by(version='0').all()
    count_documents = len(documents)
    return render_template("documents/list.html", documents=documents, count_documents=count_documents)


@documents_app.route("/<int:document_id>/", endpoint="details")
def document_details(document_id):
    document = Documents.query.filter_by(id=document_id).one_or_none()
    if document is None:
        raise NotFound
    return render_template("documents/details.html", document=document)


@documents_app.route("/create/", methods=["GET", "POST"], endpoint="create")
@login_required
def create_document():
    error = []
    form = CreateDocumentForm(request.form)
    if request.method == "POST" and form.validate_on_submit():
        document = Documents(name=form.name.data.strip(), body=form.body.data, version='0')
        db.session.add(document)
        try:
            db.session.commit()
        except IntegrityError:
            current_app.logger.exception("Could not create a new document!")
            error.append("Could not create document!")
        else:
            return redirect(url_for("documents_app.details", document_id=document.id))

    return render_template("documents/create.html", form=form, error=error)


@documents_app.route("/del/<int:document_id>/", endpoint="delete")
def document_delete(document_id):
    document = Documents.query.filter_by(id=document_id).one_or_none()
    if document is None:
        raise NotFound
    else:
        document.version = 'D'
        db.session.commit()
    return redirect(url_for("documents_app.list"))


@documents_app.route("/edit/<int:document_id>/", methods=["GET", "POST"], endpoint="edit")
def document_edit(document_id):
    document = Documents.query.filter_by(id=document_id).one_or_none()
    error = []
    form = CreateDocumentForm(request.form)
    form.name.data = document.name
    form.body.data = document.body
    if request.method == "POST" and form.validate_on_submit():
        form = CreateDocumentForm(request.form)
        docs_version = Documents.query.filter_by(id_main=document_id).all()
        if not docs_version:
            vers = 1
        else:
            vers = 0
            for docs in docs_version:
                if (docs.name == form.name.data.strip()) and (docs.name == form.body.data):
                    error.append("Такая версия уже есть")
                    docs.version = 'D'
                    docs.id_main = None
                    vers = None
                    break
                if int(docs.version) > vers:
                    vers = int(docs.version) + 1
        if vers != None:
            document_new = Documents(name=document.name, body=document.body, version=f'{vers}', id_main=document.id)
            db.session.add(document_new)
        document.name = form.name.data.strip()
        document.body = form.body.data

        try:
            db.session.commit()
        except IntegrityError:
            current_app.logger.exception("Could not edit a this document!")
            error.append("Could not edit document!")
        else:
            return redirect(url_for("documents_app.details", document_id=document.id))

    return render_template("documents/edit.html", form=form, error=error)
