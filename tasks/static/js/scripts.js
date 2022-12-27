    // CRIANDO ALERTA POR QUERY PARA ALERTAR ANTES DE DELETAR AS TAREFAS
$(document).ready(function(){
    
    var baseUrl = 'http://localhost:8000/'; //URL BASE DE CONFIGURAÇÃO
    var deleteBtn = $('.delete-btn'); //ATIVAÇÃO DO COMANDO NO TEMPLATE
    
    
    $(deleteBtn).on('click', function(e){

        e.preventDefault();
        
        var delLink = $(this).attr('href');
        var result = confirm('Quer deletar está tarefa?');
        
        if(result){
            window.location.href = delLink;
        }
    });
    
    
    // CRIANDO SISTEMA DE BUSCAS
    var searchBtn = $('.search-btn'); //ATIVAÇÃO DO COMANDO NO TEMPLATE
    var searchForm = $('.search-form'); 

    $(searchBtn).on('click', function(){
        searchForm.submit();

    });

    var filter = $('#filter');

    $(filter).change(function(){
        var filter = $(this).val()
        window.location.href = baseUrl + '?filter='+ filter;
    });

    
});


