# for loading html pages.
from django.shortcuts import render, redirect
#importing all the models database tables.
from .models import Applications, Work, WorkType, Images, ManyToManyRelation
#Used Django inbuilt User Model.
from django.contrib.auth.models import User
#Used Login logout authenticate of django.
from django.contrib.auth import authenticate, login, logout
# login_required decorator.
from django.contrib.auth.decorators import login_required
#for json

from django.template.loader import render_to_string
from django.http import JsonResponse
from django.core.serializers import serialize # to convert django object into json.

from googletrans import Translator
from django.views.generic import ListView
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages

# Create your views here.

def update_address(request):
    address = request.POST["address"]
    print(address)

#registration view.
def register(request):
    if request.method == "POST":
        #get data from form validation remaining.
        a = request.POST["username"]
        b = request.POST["password"]
        c = request.POST["type"]
        d = request.POST["FirstName"]
        e = request.POST["contactno"]
        f = request.POST["LastName"]

        p = User.objects.create_user(username=a, first_name=d, password=b, last_name=f)  #create User object first then
        p.save()    # making User object.

        m = User.objects.get(username=a)    #retrive same user object.

        obj = Applications(user=m, contact_no=e, type=c)    #creating Application object.
        obj.save() #User and Application is having one to one relation.
        #validations
        return redirect("login")    #data valid then go to login page.
    return render(request, 'app1/register.html')    #else return same page.


#login view
def LoginPage(request):
    if request.method == "POST":

        username = request.POST["username"]
        passw = request.POST["password"]

        user = authenticate(request, username=username, password=passw) # check is user Exist
        print(user)
        if user is not None:
            login(request, user)    #send login request to database.
            return redirect('home')  # this will call home fun.
        else:
            return render(request, 'app1/login.html', {"WA" : "Incorrect Credentials"})
    return render(request, 'app1/login.html') # if method is not post.


# searching type of work ajax search.
@login_required(login_url='login')
def home(request):
    ctx = {}
    url_parameter = request.GET.get('q')  # get the parameter which is send

    if url_parameter:
        # icontains search filter will be case insensitive.
        works = WorkType.objects.filter(TypeOfWork__icontains=url_parameter)
    else:
        works = ""

    ctx["works"] = works
    is_ajax_request = request.headers.get("x-requested-with") == "XMLHttpRequest"
    print(works)
    if is_ajax_request:
        html = render_to_string(
            template_name='app1/partial.html',
            context={"works": works}
        )

        data_dict = {"html_from_view": html}
        

        return JsonResponse(data=data_dict, safe=False)

    l1 = []
    obj = WorkType.objects.all() #fetch all the WorkType objects.
    # translation ka badme dekh lena.

    obj1 = Translator()
    out = obj1.translate("How are you", dest="hi")

    for item in obj:
        l1.append(item)
    print("no ajax")
    return render(request, "app1/home.html", {"workss" : l1}) #passing list to html


@login_required(login_url='login')
def work(request, item_id):
    a = Work.objects.all().filter(work_id=item_id, approved=True) # check if status is approved.
    status = Applications.objects.get(user=request.user)    # to check user is job giver or job seeker.
    print(status.type)
    flag = True
    if status.type == 'JobSeeker':
        flag = False
    return render(request, "app1/description.html", {"work" : a, 'id' : item_id, "flag":flag})


# searching on the basis of city
def worksearch(request):
    ctx = {}
    url_parameter = request.GET.get('q')     # data from front end  by ajax call.
    url_parameter2 = request.GET.get('id')
    print(url_parameter)
    print(url_parameter2)

    # filter data
    if url_parameter == '' or url_parameter:
        var = Work.objects.filter(city__icontains=url_parameter, work_id=url_parameter2)     # using case insensitve filter to search object
    else:
        var = ''
    print(var)
    # newlist = []
    # for ele in var:
    #     newlist.append(ele)
    is_ajax_request = request.headers.get("x-requested-with") == "XMLHttpRequest"
    if is_ajax_request:

        html = render_to_string(    # pass ajax response.
            template_name='app1/partial2.html',
            context={"var": var, "id" :url_parameter2}
        )
        # only partial2 html wala page update karna hai .

        data_dict = {"html_from_view": html}
        return JsonResponse(data=data_dict, safe=False)


# create worktype is there need to check if work is valid or not?
def create(request):
    a = WorkType(TypeOfWork=request.POST["worktype"])
    a.save()
    return redirect('home')


