from django.db import models 
import string,numbers, uuid, random

# Create your models here.
class login_data(models.Model): 
    us_in = models.UUIDField(primary_key=True, editable=False,default=uuid.uuid4,unique=True) 
    username  = models.CharField(max_length=50)  
    email= models.EmailField(max_length=30) 
    passwrd = models.CharField(max_length=300) 
    
    def __str__(self):
        return f'{self.us_in}' 

class user_dt(models.Model): 
    acc_id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, unique=True)
    user_inf = models.ForeignKey(login_data, on_delete=models.CASCADE) 
    site = models.CharField(max_length=50)
    link = models.URLField(max_length=100) 
    user_name = models.CharField(max_length=50, null=True) 
    password = models.CharField(max_length=400) 
    category = models.CharField(max_length=50 , null=True) 
    Notes = models.CharField(max_length=500, null=True)  

    def __str__(self):
       return f'{self.user_inf}'
    
class info_db(models.Model): 
    user_inf_pi = models.ForeignKey(login_data, on_delete=models.CASCADE)
    info_acc_id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    firstnme= models.CharField(max_length=30) 
    middlenme = models.CharField(max_length=30)  
    lastnme = models.CharField(max_length=30) 
    email = models.EmailField() 
    dob = models.DateField(null= True) 
    phone = models.CharField(max_length=50)
    address = models.CharField(max_length=100) 
    pin = models.CharField(max_length=50) 
    city = models.CharField(max_length=50) 
    state = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    organizations = models.CharField(max_length=150) 

    def __str__(self):
        return f'{self.user_inf_pi}' 
    
class notes_db(models.Model): 
    user_inf_notes = models.ForeignKey(login_data, on_delete=models.CASCADE) 
    notes_acc_id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    note_name = models.CharField(max_length=50)   
    def __str__(self):
        return f'{self.notes_acc_id} - {self.note_name}' 
    
class notes_con(models.Model): 
    user_idf = models.ForeignKey(notes_db, on_delete=models.CASCADE)
    note_con = models.TextField()     

    def __str__(self):
        return f'{self.user_idf}-{self.pk}'