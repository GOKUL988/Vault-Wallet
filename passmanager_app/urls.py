from django.urls import path 
from .import views 
urlpatterns = [
    path("", views.login, name="login"),   
    path("signup", views.signup, name="signup"), 
    path("base",views.base, name="base"), 
    path("pass_source", views.pass_source, name="pass_source"),
    path("logout",views.logout, name="logout"),
    path("view_pass/<uuid:acc_id>",views.view_pass, name="view_pass"),
    path("add_pass", views.add_pass, name="add_pass"), 
    path("info_base", views.info_base, name= "info_base"),  
    path("add_info", views.add_info, name="add_info.html"), 
    path("dt_info/<uuid:info_acc_id>", views.dt_info, name= "dt_info"),
    path("note_base", views.note_base, name="note_base"),
    path("note_add", views.note_add, name="note_add"), 
    path("notes_dt/<notes_acc_id>" , views.notes_dt, name="notes_dt"),
]