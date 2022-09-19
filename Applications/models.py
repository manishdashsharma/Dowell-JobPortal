from django.db import models
#from accounts.models import User
from django.contrib.auth import get_user_model
#User = get_user_model()


class Project(models.Model):
    project_name = models.CharField(max_length=100, null=False)
    project_leader = models.CharField(max_length=100, null=False)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.project_name}-{self.project_leader}'


class Job(models.Model):
    title = models.CharField(max_length=100, null=False)
    description = models.TextField(null=False)
    skills = models.CharField(max_length=500, null=False, default="None")
    is_active = models.BooleanField(default=False)
    TYPECHOICES = (
        ('Freelancer', 'Freelancer'),
        ('Employee', 'Employee'),
        ('Internship', 'Internship'),
        ('Research Associate', 'Research Associate'),
    )
    typeof = models.CharField(
        max_length=100, choices=TYPECHOICES, default="Freelance")
    time_period = models.CharField(max_length=100, null="False")
    general_terms = models.JSONField(null=True)
    Technical_Specifications = models.JSONField(null=True)
    Payment_terms = models.JSONField(null=True)
    workflow = models.JSONField(null=True)
    others = models.JSONField(null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class JobApplication(models.Model):
    applicant = models.CharField(max_length=100, null=False)
    job = models.ForeignKey(Job, on_delete=models.CASCADE, null=False)
    feedBack = models.TextField(null=True)
    freelancePlatform = models.CharField(max_length=132, null=True)
    freelancePlatformUrl = models.URLField(null=True)
    country = models.CharField(max_length=132, null=True)
    hr_remarks = models.CharField(max_length=500, null=True)
    status = models.CharField(max_length=132, null=True, default="Pending")
    others = models.JSONField(null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Job Applications'

    def __str__(self):
        return f'{self.job}-{self.applicant}'


class Meeting(models.Model):
    date_applied = models.DateTimeField()
    applicant = models.CharField(max_length=100, null=False)
    #interviewer = models.CharField(max_length=100, null=False)
    job_applied = models.ForeignKey(Job, on_delete=models.CASCADE)
    remarks = models.CharField(max_length=200)
    status = models.CharField(max_length=50, default="Pending")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.applicant}-{self.job_applied}'


class FreelancersAndInterns(models.Model):

    freelancer = models.CharField(max_length=100, null=False)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    hr_remarks = models.CharField(max_length=500, null=True)
    tl_remarks = models.CharField(max_length=500, null=True)
    CHOICES = (
        ('Rehire', 'Rehire'),
        ('Reject', 'Reject'),
    )
    status = models.CharField(max_length=70, choices=CHOICES, default="Rehire")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.freelancer.username}-{self.project}'

    class Meta:
        verbose_name_plural = 'Freelancers And Interns'


class RehiredCandidate(models.Model):
    freelancer = models.CharField(max_length=100, null=False)
    job_applied = models.ForeignKey(Job, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    tl_remarks = models.CharField(max_length=500, null=True)
    CHOICES = (
        ('Rehire', 'Rehire'),
        ('Reject', 'Reject'),
        ('Pay', 'Pay'),
    )
    teamlead_options = models.CharField(
        max_length=70, choices=CHOICES, default="Rehire")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.freelancer.freelancer}-{self.project}'

    class Meta:
        verbose_name_plural = 'Rehired Freelancers'


class RejectedCandidate(models.Model):
    freelancer = models.CharField(max_length=100, null=False)
    job_applied = models.ForeignKey(Job, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    tl_remarks = models.CharField(max_length=500, null=True)
    CHOICES = (
        ('Rehire', 'Rehire'),
        ('Reject', 'Reject'),
        ('Pay', 'Pay'),
    )
    teamlead_options = models.CharField(
        max_length=70, choices=CHOICES, default="Reject")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.freelancer.freelancer}-{self.project}'

    class Meta:
        verbose_name_plural = 'Rejected Freelancers'
# after selection


class Team(models.Model):
    name = models.CharField(max_length=300)
    team_lead = models.CharField(max_length=100, null=False)
    github_url = models.URLField()
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="project_teams")
    discord_link = models.URLField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name}-{self.team_lead}-{self.project}'


class Alert(models.Model):
    title = models.CharField(max_length=300)
    recipient = models.CharField(max_length=300)
    CHOICES = (
        ('Success', 'Success'),
        ('Failure', 'Failure'),
        ('Pending', 'Pending'),
    )
    typeof = models.CharField(
        max_length=300, choices=CHOICES, default="Pending")
    message = models.CharField(max_length=500)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name}-{self.recipient}-{self.typeof}'


class Task(models.Model):
    mongo_id = models.CharField(max_length=256, null=True)
    user = models.CharField(max_length=256, null=False)
    title = models.CharField(max_length=300, null=False)
    description = models.CharField(max_length=2048, null=True)
    STATUS_CHOICES = (
        ('Complete', 'Complete'),
        ('Incomplete', 'Incomplete'),
        ('Inprogress', 'Inprogress'),
    )
    status = models.CharField(
        max_length=24, choices=STATUS_CHOICES, default='Incomplete', null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
