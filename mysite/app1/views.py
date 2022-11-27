"""This Module Contain All The Views"""
# for loading html pages.
from django.shortcuts import render, redirect

# importing all the models database tables.
from .models import Applications, Work, WorkType, Images, ManyToManyRelation

# Used Django inbuilt User Model.
from django.contrib.auth.models import User

# Used Login logout authenticate of django.
from django.contrib.auth import authenticate, login, logout

# login_required decorator.
from django.contrib.auth.decorators import login_required

# for json
from django.template.loader import render_to_string
from django.http import JsonResponse
# to convert django object into json.
from django.core.serializers import serialize

from googletrans import Translator
from django.views.generic import ListView
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
import requests
from django.db.models import Q


# Create your views here.

def update_address(request):
    """Update Address Of User"""
    if request.method == "POST":
        state = request.POST["state"]
        district = request.POST["district"]
        print(state)
        var1 = Applications.objects.get(
            user=request.user.id
        )  # getting application from user
        var1.users_state = state
        var1.users_dist = district
        var1.save()
        return redirect("profile")


def register(request):
    """Registration View"""
    if request.method == "POST":
        a = request.POST["username"]
        b = request.POST["password"]
        c = request.POST["type"]
        d = request.POST["FirstName"]
        e = request.POST["contactno"]
        f = request.POST["LastName"]

        p = User.objects.create_user(
            username=a, first_name=d, password=b, last_name=f
        )
        p.save()
        m = User.objects.get(username=a)  # retrive same user object.
        # creating Application object.
        obj = Applications(user=m, contact_no=e, type=c)
        obj.save()  # User and Application is having one to one relation.
        return redirect("login")  # data valid then go to login page.
    return render(request, "app1/register.html")  # else return same page.


def login_page(request):
    """Login Page View"""
    if request.method == "POST":
        username = request.POST["username"]
        passw = request.POST["password"]
        user = authenticate(
            request, username=username, password=passw
        )  # check is user Exist
        if user is not None:
            login(request, user)  # send login request to database.
            return redirect("home")  # this will call home fun.
        else:
            return render(request, "app1/login.html",
                          {"WA": "Incorrect Credentials"})
    return render(request, "app1/login.html")  # if method is not post.


@login_required(login_url="login")
def home(request):
    """Searching Type Of Work Ajax Search."""
    ctx = {}
    url_parameter = request.GET.get("q")  # get the parameter which is send
    if url_parameter:
        # icontains search filter will be case insensitive.
        works = WorkType.objects.filter(TypeOfWork__icontains=url_parameter)
    else:
        works = ""
    ctx["works"] = works
    is_ajax_request = request.headers.get(
        "x-requested-with") == "XMLHttpRequest"
    temp = len(works)
    if is_ajax_request:
        html = render_to_string(
            template_name="app1/partial.html",
            context={
                "works": works,
                "flag": temp})
        data_dict = {"html_from_view": html}
        return JsonResponse(data=data_dict, safe=False)

    obj = WorkType.objects.all()  # fetch all the WorkType objects.
    obj1 = Translator()
    for ele in obj:
        out = obj1.translate(ele.TypeOfWork, dest="hi")
        print(out)
    mydict = {}
    for item in obj:
        out = obj1.translate(item.TypeOfWork, dest="hi")
        mydict[item] = out.text
    return render(request, "app1/home.html",
                  {"workss": mydict})  # passing list to html


@login_required(login_url="login")
def work(request, item_id):
    """location on the basis of ip of user"""
    ip = requests.get("https://api64.ipify.org?format=json")  # to get ip.
    # since it is in json convert it to python dict.
    ip_data = json.loads(ip.text)
    req = requests.get(
        "http://ip-api.com/json/" + ip_data["ip"]
    )  # to get location infor on the basis of ip.
    location_data_one = req.text
    location_data = json.loads(location_data_one)  # convert json to python.
    # if more than 1 job available then shows according to state, city, district...
    # else showing global result.
    cri1 = Q(work_id=item_id)
    cri2 = Q(approved=True)
    cri3 = Q(city__icontains=location_data["city"])
    # check if status is approved.
    a = Work.objects.all().filter((cri1 & cri2) & cri3)
    if len(a) <= 0:
        a = Work.objects.all().filter(cri1, cri2)

    status = Applications.objects.get(
        user=request.user
    )  # to check user is job giver or job seeker.
    flag = True
    if status.type == "JobSeeker":
        flag = False
    return render(request, "app1/description.html",
                  {"work": a, "id": item_id, "flag": flag})


