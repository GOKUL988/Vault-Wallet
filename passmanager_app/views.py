from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.models import User  
from django.contrib.auth.hashers import check_password, make_password
from django.contrib import messages 
from .models import login_data,user_dt, info_db, notes_db, notes_con
from cryptography.fernet import Fernet 
from dotenv import load_dotenv 
import os
from django.db.models import Q
from datetime import datetime
# Create your views here.
load_dotenv() 
key = os.getenv("_KEY") 
cipher = Fernet(key.encode())

def login(request): 
    if request.method == "POST":
        email = request.POST.get("email") 
        mast_pass = request.POST.get("password") 
        if login_data.objects.filter(email = email).exists(): 
            log_data = login_data.objects.get(email = email)
            un_id = log_data.us_in
            if check_password(mast_pass, log_data.passwrd): 
                request.session['access_id'] = str(un_id)
                return redirect('pass_source') 
            else: 
                messages.error(request, "PASSWORD error re-type it") 
        else: 
            messages.warning(request, "Email not found")         
    return render(request, "login.html") 

def signup(request): 
    if request.method == "POST" :
        user_name = request.POST.get("username") 
        e_mail = request.POST.get("email") 
        pass_word = request.POST.get("password") 
        re_pass = request.POST.get("password_re") 
        if login_data.objects.filter(email = e_mail).exists(): 
            messages.warning(request, "MAIL ALREADY USED")
        elif pass_word != re_pass: 
            messages.warning(request, "Password does not match") 
        else: 
            ency_pass = make_password(pass_word)
            fin_data = login_data(
                username = user_name, 
                email = e_mail,  
                passwrd = ency_pass,
            )
            fin_data.save()
            return redirect('login')
    return render(request, "signup.html") 


def logout(request):
    request.session.flush()
    return redirect('login')

def base(request): 
    access_id = request.session.get('access_id') 
    if not access_id:
        return redirect('login') 
    else:
        user_id = login_data.objects.get(us_in = access_id) 
    con = {
        'a': user_id, 
    }
    return render(request, "base.html", con)

def pass_source(request):
    access_id = request.session.get('access_id') 
    if not access_id:
        return redirect('login') 
    try: 
        user_id = login_data.objects.get(us_in = access_id) 
        search_q = request.GET.get("pass_search") 
        if search_q: 
            info = user_dt.objects.filter(
                Q(site__icontains = search_q) , 
                user_inf = user_id,
            ).order_by("site")
        else:    
            info = user_dt.objects.filter(user_inf = user_id).order_by("site")
    except user_id.DoesNotExist:    
        return redirect('login')
    con = {
        'a':user_id,
        'b': info,
    }
    return render(request, "passwords/pass_source.html", con)
def add_pass(request): 
    access_id = request.session.get('access_id') 
    user_data1 = login_data.objects.get(us_in = access_id)
    if request.method == "POST": 
        site_a = request.POST.get("site_name") 
        link_a = request.POST.get("link_f") 
        user_a = request.POST.get("username") 
        pass_a = request.POST.get("pass_word") 
        cat_a = request.POST.get("cate") 
        note_a = request.POST.get("notes") 
        if access_id and key: 
            user_data = login_data.objects.get(us_in = access_id)
            enc_pass = cipher.encrypt(pass_a.encode()).decode()
            user_dt.objects.create(
                user_inf = user_data,
                site = site_a, 
                link = link_a,
                user_name = user_a,
                password = enc_pass,
                category = cat_a, 
                Notes = note_a
            ) 
            return redirect('pass_source')
        else: 
            if not access_id:
                return redirect('login')
            messages.error(request, "Key Required to save")
            raise Exception("⚠️ FERNET_KEY is missing. Please create a .env file based on .env.example.")
    con={
        'a':user_data1
    }
    return render(request, "passwords/add_pass.html",con)        


