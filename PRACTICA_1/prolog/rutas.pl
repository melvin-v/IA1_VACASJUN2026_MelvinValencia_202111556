ciudad(guatemala).
ciudad(escuintla).
ciudad(sacatepequez).
ciudad(chimaltenango).
ciudad(quetzaltenango).
ciudad(suchitepequez).
ciudad(retalhuleu).
ciudad(solola).
ciudad(totonicapan).
ciudad(huehuetenango).
ciudad(quiche).
ciudad(alta_verapaz).
ciudad(baja_verapaz).
ciudad(el_progreso).

conectado(guatemala,    escuintla,       58).
conectado(guatemala,    sacatepequez,    28).
conectado(guatemala,    chimaltenango,   54).
conectado(guatemala,    el_progreso,     74).
conectado(guatemala,    baja_verapaz,   130).

conectado(sacatepequez, chimaltenango,   20).
conectado(sacatepequez, escuintla,       52).

conectado(chimaltenango, solola,         57).
conectado(chimaltenango, quiche,        110).
conectado(chimaltenango, baja_verapaz,  110).

conectado(escuintla,    suchitepequez,   69).
conectado(escuintla,    retalhuleu,     105).

conectado(solola,       quetzaltenango,  51).
conectado(solola,       totonicapan,     35).
conectado(solola,       suchitepequez,   55).

conectado(quetzaltenango, totonicapan,   40).
conectado(quetzaltenango, huehuetenango, 95).
conectado(quetzaltenango, retalhuleu,    65).
conectado(quetzaltenango, suchitepequez, 60).

conectado(totonicapan,  huehuetenango,  104).
conectado(totonicapan,  quiche,          74).

conectado(huehuetenango, quiche,        105).

conectado(quiche,       alta_verapaz,   118).
conectado(quiche,       baja_verapaz,   105).

conectado(baja_verapaz, alta_verapaz,    75).
conectado(baja_verapaz, el_progreso,     60).

conectado(suchitepequez, retalhuleu,     35).

arista(A, B, D) :- conectado(A, B, D).
arista(A, B, D) :- conectado(B, A, D).

ruta(Origen, Destino, Visitados, [Origen, Destino], Dist) :-
    arista(Origen, Destino, Dist),
    \+ member(Destino, Visitados).

ruta(Origen, Destino, Visitados, [Origen | Resto], DistTotal) :-
    arista(Origen, Siguiente, D1),
    Siguiente \= Destino,
    \+ member(Siguiente, Visitados),
    ruta(Siguiente, Destino, [Siguiente | Visitados], Resto, D2),
    DistTotal is D1 + D2.

todas_rutas(Origen, Destino, Rutas) :-
    findall(
        ruta(Camino, Dist),
        ruta(Origen, Destino, [Origen], Camino, Dist),
        Rutas
    ).

ruta_mas_corta(Origen, Destino, CaminoMinimo, DistMinima) :-
    todas_rutas(Origen, Destino, Rutas),
    Rutas \= [],
    minima(Rutas, ruta(CaminoMinimo, DistMinima)).

minima([Unica], Unica) :- !.
minima([ruta(C1, D1) | Resto], Minima) :-
    minima(Resto, ruta(C2, D2)),
    (   D1 =< D2
    ->  Minima = ruta(C1, D1)
    ;   Minima = ruta(C2, D2)
    ).

ciudad_existe(Ciudad) :- ciudad(Ciudad).

:- dynamic ciudad/1.
:- dynamic conectado/3.

agregar_ciudad(Ciudad) :-
    (   ciudad(Ciudad)
    ->  true
    ;   assertz(ciudad(Ciudad))
    ).

agregar_conexion(A, B, D) :-
    (   conectado(A, B, D)
    ->  true
    ;   assertz(conectado(A, B, D))
    ).

listar_ciudades(Lista) :-
    findall(C, ciudad(C), Lista).