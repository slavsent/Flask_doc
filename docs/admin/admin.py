from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
import Flask_doc.docs.models
from Flask_doc.docs.models.database import db
from flask import redirect, url_for
from flask_login import current_user
from flask_admin import Admin, AdminIndexView, expose


# Customized admin interface
class CustomView(ModelView):

    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_staff

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for("auth_app.login"))


class MyAdminIndexView(AdminIndexView):

    @expose("/")
    def index(self):
        if not (current_user.is_authenticated and current_user.is_staff):
            return redirect(url_for("auth_app.login"))
        return super(MyAdminIndexView, self).index()


# Create admin with custom props
admin = Admin(
    name="Document Admin",
    index_view=MyAdminIndexView(),
    template_mode="bootstrap4",
)

# Create admin with custom base template
admin = Admin(name="Document Admin", template_mode="bootstrap4")


class UserAdminView(CustomView):
    column_exclude_list = ("password",)
    column_details_exclude_list = ("password",)
    column_searchable_list = ("first_name", "last_name", "username", "is_staff", "email")
    column_filters = ("first_name", "last_name", "username", "is_staff", "email")
    column_editable_list = ("first_name", "last_name", "is_staff")
    can_create = True
    can_edit = True
    can_delete = False


class DocumentAdminView(CustomView):
    column_searchable_list = ("name",)
    column_filters = ("name", "body", "dt_created", "version", "id_main")
    column_list = ("name", "body", "dt_created", "version", "id_main")
    can_export = True
    export_types = ["csv", "xlsx"]
    create_modal = True
    edit_modal = True


# Add views
admin.add_view(DocumentAdminView(Flask_doc.docs.models.Documents, db.session, category="Models"))
admin.add_view(UserAdminView(Flask_doc.docs.models.User, db.session, category="Models"))
