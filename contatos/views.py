from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.http import Http404
from .models import Contato
from django.db.models import Q, Value
from django.db.models.functions import Concat


def index(request):
    # contatos = Contato.objects.all()
    # contatos = Contato.objects.order_by('nome') # Ordem crescente
    # Ordem decrescente
    contatos = Contato.objects.order_by('-id').filter(
        mostrar=True
    )

    paginator = Paginator(contatos, 5) 
    
    page = request.GET.get('p')
    contatos = paginator.get_page(page)
    
    return render(request, 'contatos/index.html', {
        'contatos': contatos
    })


def ver_contato(request, contato_id):
    contato = get_object_or_404(Contato, id=contato_id)
    if not contato.mostrar:
        raise Http404
    return render(request, 'contatos/ver_contato.html', {
        'contato': contato
    })


def busca(request):
    termo = request.GET.get('termo')

    if termo is None:
        raise Http404

    campos = Concat('nome', Value(' '), 'sobrenome')

    # forma de pesquisar 1
    # contatos = Contato.objects.order_by('-id').filter(
    #     # nome=termo, # busca extata usando and
    #     # nome__icontains=termo, sobrenome__icontains=termo,
    #     # busca usando o Or
    #     Q(nome__icontains=termo) | Q(sobrenome__icontains=termo),
    #     mostrar=True
    # )

    # forma de pesquisar 2
    contatos = Contato.objects.annotate(
        nome_completo=campos
    ).filter(
        Q(nome_completo__icontains=termo) | Q(telefone__icontains=termo)
    )


    # string da consulta sql
    # print(contatos.query)

    paginator = Paginator(contatos, 5) 
    
    page = request.GET.get('p')
    contatos = paginator.get_page(page)
    
    return render(request, 'contatos/busca.html', {
        'contatos': contatos
    })