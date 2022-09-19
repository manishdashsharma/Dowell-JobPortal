from django.http import HttpResponse, JsonResponse 
from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt
from .dowellpopulationfunction import targeted_population
import json


@csrf_exempt
def home(request):
    return JsonResponse({"Manish":"Manish"})


def main(request):
    return render(request , 'main.html')


@csrf_exempt
def candidate_name(request):
  if request.method == 'POST':
    Time_period = request.POST.get('Timeperiod')
    response = targeted_population('hr_hiring','accounts_view',  ['application_details'],  Time_period )
    candidate=[]
    for i in response['normal']['data'][0]:
        candidate.append(i['application_details']['applicant'])
  return JsonResponse({"candidate":candidate})

@csrf_exempt
def task_report(request):
    if request.method == 'POST':
        candidate_name =request.POST['candidate_name']
        time_period = request.POST['time_period']
        response = targeted_population('hr_hiring','tasks',  ['task_details'], time_period)
        all_tasks = [data['task_details'] for data in response['normal']['data'][0]]
        def find_candidate_tasks(candidate, task_list):
            tasks = []
            for task in task_list:
                if task['user'] == candidate:
                    tasks.append(task)
            if len(tasks) != 0:
                return tasks

            return tasks
        candidate_task = find_candidate_tasks(candidate_name, all_tasks)
        return JsonResponse({"candidate_task":candidate_task})

@csrf_exempt
def timeperiod(request):
    timeperiod= ['custom' , 'last_1_day' , 'last_30_days' , 'last_90_days' , 'last_180_days' , 'last_1_year' , 'life_time']
    return JsonResponse({"time":timeperiod})


@csrf_exempt
def candidate_count(request):
  if request.method == 'POST':
    Time_period = request.POST.get('Timeperiod')
    response = targeted_population('hr_hiring','accounts_view',  ['application_details'],  Time_period )
    candidate=[]
    for i in response['normal']['data'][0]:
        candidate.append(i['application_details']['applicant'])
    total_candidate = len(candidate)
    print(total_candidate)
  return JsonResponse({"total_candidate":total_candidate})


@csrf_exempt
def Candidate_report(request):
    global total_pending_candidate
    if request.method == 'POST':
        Time_period = request.POST.get('Timeperiod')
        response = targeted_population('hr_hiring','candidate_view',  ['candidate_data'], Time_period)
        if response['normal']['is_error'] == True :
              return render(request, 'main.html',context={"timeperiod":timeperiod})
        else:
         candidate_detail = [data['candidate_data'] for data in response['normal']['data'][0]]
         def find__status(candidate_detail):
         
            Pending = []
            for candidate in candidate_detail:
                
                if candidate ['status'] == "Pending":
                          Pending.append(candidate )
                
         
            total_pending_candidate = len(Pending)
            data =[ total_pending_candidate]
           
            return data
        candidate_status = find__status(candidate_detail)
        print('candidate', candidate_status)
        return JsonResponse({"status":   candidate_status })
       


@csrf_exempt
def hr_report(request):
    if request.method == 'POST':
        Time_period = request.POST.get('Timeperiod')
        print(Time_period)
        response = targeted_population('hr_hiring','hr_view',  ['application_details'], Time_period)
        if response['normal']['is_error'] == True :
              return render(request, 'main.html',context={"timeperiod":timeperiod})
        else:
         Task_detail = [data['application_details'] for data in response['normal']['data'][0]]
        def find__status(task_detail):
            shortlisted = []
            selected  = []
           
            for task in task_detail:
                if task['status'] == "shortlisted":
                     shortlisted.append(task)
                elif task['status'] == "selected":
                     selected.append(task)
               
         
            total_shorlisted_candidate = len(shortlisted)
            total_selected_candidate = len(selected)  
            data =[total_shorlisted_candidate , total_selected_candidate]
           
            return data
        status = find__status(Task_detail)
        return JsonResponse({"status":  status})
    
    
    
@csrf_exempt
def Teamlead_report(request):
    global  team_lead_candidate
    if request.method == 'POST':
        Time_period = request.POST.get('Timeperiod')
        response = targeted_population('hr_hiring','teamlead_view',  ['full_name'], Time_period)
        if response['normal']['is_error'] == True :
              return render(request, 'main.html',context={"timeperiod":timeperiod})
        else:
         Teamlead_detail = [data['full_name'] for data in response['normal']['data'][0]]
        def find__status(teamlead_detail):
         
            teamlead_hire = []
            for teamlead in teamlead_detail:
                
                if teamlead['status'] == "teamlead_hire":
                          teamlead_hire.append(teamlead)
                
         
            team_lead_candidate = len( teamlead_hire )
            data =[ team_lead_candidate]
           
            return data
        status = find__status(Teamlead_detail)
        print('teamlead',status)
        return JsonResponse({"status":  status})
      

@csrf_exempt
def account_report(request):
    global total_hired_candidate
    if request.method == 'POST':
        Time_period = request.POST.get('Timeperiod')
        response = targeted_population('hr_hiring','accounts_view',  ['application_details'], Time_period)
        if response['normal']['is_error'] == True :
              return render(request, 'main.html',context={"timeperiod":timeperiod})
        else:
         account_detail = [data['application_details'] for data in response['normal']['data'][0]]
       
        def find__status(account_detail):
         
            hired = []
            for account in account_detail:
                
                if account['status'] == "hired":
                          hired.append(account)
                
         
            total_hired_candidate = len(hired) 
            data =[ total_hired_candidate]
           
            return data
        status = find__status(account_detail)
        print('Hired',status)
        return JsonResponse({"status":   status })
