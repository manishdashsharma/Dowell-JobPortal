from django.urls import path
from report.views import home , candidate_count , main ,timeperiod ,candidate_name ,task_report
from report.views import  hr_report, Teamlead_report, Candidate_report,account_report 

urlpatterns =[
    path('home/',home, name= 'home'),
    path('timeperiod/',timeperiod, name= 'timeperiod'),
    path('main/',main, name= 'mainpage'),

    path('hr_report/',hr_report, name= 'hr_report'),
    path('Teamlead_report/',Teamlead_report, name= 'Teamlead_report'),
    path('Candidate_report/',Candidate_report, name= 'Candidate_report'),
    path('account_report/',account_report, name= 'account_report'),
    path('candidate_count/',candidate_count,name='candidate_count'),

    path('candidate_name/',candidate_name,name='candidate_name'),
    path('task_report/',task_report,name='task_report')


]