import datetime
import random

import django
import matplotlib.pyplot as plt
from django.contrib import auth
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import render
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.dates import DateFormatter
from matplotlib.figure import Figure

from web.models import *
from web.models import result_test_runss
from django.db.models import Q


# Create your views here.

#首页
def login_action(request):

    if request.method == 'GET':
        return render(request, 'login.html')

    if request.method == 'POST':
        #寻找名称为'username'和'password'的POST 参数，而且如果参数没有提交，则返回一个空字符串
        username = request.POST.get('username','')
        password = request.POST.get('password','')
        print(username,password)
        if username == '' or password == '':
            return render(request,'Login.html',{'error':'账号或密码为空'})
        user = auth.authenticate(username = username, password = password)
        if user is not None:
            auth.login(request, user)
            response = HttpResponseRedirect('/index/')
            request.session['username'] = username
            return response

        else:
            return render(request,'Login.html',{'error':'用户名或密码错误'})




def index(request):
    result_list = result_test_runss.objects.all()
    username = request.session.get('username', '')

    paginator = Paginator(result_list, 10)
    page = request.GET.get('page')

    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        contacts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        contacts = paginator.page(paginator.num_pages)

    return render(request,'Index.html',{"user":username,"events":contacts})

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/login/")

def sreach_name(request):
    username = request.session.get('username', '')
    sreach_name = request.GET.get("name", "")
    # sreach_casesname = request.GET.get("casesname", "")
    sreach_name_bytes = sreach_name.encode(encoding="utf-8")
    # sreach_casesname_bytes = sreach_casesname.encode(encoding="utf-8")

    print(sreach_name_bytes)
    # event_list = result_test_runss.objects.filter(source_file__contains=sreach_name_bytes).filter(id__contains = sreach_casesname)
    event_list = result_test_runss.objects.filter(Q(source_file__contains=sreach_name_bytes)|Q(id__contains = sreach_name_bytes)|Q(started_at__startswith=sreach_name))
    # started_at__contains = sreach_casesname.encode(encoding="utf-8")
    return render(request, "Index.html", {"user": username, "events": event_list})

def del_data(request,aid):
    # print('article_id %s' % aid)
    result_data = result_test_runss.objects.get(id = aid)
    result_data.delete()
    return HttpResponseRedirect('/index/')

def columnar_analysic(request):

    result_data = result_test_runss.objects.all()

    return render(request,'columnar_analysic.html',{'result_data':result_data})

def sreach_name_result(request):
    username = request.session.get('username', '')
    sreach_name = request.GET.get("name", "")
    # sreach_casesname = request.GET.get("casesname","")

    sreach_name_bytes = sreach_name.encode(encoding="utf-8")
    # sreach_casesname_bytes = sreach_casesname.encode(encoding="utf-8")
    # print(sreach_name,sreach_casesname)
    # result_data = result_test_runss.objects.filter(source_file__contains=sreach_name_bytes).filter(id__contains = sreach_casesname)
    result_data = result_test_runss.objects.filter(Q(source_file__contains=sreach_name_bytes)|(Q(started_at__gte=sreach_name)))


    # print(result_data,)
    # if isinstance(result_data):
    #     result_data = result_data
    # else:
    #     result_data = result_test_runss.objects.filter(started_at__day=sreach_name_bytes)
    # result_data1 = result_test_runss.objects.filter(started_at__day=sreach_name_bytes)
    print(result_data)
    return render(request, "columnar_analysic.html", {"user": username, 'result_data':result_data})

def databasconn(request):
    return render(request,'database_connection.html')


def analysis(request):

    d ={
        '1.hldxhzj.duapp.com':9397,
        'www.xxx.com':777,
    }

    plt.figure(figsize=(8,6),dpi=80)
    cataegories = d.keys()
    data = d.values()
    return render(request, "Analysis.html",{'user':request.user,'cataegories':cataegories,'data':data})





def simple(request):

    fig=Figure()
    ax=fig.add_subplot(111)
    x=[]
    y=[]
    now=datetime.datetime.now()
    delta=datetime.timedelta(days=1)
    for i in range(10):
        x.append(now)
        now+=delta
        y.append(random.randint(0, 1000))
    ax.plot_date(x, y, '-')
    ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
    fig.autofmt_xdate()
    canvas=FigureCanvas(fig)
    response=django.http.HttpResponse(content_type='image/png')
    canvas.print_png(response)
    return render(request,'Analysis.html',canvas.print_png(response))


def show_result(request):
    """draw result image"""
    import matplotlib_util
    from Py3ForRfResultAnalysis.settings import MEDIA_ROOT

    # draw histogram
    n_groups = Question.objects.all().count()
    options = ('A', 'B', 'C', 'D')
    nums = []
    for option in options:
        num = []
        for tid in range(1, n_groups + 1):
            cnt = Result.objects.filter(t_id=tid, my_option=option).count()
            num.append(cnt)
        nums.append(num)
    histogram_path = MEDIA_ROOT + 'images\\results\\' + '0.png'
    print (histogram_path)
    try:
        matplotlib_util.draw_histogram(nums[0], nums[1], nums[2], nums[3],
                                      n_groups, histogram_path)
    except:    # handle all exception
        return render(request, 'result_image.html',
                      {'images': None})

    # draw pie chart
    for tid in range(1, n_groups+1):
        explode = [0.0, 0.0, 0.0, 0.0]
        answer_num = ord(Question.objects.get(t_id=tid).t_answer.upper()) - ord('A')
        explode[answer_num] = 0.1
        explode = tuple(explode)

        question_info = []
        for each in options:
            cnt = Result.objects.filter(t_id=tid, my_option=each).count()
            question_info.append(cnt)

        chart_path = MEDIA_ROOT + 'images\\results\\' + str(tid) + '.png'
        print (chart_path)
        try:
            matplotlib_util.draw_piechart(question_info, explode, chart_path)
        except:
            return render(request, 'result_image.html',
                          {'images': None})

    images = []
    for i in range(n_groups+1):
        images.append('/media/images/results/'+str(i)+'.png')
    return render(request, 'result_image.html', {'images': images})

