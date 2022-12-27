from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required # IMPORTANDO DECORADORES PARA ACESSAR COM LOGIN
from django.core.paginator import Paginator # PAGINAÇÃO "DELIMITADOR DE QUANTAS TAREFAS POR PÁGINA"
from django.http import HttpResponse
from .forms import TaskForm
from django.contrib import messages
import datetime

from .models import Task

#CRUD - READ
@login_required
def taskList(request):

    search = request.GET.get('search') #SETAR O NAME QUE FOI UTILIZADO NO TEMPLATE
    filter = request.GET.get('filter') #FILTRAR O NAME QUE FOI UTILIZADO NO TEMPLATE
    taskDoneRecently = Task.objects.filter(done='done', updated_at__gt=datetime.datetime.now()-datetime.timedelta(days=30)).count() #TAREFAS FEITAS NOS ULTIMOS 30 DIAS
    taskDone = Task.objects.filter(done='done', user=request.user).count() #TAREFAS FEITAS
    taskDoing = Task.objects.filter(done='doing', user=request.user).count() #TAREFAS QUE ESTÃO SENDO FEITAS 


    if search:

        tasks = Task.objects.filter(title__icontains=search, user=request.user) #PARA NÃO PRECISAR ESCREVER A PALAVRA TAL E QUAL ESTÁ NO TITULO / FILTRAR AS TAREFAS POR ID

    elif filter:
        tasks = Task.objects.filter(done=filter, user=request.user)

    else:
        tasks_list = Task.objects.all().order_by('-created_at').filter(user=request.user)

        # DELIMITADOR DE QUANTAS TAREFAS POR PÁGINA
        paginator = Paginator(tasks_list, 5) 

        page = request.GET.get('page')

        tasks = paginator.get_page(page)

    return render(request, 'tasks/list.html', {'tasks':tasks, 'taskDoneRecently':taskDoneRecently, 'taskDone':taskDone, 'taskDoing':taskDoing})

@login_required
def taskView(request, id):
    task = get_object_or_404(Task, pk=id) # TRATAR O ERRO CASO NAO TENHA NENHUMA TAREFA A SER DESCRITA
    return render(request, 'tasks/task.html', {'task':task})
    

#CRUD - CREATE
@login_required
def newTask(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)

        if form.is_valid():
            task = form.save(commit=False) #VAI PARA O PROCESSO DE INSERIR DADOS ATÉ A GENTE SALVAR 
            task.done = 'doing'
            task.user = request.user #ADICONANDO UMA TAREFA NO ID DO USUARIO LOGADO
            task.save()
            return redirect('/')  # RETORNAR PARA A LISTA DE POST NOVAMENTE (IMPORTAR)

    else:
        form = TaskForm()
        return render(request,'tasks/addtask.html', {'form':form})


#CRUD - EDIT
@login_required
def editTask(request, id):
    task = get_object_or_404(Task, pk=id) #VAI ALTERAR DE ACORDO COM O ID
    form = TaskForm(instance=task) 

    if(request.method == 'POST'):
        form = TaskForm(request.POST, instance=task)

        if form.is_valid():
            task.save()
            return redirect('/')  #RETORNAR PARA A LISTA DE POST NOVAMENTE (IMPORTAR) 
        else:
            return render(request, 'tasks/edittask.html', {'form': form, 'task': task})

    else:
        return render(request, 'tasks/edittask.html', {'form': form, 'task': task})


#CRUD - DELETE
@login_required
def deleteTask(request, id):
    task = get_object_or_404(Task, pk=id)
    task.delete()

    messages.info(request, 'Tarefa deletada com sucesso') #CRIANDO ALERTA DE MENSAGEM  

    return redirect('/')


@login_required
def changeStatus(request, id):
    task = get_object_or_404(Task, pk=id)

    if(task.done == 'doing'):
        task.done = 'done'
    
    else:
        task.done = 'doing'

    task.save()

    return redirect('/')


def yourName(request, name):
    return render(request, 'tasks/yourname.html', {'name':name})


def helloWorld(request):
    return HttpResponse("Hello World!")