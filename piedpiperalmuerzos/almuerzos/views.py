from django.shortcuts import render, render_to_response, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth
from django.template.context_processors import csrf
from django.contrib.auth.decorators import login_required
from .forms import *
from django.urls import reverse
from django.http import JsonResponse


def index(request):
    user = request.user
    activo = False
    if not user.is_anonymous() and user.userType.id in [1,2]:
        v = Vendedor.objects.get(user_id=user.id)
        try:
             p = Productos.objects.get(vendedor_id=v.id)
        except:
            p = []

        if user.userType.id == 2:
            c = MovilProfile.objects.get(vendedor_id=v.id)
            activo = c.activo
            return render_to_response('almuerzos/vendedor_perfil.html', {'user' : user, 'vendedor' : v, 'activo' : activo, 'productos' : p})
        if user.userType.id == 1:
            return render_to_response('almuerzos/vendedor_perfil.html', {'user': user, 'vendedor' : v, 'activo': activo, 'productos' : p})
    return render_to_response('almuerzos/index.html', {'user' : user, 'activo' : activo })


def base(request):

    return render(request, 'almuerzos/base.html')


def gestion_productos(request):
    return render(request, 'almuerzos/gestion_productos.html')


def vendedor_perfil(request, vendedor_id = 1):
    user = request.user
    activo = False
    try:
        p = Productos.objects.get(vendedor_id=v.id)
    except:
        p = []
    v = Vendedor.objects.get(id=vendedor_id)
    c = MovilProfile.objects.get(vendedor_id=vendedor_id)
    activo = c.activo
    return render_to_response('almuerzos/vendedor_perfil.html', {'user': user, 'activo' : activo, 'vendedor' : Vendedor.objects.get(id=vendedor_id), 'productos' : p})


def signup(request):
    return render(request, 'almuerzos/signup.html')


def login(request):
    c = {}
    c.update(csrf(request))
    return render_to_response('almuerzos/login.html', c)

def logout(request):
    auth.logout(request)
    return redirect('/almuerzos/')


def auth_view(request):
    email = request.POST.get('email', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username=email, password=password)

    if user is not None:
        auth.login(request, user)
        return HttpResponseRedirect('/almuerzos/')
    else:
        return HttpResponseRedirect('/almuerzos/login/')


def registration(request):
    if request.method == "POST":
        utype = request.POST.get('userType')
        if utype == None:
            return redirect('/almuerzos/signup/')

        uform = MyUserForm(request.POST)

        vform = None
        if utype == "3":
            cform = ConsumidorForm(request.POST)

        elif utype == "2":
            cform = MovilForm(request.POST)
            vform = VendedorForm(request.POST)

        elif utype == "1":
            cform = FijoForm(request.POST)
            vform = VendedorForm(request.POST)

        uform.userType = int(utype)


        if uform.is_valid() and cform.is_valid():
            user = uform.save()
            user.set_password(user.password)
            user.save()
            if utype in ["1", "2"]:
                if vform.is_valid():
                    vendedor = vform.save(commit = False)
                    vendedor.user = user
                    vendedor.save()
                    profile = cform.save(commit = False)
                    profile.vendedor = vendedor
                    profile.save()
                    new_user = auth.authenticate(username = uform.cleaned_data['email'],
                                                 password=uform.cleaned_data['password'])
                    auth.login(request, new_user)
                    return redirect('/almuerzos/')
                else :
                    return redirect('/almuerzos/signup/')

            profile = cform.save(commit = False)
            profile.user = user
            profile.save()
            new_user = auth.authenticate(username=uform.cleaned_data['email'],
                                         password=uform.cleaned_data['password'])
            auth.login(request, new_user)
            return redirect('/almuerzos/')
        else:
            return redirect('/almuerzos/signup/')

    else:
        return redirect('/almuerzos/login/')


def edit(request):
    return render(request, 'almuerzos/edit.html')




@login_required
def edit_auth(request):
    if request.method == 'POST':
        user = MyUser.objects.get(pk=request.user.id)
        if request.POST.get('nombre') != '':
            user.nombre = request.POST.get('nombre')
        user.save(update_fields=['nombre'])

        utype = user.userType.id

        c = None
        v = None
        if utype == 3:
            c = ConsumidorProfile.objects.get(user_id = user.id)
            if request.POST.get('avatar') != None:
                c.avatar = request.POST.get('avatar')
            c.save(update_fields=['avatar'])

        if utype == 2:
            v = Vendedor.objects.get(user_id = user.id)
            if request.POST.get('efectivo') != None:
                v.efectivo = True

            if request.POST.get('debito') != None:
                v.debito = True

            if request.POST.get('credito') != None:
                v.credito = True

            if request.POST.get('junaeb') != None:
                v.junaeb = True

            v.save(update_fields=['efectivo', 'debito', 'credito', 'junaeb'])

        elif utype == 1:
            v = Vendedor.objects.get(user_id = user.id)
            if request.POST.get('efectivo') != None:
                v.efectivo = True
            else:
                v.efectivo = False

            if request.POST.get('debito') != None:
                v.debito = True
            else:
                v.debito = False

            if request.POST.get('credito') != None:
                v.credito = True
            else:
                v.credito = False

            if request.POST.get('junaeb') != None:
                v.junaeb = True
            else:
                v.junaeb = False

            if request.POST.get('avatar') != None:
                v.avatar = request.POST.get('avatar')


            v.save(update_fields=['efectivo', 'debito', 'credito', 'junaeb', 'avatar'])
            c = FijoProfile.objects.get(vendedor_id = v.id)
            if request.POST.get('horaIni') != '':
                c.horaIni = request.POST.get('horaIni')

            if request.POST.get('horaFin') != '':
                c.horaFin = request.POST.get('horaFin')


            c.save(update_fields=['horaIni', 'horaFin'])

            return redirect('/almuerzos/vendedor_perfil/')


def ajaxActive(request):
    act = request.GET.get('activo', None)
    user = request.user
    v = Vendedor.objects.get(user_id = user.id)
    m = MovilProfile.objects.get(vendedor_id=v.id)
    acti = None
    if act == 'true':
        acti = True
    if act == 'false':
        acti = False
    m.activo = acti
    m.save(update_fields=['activo'])
    data = {
        'activacion': MovilProfile.objects.filter(vendedor_id=v.id)[0].activo
    }
    if data['activacion']:
        data['succ'] = 'CheckIn'
    return JsonResponse(data)