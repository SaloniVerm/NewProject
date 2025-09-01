from django.db import models

# Create your models here.
class USEROTP(models.Model):

     otp_code = models.CharField(max_length=6)  # Assuming OTP is a 6-digit code
     type = models.CharField(max_length=10)
     email = models.CharField(max_length=100)

     created_at = models.DateTimeField(auto_now_add=True)
    
     class Meta:
         db_table = 'otp'
         managed=False
        
        

# class DummyTest(models.Model):
#     # Define the fields corresponding to the table columns
#     # Assuming `id` is the primary key and auto-incremented
#     # id = models.AutoField(primary_key=True)
#     randNum = models.IntegerField()
#     managed=False
    

   

#     class Meta:
#         # Set the table name to match the existing MySQL table
#         db_table = 'dummy_test'

'''from django.db import models

class RegisteredUser(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)  # Store hashed in real app
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email'''
'''class ZqUser(models.Model):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    is_active = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    referral_id = models.CharField(max_length=50, blank=True, null=True)
    joined_on = models.DateTimeField(auto_now_add=True)'''
