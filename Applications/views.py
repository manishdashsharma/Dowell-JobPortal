from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q
from datetime import datetime
from .dowell_function import save_candidate, save_task, save_application, save_to_teamleadview
from .dowell_function import update_task_data
import json

from .models import JobApplication, Job, Meeting, Project, RehiredCandidate, RejectedCandidate, Team, Alert
from .models import Task
from .serializers import JobApplicationSerializer, JobSerializer, JobApplicationSerializer
from .serializers import MeetingSerializer, ProjectSerializer, RehiredCandidateSerializer
from .serializers import TaskSerializer
#from accounts.serializers import UserSerializer
from .serializers import RejectedCandidateSerializer, TeamSerializer, AlertSerializer
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import redirect
import requests


def Dowell_Login(username, password):
    url = "http://100014.pythonanywhere.com/api/login/"
    userurl = "http://100014.pythonanywhere.com/api/user/"
    payload = {
        'username': username,
        'password': password
    }
    with requests.Session() as s:
        p = s.post(url, data=payload)
        if "Username" in p.text:
            return p.text
        else:
            user = s.get(userurl)
            return user.text


# r = Dowell_Login()


@api_view(['GET'])
# @permission_classes((permissions.IsAuthenticated,))
# def get_user(request):
#     user = request.user
#     serializer = UserSerializer(user, many=False)
#     return Response(serializer.data)
@api_view(['GET'])
def application_view(request):
    applications = JobApplication.objects.all()
    serializer = JobApplicationSerializer(applications, many=True)
    return Response(serializer.data)