def view_pass(request, acc_id): 
    access_id = request.session.get('access_id')
    user_data = login_data.objects.get(us_in = access_id)
    if not access_id:
        return redirect('login')
    try:
        if key and access_id:
            det = get_object_or_404(user_dt, acc_id=acc_id)
            details = user_dt.objects.get(acc_id=det.acc_id)
            re_pg= details.acc_id
            print(re_pg)
            pas_enc = details.password     
            dec_pas = cipher.decrypt(pas_enc.encode()).decode()  

            if access_id: 
                if request.method == "POST": 
                    form_type = request.POST.get("form_type")

                    if form_type == "edit":
                        site_a= request.POST.get("site_edt") 
                        link_a = request.POST.get("link_edt") 
                        user_a = request.POST.get("user_edt") 
                        pass_a = request.POST.get("pass_edt")
                        cate_a = request.POST.get("cate_edt") 
                        res_a = request.POST.get("note_edt")

                        details.site = site_a 
                        details.link = link_a
                        details.user_name = user_a 
                        details.password = cipher.encrypt(pass_a.encode()).decode() 
                        details.category = cate_a
                        details.Notes =res_a 
                        details.save()
                        print("works on edit sections")
                        return redirect("view_pass", acc_id=details.acc_id)

                    elif form_type == "delete":
                        details.delete()
                        return redirect('pass_source')   
                    else:
                        print("some thing error in form section") 
            else:
                return redirect("login")      
    except user_data.DoesNotExist:
        return redirect('login')         
    con = {
        'a': user_data,
        'result': details,
        'pass': dec_pas
    }
    return render(request, "passwords/view_pass.html", con)

def info_base(request): 
    access_id = request.session.get('access_id') 
    user_data = login_data.objects.get(us_in = access_id)
    if not access_id: 
        return redirect("login")
    try:
        user_save_info = info_db.objects.filter(user_inf_pi = access_id)
    except access_id.DoesNotExist:
        return redirect("login")
    con = {
        'a':user_data,
        'b':user_save_info,
    }
    return render( request, "info/info_base.html",con) 

def add_info(request): 
    access_id = request.session.get('access_id') 
    user_data = login_data.objects.get(us_in = access_id)
    if not access_id:
        return redirect('login')
    else:
        if request.method == "POST" and access_id: 
            first_b = request.POST.get("first") 
            middle_b = request.POST.get("middle") 
            last_b = request.POST.get("last") 
            email_b = request.POST.get("email")
            dob_b = request.POST.get("dob")
            phone_b = request.POST.get("phone")
            address_b = request.POST.get("address")
            pincode_b = request.POST.get("pincode")
            city_b = request.POST.get("city")
            state_b = request.POST.get("state")
            country_b = request.POST.get("country")
            organi_b = request.POST.get("organi")

            dob_change = datetime.strptime(dob_b, "%d-%m-%Y").date()
            info_db.objects.create(
                user_inf_pi = user_data, 
                firstnme = first_b, 
                middlenme = middle_b, 
                lastnme = last_b ,
                email = email_b, 
                dob =dob_change, 
                phone = phone_b, 
                address = address_b, 
                pin = pincode_b, 
                city = city_b, 
                state = state_b, 
                country = country_b, 
                organizations = organi_b
            )
            return redirect('info_base')

    con = {
        'a':user_data
    }
    return render(request, "info/add_info.html",con)  

