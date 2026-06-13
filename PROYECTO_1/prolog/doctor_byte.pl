sintoma(no_enciende,             'El equipo no enciende en absoluto').
sintoma(sin_energia,             'No hay luces ni ventiladores girando').
sintoma(pantalla_negra,          'Enciende pero la pantalla queda en negro').
sintoma(pantalla_azul,           'Aparece una pantalla azul (BSOD)').
sintoma(reinicios_inesperados,   'El equipo se reinicia solo sin avisar').
sintoma(apagados_repentinos,     'El equipo se apaga de golpe').
sintoma(sobrecalentamiento,      'El equipo se siente muy caliente').
sintoma(ventilador_ruidoso,      'El ventilador suena muy fuerte').
sintoma(ventilador_no_gira,      'El ventilador no gira').
sintoma(ruido_extrano,           'Se escuchan ruidos extranos o clics internos').
sintoma(lentitud,                'El sistema funciona muy lento').
sintoma(congelamiento,           'El sistema se congela con frecuencia').
sintoma(no_arranca_so,           'El sistema operativo no inicia').
sintoma(error_arranque,          'Muestra un error al arrancar').
sintoma(ventanas_emergentes,     'Aparecen ventanas o anuncios no deseados').
sintoma(sin_internet,            'No hay conexion a Internet').
sintoma(imagen_distorsionada,    'La imagen se ve distorsionada o con artefactos').
sintoma(bateria_no_carga,        'La bateria no carga').
sintoma(perifericos_no_responden,'El teclado o el mouse no responden').
sintoma(usb_no_reconocido,       'Los dispositivos USB no son reconocidos').

falla(falla_fuente_poder,     'Falla en la fuente de poder').
falla(falla_ventilador,       'Falla en el ventilador').
falla(sobrecalentamiento_cpu, 'Sobrecalentamiento del procesador (CPU)').
falla(acumulacion_polvo,      'Acumulacion de polvo en el interior del equipo').
falla(falla_ram,              'Falla en la memoria RAM').
falla(falla_disco_duro,       'Falla en el disco duro').
falla(infeccion_malware,      'Infeccion por malware o virus').
falla(falla_tarjeta_video,    'Falla en la tarjeta de video (GPU)').
falla(corrupcion_so,          'Corrupcion del sistema operativo').
falla(falla_tarjeta_red,      'Falla en la tarjeta de red').
falla(falla_bateria,          'Falla en la bateria').
falla(falla_perifericos,      'Falla en perifericos (teclado / mouse / USB)').


recomendacion(falla_fuente_poder,
    'Verifique el cable de poder y pruebe con otra fuente; si persiste, reemplace la fuente de poder.').
recomendacion(falla_ventilador,
    'Revise que el ventilador este conectado y libre de obstrucciones; reemplacelo si no gira.').
recomendacion(sobrecalentamiento_cpu,
    'Limpie el disipador, reaplique pasta termica y mejore la ventilacion del equipo.').
recomendacion(acumulacion_polvo,
    'Realice una limpieza interna del equipo con aire comprimido.').
recomendacion(falla_ram,
    'Reasiente los modulos de RAM y ejecute una prueba de memoria (memtest).').
recomendacion(falla_disco_duro,
    'Respalde sus datos de inmediato y ejecute un diagnostico SMART del disco.').
recomendacion(infeccion_malware,
    'Ejecute un analisis completo con un antivirus actualizado y elimine las amenazas.').
recomendacion(falla_tarjeta_video,
    'Reasiente la tarjeta de video, actualice los controladores y pruebe con video integrado.').
recomendacion(corrupcion_so,
    'Repare el sistema operativo desde el medio de instalacion o reinstalelo.').
recomendacion(falla_tarjeta_red,
    'Verifique los controladores de red, reinicie el router y pruebe con cable Ethernet.').
recomendacion(falla_bateria,
    'Calibre o reemplace la bateria y verifique el estado del cargador.').
recomendacion(falla_perifericos,
    'Pruebe los dispositivos en otros puertos USB y reinstale sus controladores.').


diagnostico(falla_fuente_poder) :-
    sintoma_activo(no_enciende),
    sintoma_activo(sin_energia).

diagnostico(falla_ventilador) :-
    sintoma_activo(ventilador_no_gira),
    sintoma_activo(sobrecalentamiento).

diagnostico(sobrecalentamiento_cpu) :-
    sintoma_activo(sobrecalentamiento),
    sintoma_activo(apagados_repentinos).

diagnostico(acumulacion_polvo) :-
    sintoma_activo(sobrecalentamiento),
    sintoma_activo(ventilador_ruidoso),
    sintoma_activo(ruido_extrano).

diagnostico(falla_ram) :-
    sintoma_activo(pantalla_azul),
    sintoma_activo(reinicios_inesperados).

diagnostico(falla_disco_duro) :-
    sintoma_activo(ruido_extrano),
    sintoma_activo(lentitud).

diagnostico(infeccion_malware) :-
    sintoma_activo(lentitud),
    sintoma_activo(ventanas_emergentes).

diagnostico(falla_tarjeta_video) :-
    sintoma_activo(imagen_distorsionada),
    sintoma_activo(pantalla_negra).

diagnostico(corrupcion_so) :-
    sintoma_activo(no_arranca_so),
    sintoma_activo(error_arranque).

diagnostico(falla_tarjeta_red) :-
    sintoma_activo(sin_internet).

diagnostico(falla_bateria) :-
    sintoma_activo(bateria_no_carga),
    sintoma_activo(apagados_repentinos).

diagnostico(falla_perifericos) :-
    sintoma_activo(perifericos_no_responden),
    sintoma_activo(usb_no_reconocido).