def addWork(request, pk):
    if request.method == "GET":
        return  render(request, "app1/addwork.html", {"id" : pk})
    else:
        #validation remaining add only if not exist.
        var1 = request.POST["descrip"]
        var2 = request.POST["wages"]
        var3 = request.POST["hours"]
        var4 = request.POST["Location"]
        temp = WorkType.objects.get(pk=pk) # one to many relation.
        # Create Object Of Work.
        obj = Work(work_id=temp, Hours=var3, city=var4, Wages=var2,Description=var1)
        obj.save()

        return redirect('work', pk, permanent=True) # permanent function is to pass args.


@login_required(login_url='login')
def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        return render(request, "app1/login.html")
    else:
        return redirect('login')


# work remaining seprate out jobgiver and jobseeker page. refer apply view.
@login_required(login_url='login')
def profile(request):
    uservar = User.objects.get(id=request.user.id)
    print(uservar.first_name)
    # print(Applications.objects.get(user=request.user.id))
    # works applied
    var1 = Applications.objects.get(user=request.user.id) # getting application from user
    var2 = ManyToManyRelation.objects.filter(userid=var1)   # then filtering out that particular user jobs applied.

    newlist = []
    # passing work object for displaying just use fields of work.
    for ele in var2:
        newlist.append(Work.objects.get(pk=ele.workid.id))


    obj1 = Applications.objects.all().filter(user=request.user) # for that User.
    if request.method == "POST":
        images = request.FILES.getlist("imgs") # for multiple images.
        for image1 in images:
            #create object for each  image .
            obj = Images(connect=obj1[0], image=image1).save()
        myimages = Images.objects.all().filter(connect=obj1[0])
        l1 = []
        #fetch all images and pass as list.
        for image1 in myimages:
            l1.append(image1.image)
        return render(request, "app1/profile.html", {"obj": obj1, "path": l1, "fname" : uservar.first_name, "lname":uservar.last_name})

    myimages = Images.objects.all().filter(connect=obj1[0])
    l1 = []
    for image1 in myimages:
        l1.append(image1.image)
    return render(request, "app1/profile.html", {"obj": obj1, "path": l1, "newlist":newlist,"fname" : uservar.first_name, "lname":uservar.last_name})


class InfoListView(ListView):
    model = WorkType
    template_name = "app1/sear.html"

    def get_context_data(self, **kwargs):
        print("deasdsa")
        context = super().get_context_data(**kwargs)
        # creates json object and pass to javascript.
        context["qs_json"] = json.dumps(list(WorkType.objects.values()))
        return context

@csrf_exempt
def apply(request, pk, item_id):
    # make links to show who applied for which job.
    if request.method == "POST":

        user_id = request.user
        # creating required instances using id/ primary key.
        obj1 =  Applications.objects.get(user=user_id)
        print(user_id)
        print(obj1.type)
        a = Work.objects.all().filter(work_id=item_id, approved=True)  # check if status is approved.

        if obj1.type == 'JobSeeker':

            obj2 = Work.objects.get(pk=pk)

            obj = ManyToManyRelation(userid=obj1, workid=obj2)  # establish relation.
            obj.save()
            # success message.
            return render(request, "app1/description.html", {"work": a, 'id': item_id, 'message':'Applied Successfully'})
        else:
            messages.success(request, 'You Cannot apply since you are JobGiver')
            return render(request, "app1/description.html", {"work": a, 'id': item_id})
            # render page with jobgiver status cant apply.

    return redirect('work', item_id, permanent=True)    # render the same page.


#1 django.views.generic import ListView
#2 from .models import tablename
#3 create class InfoListView(ListView):

# new search strategy
#implemented in home
# def search1(request):
#     ctx = {}
#     url_parameter = request.GET.get('q')    # get the parameter which is send
#
#     if url_parameter:
#         # icontains search filter will be case insensitive.
#         works = WorkType.objects.filter(TypeOfWork__icontains=url_parameter)
#     else:
#         works = WorkType.objects.all()
#
#     ctx["works"] = works
#     print(ctx)
#     is_ajax_request = request.headers.get("x-requested-with")=="XMLHttpRequest"
#     print(is_ajax_request)
#     if is_ajax_request:
#         html = render_to_string(
#             template_name='app1/partial.html',
#             context={"works":works}
#         )
#         print(html)
#
#         data_dict = {"html_from_view":html}
#
#         return JsonResponse(data=data_dict, safe=False)
#     print("ajax")
#
#     return render(request, "app1/search1.html", context=ctx)