def dt_info(request, info_acc_id): 
    access_id = request.session.get("access_id") 
    user_info = login_data.objects.get(us_in = access_id)
    if not access_id: 
        return redirect('login')
    else:
        details = info_db.objects.get(info_acc_id= info_acc_id, user_inf_pi = user_info) 
        if request.method == "POST" and access_id:  
            form_type = request.POST.get("dt_tabs")
            if form_type == "info_edit":
                fstnme = request.POST.get("first_edt")
                midnme = request.POST.get("middle_edt")
                lstnme = request.POST.get("last_edt") 
                email_ = request.POST.get("email_edt") 
                dob_ = request.POST.get("dob_edt") 
                phone_ = request.POST.get("phone_edt") 
                add_ = request.POST.get("add_edt") 
                pin_ = request.POST.get("pin_edt") 
                city_ = request.POST.get("city_edt") 
                stat_ = request.POST.get("stat_edt") 
                count_ = request.POST.get("count_edt") 
                organi_ = request.POST.get("organ_edt") 
                dob_change = datetime.strptime(dob_, "%Y-%m-%d").date()
            
                details.firstnme = fstnme 
                details.middlenme = midnme  
                details.lastnme = lstnme 
                details.email = email_ 
                details.dob = dob_change 
                details.phone = phone_ 
                details.address = add_ 
                details.pin = pin_ 
                details.city = city_ 
                details.state = stat_ 
                details.country = count_ 
                details.organizations = organi_ 
                details.save()
            
            elif form_type == "info_del": 
                details.delete() 
                return redirect('info_base')    
    con={
        'a': user_info,
        'f' : details
    }
    return render(request, "info/dt_info.html", con)

def note_base(request): 
    access_id = request.session.get("access_id") 
    user_id = login_data.objects.get(us_in = access_id) 
    if not access_id: 
        return redirect('login') 
    else: 
        note_info = notes_db.objects.filter(user_inf_notes = user_id)
    con= {
        'a': user_id, 
        'note_data': note_info
    }    
    return render(request, "notes/note_base.html", con) 

def note_add(request): 
    access_id = request.session.get("access_id") 
    user_id = login_data.objects.get(us_in = access_id) 
    if not access_id and user_id:
        return redirect('login') 
    else: 
        if request.method == "POST" and user_id:
            file_name = request.POST.get("file_name") 
            fields = request.POST.getlist("field[]") 
            notesdb = notes_db.objects.create(
                user_inf_notes = user_id, 
                note_name= file_name
            ) 
            for note_con in fields:
                notes_con.objects.create( 
                    user_idf = notesdb,
                    note_con =cipher.encrypt(note_con.encode()).decode()
                )
            return redirect('note_base')    

    return render(request, "notes/note_add.html",{'a' :user_id}) 

def notes_dt(request,notes_acc_id): 
    access_id = request.session.get("access_id") 
    user_id = login_data.objects.get(us_in = access_id) 
    if not access_id and user_id: 
        return redirect('login') 
    else: 
        notes_access= get_object_or_404(notes_db, notes_acc_id = notes_acc_id , user_inf_notes = user_id) 
        note_dt = notes_con.objects.filter(user_idf = notes_access).order_by("pk") 
        for i in note_dt:
            i.note_con= cipher.decrypt(i.note_con.encode()).decode() 
        if request.method == "POST" and user_id:
            form_type = request.POST.get("note_dt")
            if form_type == "edit_notes": 
                field_edt = request.POST.getlist("field_edit[]") 
                for i, cont in enumerate(field_edt): 
                    obj = note_dt[i] 
                    obj.note_con = cipher.encrypt(cont.encode()).decode()
                    obj.save()
                return redirect("notes_dt", notes_acc_id = notes_access.notes_acc_id)    
            elif form_type =="del_notes": 
                field_opt = request.POST.getlist("inp_choice[]") 
                if not field_opt: 
                    notes_access.delete() 
                    return redirect('note_base')
                else:
                    for j in field_opt: 
                        obj_dele =  notes_con.objects.filter(user_idf = notes_access, pk = j)
                        print(obj_dele)
                        obj_dele.delete() 
                    return redirect("notes_dt", notes_acc_id = notes_access.notes_acc_id)      

            elif form_type == "add_fields" : 
                fields_add = request.POST.getlist("field[]")
                for i in fields_add: 
                    notes_con.objects.create(
                        user_idf = notes_access, 
                        note_con = cipher.encrypt( i.encode()).decode()
                    )     
                return redirect("notes_dt", notes_acc_id = notes_access.notes_acc_id)  
            else: 
                return redirect('note_base')                                        
    con={
        'note_acc': notes_access, 
        'details' : note_dt,
        'a': user_id,
    }
    return render(request, "notes/notes_dt.html", con) 