@login_required(login_url="login")
def worksearch(request):
    """searching on the basis of city"""
    url_parameter = request.GET.get("q")  # data from front end  by ajax call.
    url_parameter2 = request.GET.get("id")
    # filter data
    if url_parameter == "" or url_parameter:
        var = Work.objects.filter(
            city__icontains=url_parameter, work_id=url_parameter2
        )  # using case insensitve filter to search object
    else:
        var = ""
    is_ajax_request = request.headers.get(
        "x-requested-with") == "XMLHttpRequest"
    if is_ajax_request:

        html = render_to_string(  # pass ajax response.
            template_name="app1/partial2.html",
            context={"var": var, "id": url_parameter2},
        )
        # update parital2 html page only.
        data_dict = {"html_from_view": html}
        return JsonResponse(data=data_dict, safe=False)


@login_required(login_url="login")
def create(request):
    """Create worktype is there need to check if work is valid or not"""
    a = WorkType(TypeOfWork=request.POST["worktype"])
    a.save()
    return redirect("home")


@login_required(login_url="login")
def addWork(request, pk):
    """Add Work Functionality Support."""
    if request.method == "GET":
        return render(request, "app1/addwork.html", {"id": pk})
    else:
        # validation remaining add only if not exist.
        var1 = request.POST["descrip"]
        var2 = request.POST["wages"]
        var3 = request.POST["hours"]
        var4 = request.POST["Location"]
        var5 = request.POST["state"]
        var6 = request.POST["district"]
        temp = WorkType.objects.get(pk=pk)  # one to many relation.
        # Create Object Of Work.
        obj = Work(
            work_id=temp,
            Hours=var3,
            city=var4,
            Wages=var2,
            Description=var1,
            state=var5,
            district=var6,
        )
        obj.save()
        return redirect(
            "work", pk, permanent=True
        )  # permanent function is to pass args.


@login_required(login_url="login")
def logout_view(request):
    """Logout View"""
    if request.user.is_authenticated:
        logout(request)
        return render(request, "app1/login.html")
    else:
        return redirect("login")


@login_required(login_url="login")
def profile(request):
    """Profile Page"""
    uservar = User.objects.get(id=request.user.id)
    var1 = Applications.objects.get(
        user=request.user.id
    )
    state = var1.users_state
    dist = var1.users_dist
    var2 = ManyToManyRelation.objects.filter(
        userid=var1
    )

    newlist = []
    # passing work object for displaying just use fields of work.
    for ele in var2:
        newlist.append(Work.objects.get(pk=ele.workid.id))

    # for that User.
    obj1 = Applications.objects.all().filter(user=request.user)
    if request.method == "POST":
        images = request.FILES.getlist("imgs")  # for multiple images.
        for image1 in images:
            # create object for each  image .
            obj = Images(connect=obj1[0], image=image1).save()
        myimages = Images.objects.all().filter(connect=obj1[0])
        l1 = []
        # fetch all images and pass as list.
        for image1 in myimages:
            l1.append(image1.image)
        return render(
            request,
            "app1/profile.html",
            {
                "obj": obj1,
                "path": l1,
                "fname": uservar.first_name,
                "lname": uservar.last_name,
                "state": state,
                "district": dist,
            },
        )

    myimages = Images.objects.all().filter(connect=obj1[0])
    l1 = []
    for image1 in myimages:
        l1.append(image1.image)
    return render(
        request,
        "app1/profile.html",
        {
            "obj": obj1,
            "path": l1,
            "newlist": newlist,
            "fname": uservar.first_name,
            "lname": uservar.last_name,
            "state": state,
            "district": dist,
        },
    )


@csrf_exempt
@login_required(login_url="login")
def apply(request, pk, item_id):
    """Make links to show who applied for which job"""
    if request.method == "POST":
        user_id = request.user
        # creating required instances using id/ primary key.
        obj1 = Applications.objects.get(user=user_id)
        print(user_id)
        print(obj1.type)
        a = Work.objects.all().filter(
            work_id=item_id, approved=True
        )  # check if status is approved.

        if obj1.type == "JobSeeker":

            obj2 = Work.objects.get(pk=pk)

            # establish relation.
            obj = ManyToManyRelation(userid=obj1, workid=obj2)
            obj.save()
            # success message.
            return render(
                request,
                "app1/description.html",
                {"work": a, "id": item_id, "message": "Applied Successfully"},
            )
        else:
            messages.success(
                request, "You Cannot apply since you are JobGiver")
            return render(request, "app1/description.html",
                          {"work": a, "id": item_id})
            # render page with jobgiver status cant apply.

    return redirect("work", item_id, permanent=True)  # render the same page.
