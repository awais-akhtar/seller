from django.db import models

class CoinOption(models.Model):
    coins = models.IntegerField()
    price = models.IntegerField()

    def __str__(self):
        return f"{self.coins} Coins"

class diamondsOption(models.Model):
    diamonds = models.IntegerField()
    price = models.IntegerField()

    def __str__(self):
        return f"{self.diamonds} Diamonds"
    

# class likeeinvoicemodel(models.Model):
#     invoice_id = models.CharField(max_length=100)
#     username = models.CharField(max_length=100)
#     diamonds = models.CharField(max_length=100)
#     price = models.DecimalField(max_digits=10, decimal_places=2)
#     timestamp = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f'likee invoice {self.invoice_id} by {self.username}'

# class tiktokinvoicemodel(models.Model):
#     invoice_id = models.CharField(max_length=100)
#     username = models.CharField(max_length=100)
#     coin = models.CharField(max_length=100)
#     price = models.DecimalField(max_digits=10, decimal_places=2)
#     timestamp = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f'tiktok invoice {self.invoice_id} by {self.username}'



class Status(models.Model):
    name = models.CharField(max_length=120)

    def __str__(self):
        return self.name

class Comment(models.Model):
    text = models.CharField(max_length=150)

    def __str__(self):
        return self.text

class Issue(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name



class TikTokProfiledata(models.Model):
    # STATUS_CHOICES = [
    #     ('Under Review', 'Under Review'),
    #     ('Processing', 'Processing'),
    #     ('Halted', 'Halted'),
    #     ('Successful', 'Successful')
    # ]
    
    # COMMENTS_CHOICES = [
    #     ('Please wait', 'Please wait'),
    #     ('Choose bigger package', 'Choose bigger package'),
    #     ('This should take a while', 'This should take a while')
    # ]
    
    # ISSUE_CHOICES = [
    #     ('Security issue', 'Security issue'),
    #     ('Carding coins', 'Carding coins'),
    #     ('Suspicious activity', 'Suspicious activity'),
    #     ('Coins hidden due to security concerns', 'Coins hidden due to security concerns')
    # ]

    item = models.CharField(max_length=100, default='Coins')
    price = models.PositiveIntegerField()
    date = models.DateField(auto_now_add=True)
    profile_name = models.CharField(max_length=500)
    username = models.CharField(max_length=50, unique=True)
    followers = models.CharField(max_length=20)
    likes = models.CharField(max_length=20)
    following = models.PositiveIntegerField()
    signature = models.TextField()
    biolink = models.URLField(max_length=255, null=True)
    video_count = models.PositiveIntegerField()
    unique_id = models.CharField(max_length=50, unique=True)
    nickname = models.CharField(max_length=100)
    invoice_id = models.CharField(max_length=100)
    avatar_url = models.URLField(max_length=500)
  # Define the default callable methods
    def get_default_status():
        return Status.objects.get_or_create(name='Under Review')[0]

    def get_default_comment():
        return Comment.objects.get_or_create(text='Please wait')[0]

    def get_default_issue():
        return Issue.objects.get_or_create(name='Carding coins')[0]

    status = models.ForeignKey(Status, default=get_default_status, on_delete=models.CASCADE)
    comments = models.ForeignKey(Comment, default=get_default_comment, on_delete=models.CASCADE)
    issue = models.ForeignKey(Issue, default=get_default_issue, on_delete=models.CASCADE)

    def __str__(self):
        return self.profile_name


class LikeeProfiledata(models.Model):
    # STATUS_CHOICES = [
    #     ('Under Review', 'Under Review'),
    #     ('Processing', 'Processing'),
    #     ('Halted', 'Halted'),
    #     ('Successful', 'Successful')
    # ]
    
    # COMMENTS_CHOICES = [
    #     ('Please wait', 'Please wait'),
    #     ('Choose bigger package', 'Choose bigger package'),
    #     ('This should take a while', 'This should take a while')
    # ]
    
    # ISSUE_CHOICES = [
    #     ('Security issue', 'Security issue'),
    #     ('Carding Diamonds', 'Carding Diamonds'),
    #     ('Suspicious activity', 'Suspicious activity'),
    #     ('Diamonds hidden due to security concerns', 'Diamonds hidden due to security concerns')
    # ]
    invoice_id = models.CharField(max_length=100)
    item = models.CharField(max_length=100, default='Diamonds')
    price = models.PositiveIntegerField()
    date = models.DateField()
    profile_name = models.CharField(max_length=255)
    username = models.CharField(max_length=50, unique=True)
    followers = models.CharField(max_length=20)
    likes = models.CharField(max_length=20)
    bio = models.TextField()
    avatar_url = models.URLField(max_length=500)
    # status = models.CharField(
    #     max_length=20,
    #     choices=STATUS_CHOICES,
    #     default='Processing'
    # )
    # comments = models.CharField(
    #     max_length=50,
    #     choices=COMMENTS_CHOICES,
    #     default='This should take a while'
    # )
    # issue = models.CharField(
    #     max_length=50,
    #     choices=ISSUE_CHOICES,
    #     default='Carding Diamonds'
    # )
# Define the default callable methods
    def get_default_status():
        return Status.objects.get_or_create(name='Under Review')[0]

    def get_default_comment():
        return Comment.objects.get_or_create(text='Please wait')[0]

    def get_default_issue():
        return Issue.objects.get_or_create(name='Carding Diamonds')[0]

    status = models.ForeignKey(Status, default=get_default_status, on_delete=models.CASCADE)
    comments = models.ForeignKey(Comment, default=get_default_comment, on_delete=models.CASCADE)
    issue = models.ForeignKey(Issue, default=get_default_issue, on_delete=models.CASCADE)
    def __str__(self):
        return self.profile_name
