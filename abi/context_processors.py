def menu_segment(request):
    path = request.path  

    if 'admin/abi/curso' in path or 'admin/abi/areapesquisa' in path or 'admin/abi/areaartistica' in path or 'admin/abi/cargo' in path or '/admin/abi/cidade/' in path or  'admin/abi/estado' in path or '/admin/abi/escolaridade/' in path or '/admin/abi/etnia/' in path or '/admin/abi/genero/' in path or '/admin/abi/orientacaosexual/' in path: 
        secao = 'parametros_do_sistema'
    elif 'admin/abi/oficineiro' in path or 'admin/abi/pessoa' in path or '/admin/abi/membrodiretoria/' in path or '/admin/abi/bolsista/' in path:
        secao = 'integrantes'
    elif 'admin/abi/agenda' in path or '/admin/abi/evento/' in path or '/admin/abi/eventoxpessoa/' in path:
        secao =  'agenda'
    elif '/admin/abi/oficio/' in path:
        secao = 'oficios'
    else:
        secao = ''

    return {'secao': secao}
