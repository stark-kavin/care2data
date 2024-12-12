from django.db import models


class Phase(models.Model):
    name = models.CharField(null=False,max_length=20)

    def __str__(self):
        return self.name

class Sponser(models.Model):
    name     = models.CharField(null=False,max_length=20)
    contact  = models.CharField(null=True,max_length=20,blank=True)

    def __str__(self):
        return self.name

class Study(models.Model):
    name    = models.CharField(null=False,max_length=20)
    phase   = models.ForeignKey(Phase,on_delete=models.SET_NULL,null=True)
    sponser = models.ForeignKey(Sponser,on_delete=models.SET_NULL,null=True)
    discription = models.CharField(null=True,max_length=50,blank=True)

    def __str__(self):
        return self.name