@api_view(['GET'])
# @permission_classes((permissions.AllowAny,))
def get_jobs(request):
    jobs = Job.objects.all()
    serializer = JobSerializer(jobs, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_applications(request):
    applications = JobApplication.objects.all()
    serializer = JobApplicationSerializer(applications, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_my_applications(request):
    user = request.user
    if user is None:
        return Response({"message": "You do not have the necessary Privileges! Must be logged in"})
    applications = JobApplication.objects.filter(applicant=user)
    if applications.len() < 1:
        return Response({"message": "You do not have any applications Yet!"})
    serializer = JobApplicationSerializer(applications, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def add_application(request):
    serializer = JobApplicationSerializer(data=request.data)
    date_applied = datetime.now()
    applicant = request.data["applicant"]
    job_id = request.data["job"]
    job_applied = Job.objects.get(id=job_id)
    title = request.data["title"]
    description = request.data["description"]
    remarks = f"This is the initial meeting for {title} and its all about {description}"
    new_meeting = Meeting(date_applied=date_applied, applicant=applicant,
                          job_applied=job_applied, remarks=remarks)
    new_meeting.save()
    if serializer.is_valid():
        serializer.save()
        try:
            save_candidate(serializer.data)
        except:
            print("Candidate data not saved to MongoDB Database")
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def add_new_job(request):
    serializer = JobSerializer(data=request.data)
    print(serializer)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST', 'GET'])
def candidateview(request):
    print(type(request))
    print(dir(request))
    print(request)
    return Response({"message": "Welcome to candidate view page!"})
    # give access to all links that are related to a candidate


@api_view(['POST', 'GET'])
def account_view(request):
    return Response({"message": "Welcome to the Accounts page!"})


@api_view(['POST', 'GET'])
def team_lead_view(request):
    return Response({"message": "Welcome to the Team Lead Page!"})


@api_view(['POST', 'GET'])
def hrview(request):
    return Response({"message": "Welcome to HR View. You can now create new jobs and review applications"})


@api_view(['POST'])
def update_job(request, pk):
    job = Job.objects.get(id=pk)
    serializer = JobSerializer(instance=job, data=request.data)
    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(['DELETE'])
def delete_job(request, pk):
    job = Job.objects.get(id=pk)
    job.delete()
    return Response("Job successfully deleted")


test_strings = ["Hired", "Hire", "Select",
                "Selected", "shortlisted", "teamlead_hire"]


@api_view(['POST'])
def update_application(request, pk):
    job_application = JobApplication.objects.get(id=pk)
    status = request.data["status"]
    applicant = job_application.applicant
    job_applied = job_application.job
    #remarks = job_application.hr_remarks
    title = f'{job_applied}: Job application update'
    message = f"Your application for the position {job_applied} was {status} and interview scheduled."
    if any(word.lower() in status.lower() for word in test_strings):
        new_alert = Alert(title=title, recipient=applicant,
                          typeof=status, message=message)
        new_alert.save()
    else:
        pass
    serializer = JobApplicationSerializer(
        instance=job_application, data=request.data)
    if serializer.is_valid():
        serializer.save()
        if status.lower() == "shortlisted":
            document_name = "hr_view"
            member_id = "4646111"
            save_application(document_name, member_id, serializer.data)
        elif status.lower() == "selected":
            document_name = "hr_view"
            member_id = "4646111"
            save_application(document_name, member_id, serializer.data)
        elif status.lower() == "teamlead_hire":
            document_name = "teamelead_view"
            member_id = "1000552"
            #save_application(document_name, member_id, serializer.data)
            save_to_teamleadview(serializer.data)
        elif status.lower() == "hired":
            document_name = "accounts_view"
            member_id = "1000551"
            save_application(document_name, member_id, serializer.data)
        else:
            print("Application update and its details not saved to MongoDB Database")
    else:
        return Response("Job application updating was not successfull. Try look for possible errors! Ensure you have included the relevant job/job id")

    return Response(serializer.data)


@api_view(['DELETE'])
def delete_application(request, pk):
    job = JobApplication.objects.get(id=pk)
    job.delete()
    return Response("Application successfully deleted")


@api_view(['GET', 'POST'])
def meeting(request):
    if request.method == 'GET':
        meetings = Meeting.objects.all()
        serializer = MeetingSerializer(meetings, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = MeetingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def project(request):
    if request.method == 'GET':
        projects = Project.objects.all()
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def alerts(request):
    if request.method == 'GET':
        alerts = Alert.objects.all()
        serializer = AlertSerializer(alerts, many=True)
        return Response(serializer.data)

    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def rehired_candidate(request):
    if request.method == 'GET':
        rehired_candidates = RehiredCandidate.objects.all()
        serializer = RehiredCandidateSerializer(rehired_candidates, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = RehiredCandidateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def rejected_candidate(request):
    if request.method == 'GET':
        rejected_candidates = RejectedCandidate.objects.all()
        serializer = RejectedCandidateSerializer(
            rejected_candidates, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = RejectedCandidateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def teams(request):
    if request.method == 'GET':
        teams = Team.objects.all()
        serializer = TeamSerializer(
            teams, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = TeamSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_tasks(request):
    tasks = Task.objects.all()
    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def add_new_task(request):
    serializer = TaskSerializer(data=request.data)
    if serializer.is_valid():
        mongo_response = save_task(serializer.data)
    else:
        print("Task details not saved to MongoDB Database")
    request.data["mongo_id"] = mongo_response
    refined_serializer = TaskSerializer(data=request.data)
    if refined_serializer.is_valid():
        refined_serializer.save()
        return Response(refined_serializer.data, status=status.HTTP_201_CREATED)

    return Response(refined_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST', 'PUT'])
def update_task(request, pk):
    try:
        task = Task.objects.get(id=pk)
        serializer = TaskSerializer(instance=task, data=request.data)
    except:
        return Response({
            "Error message": f"There is no task with id {pk}!"
        },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    if serializer.is_valid():
        try:
            serializer.save()
            task_object = json.dumps(serializer.validated_data)
            update_task_data(task_id=task.mongo_id, task_object=task_object)
            print("Task updated successfully both locally and in MongoDB")
        except:
            return Response("Task update was not successful. Try look for possible errors!")
    return Response(serializer.data)


@api_view(['DELETE'])
def delete_task(request, pk):
    task = Task.objects.get(id=pk)
    task.delete()
    return Response("Task deleted successfully!")


@api_view(['POST'])
def Jobs_list_Search(request):
    # receives a search term assigned q and should be a post request
    q = request.GET.get('q')
    if request.GET.get('q') == None:
        q = ''
    jobs = Job.objects.filter(  # search functionality, have any of the below
        Q(title__icontains=q) |
        Q(skills__icontains=q) |
        Q(description__icontains=q) |
        Q(is_active__icontains=q)
    )

    if jobs is not None:
        serializer = JobSerializer(
            jobs, many=True)
        return Response(serializer.data)
    else:
        pass


@api_view(['POST'])
def Jobs_application_list_Search(request):
    # receives a search term assigned q and should be a post request
    q = request.GET.get('q')
    if request.GET.get('q') == None:
        q = ''
    jobs = Job.objects.filter(  # search functionality, have any of the below
        Q(job__title__icontains=q) |
        Q(applicant__username__icontains=q) |
        Q(status__icontains=q)
    )

    if jobs is not None:
        serializer = JobSerializer(
            jobs, many=True)
        return Response(serializer.data)
    else:
        pass
