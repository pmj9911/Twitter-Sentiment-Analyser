from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
	Username = models.OneToOneField(User, default=None, on_delete=models.PROTECT)
	First_Name = models.CharField(max_length=100)
	Last_Name = models.CharField(max_length=100)
	Email_Address = models.EmailField()
	Age = models.IntegerField(default='18')
	#Date_Of_Birth = models.DateTimeField()
	Profile_Pic =  models.ImageField(upload_to='ProfilePics/',default='ProfilePics/default.jpg',blank=True, null=True)    

	def __str__(self):
		return self.First_Name + " " + self.Last_Name +"\t" +self.Email_Address

	def delete(self, *args, **kwargs):
		self.Profile_Pic.delete()
		super().delete(*args, **kwargs)

	# def save(self):
	# 	super().save()
	# 	img = Image.open(self.image.path)
	# 	if img.height > 300 or img.width > 300:
	# 		output_size = (300, 300)
	# 		img.thumbnail(output_size)
	# 		img.save(self.image.path)