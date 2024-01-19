from django.db import models



class UserProfile(models.Model):
    id = models.AutoField(primary_key=True, db_column="id")
    username = models.CharField(max_length=250, unique=True,null=False)
    password = models.TextField(max_length=250,db_column='password',null=False)

    

    class Meta:
        managed = False
        db_table = 'user_profile'

    def __str__(self):
        return f"UserProfile(id={self.id},username='{self.username}')"
    

    
    





    

