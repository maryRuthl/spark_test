from django.shortcuts import render,HttpResponse,redirect

# Create your views here.
from app01.models import User_Info
def login(request):
    if request.method =="POST":
        user = request.POST.get('username')
        pwd = request.POST.get('pwd')

        user = User_Info.objects.filter(user=user,pwd=pwd).first()
        if user:
            response= HttpResponse('登录成功')
            response.set_cookie('is_login',True,max_age=100)
            response.set_cookie('username',user.user,path='/index/')
            return response
    return render(request,'login.html')


def index(request):
    print(request.COOKIES)
    is_login = request.COOKIES.get('is_login')
    if is_login:
        username = request.COOKIES.get('username')

        import datetime
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # 先取出时间
        last_time = request.COOKIES.get('last_visit_time','')  # 第一次取出来是空
        response = render(request,'index.html',{"username":username,"last_time":last_time})
        response.set_cookie('last_visit_time',now)   # 这里才记录这次时间下次访问就会有上次访问的时间
        return response
    else:
        return redirect('/login/')

def login_session(request):
    if request.method == "POST":
        user = request.POST.get('username')
        pwd = request.POST.get('pwd')
        user = User_Info.objects.filter(user=user,pwd=pwd).first()

        if user:
            # 登录成功
            import datetime
            now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            request.session['is_login'] = True
            request.session['username'] = user.user
            # 键就是sessionid,值就是生成的随机字符串
            # sessionid      kx84zzgoqnumdrncxifym6r0y9mdz3pu

            request.session['last_visit_time'] = now
            return HttpResponse("登录成功")

    return render(request,'login.html')

def index_session(request):
    is_login = request.session.get('is_login')
    if not is_login:
        return redirect('/login_session/')

    username = request.session.get('username')
    last_time = request.session.get('last_visit_time')
    return render(request,'index.html',{"username":username,"last_time":last_time})

def login_out(request):

    # del request.session['is_login']
    # 一次性删除整条记录
    request.session.flush()
    """
    执行request.session.flush()会做3个步骤
        1. 读到浏览器发来的请求中带的sessionid    random_str = request.COOKIE.get('sessionid') 
        2. 去数据库过滤这条sessionid的值(一个随机字符串)与session_key字段中的值   django_session.object.filter(session_key=random_str) 
        3. 删除浏览器Cookie的值    response.delete_cookie('session')
    """

    return redirect('/login_session/')