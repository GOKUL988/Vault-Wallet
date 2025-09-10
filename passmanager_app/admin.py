from django.contrib import admin
from .models import login_data, user_dt, info_db, notes_db, notes_con
# Register your models here.
admin.site.register(login_data)
admin.site.register(user_dt)
admin.site.register(info_db)
admin.site.register(notes_db)   
admin.site.register(notes_con) 