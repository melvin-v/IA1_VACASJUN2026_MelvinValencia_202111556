import bcrypt

from .database import Base, SessionLocal, engine
from .models import Categoria, Configuracion, Pregunta, UsuarioAdmin


def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


CATEGORIAS = [
    {
        "nombre": "Asignación e inscripción",
        "descripcion": "Dudas sobre asignación, reasignación, cupos y fechas.",
    },
    {
        "nombre": "Evaluación y aprobación",
        "descripcion": "Notas, asistencia, parciales y requisitos para aprobar.",
    },
    {
        "nombre": "Pagos, cuotas y reembolsos",
        "descripcion": "Costos de cursos y laboratorios, reajustes y reembolsos.",
    },
    {
        "nombre": "Modalidad y desarrollo",
        "descripcion": "Modalidad virtual, horarios y carga de notas.",
    },
]


PREGUNTAS = [
    {
        "categoria": "Asignación e inscripción",
        "pregunta": "¿Cuántos cursos puedo asignarme en la Escuela de Vacaciones?",
        "respuesta": "Puedes asignarte como máximo en dos cursos simples, siempre que tengan compatibilidad de horarios, o en un curso doble. Las horas asignadas a laboratorios no se incluyen dentro de este límite.",
        "palabras_clave": "cuantos cursos asignar maximo dos simples doble limite asignacion",
    },
    {
        "categoria": "Asignación e inscripción",
        "pregunta": "¿Qué es la asignación condicionada?",
        "respuesta": "La asignación condicionada aplica cuando no tienes aprobado el prerrequisito de un curso. Puedes asignarte siempre que apruebes ese prerrequisito durante las evaluaciones finales o la primera retrasada del semestre. Si no cumples esa condición, tu asignación no tendra validez y Centro de Cálculo realizará la desasignación automática.",
        "palabras_clave": "asignacion condicionada prerrequisito desasignacion automatica final retrasada",
    },
    {
        "categoria": "Asignación e inscripción",
        "pregunta": "¿Puedo asignarme cursos con horarios traslapados?",
        "respuesta": "No. No puedes asignarte cursos ni laboratorios si los horarios de las asignaturas se traslapan entre sí.",
        "palabras_clave": "horarios traslape traslapados choque cursos laboratorios asignar",
    },
    {
        "categoria": "Asignación e inscripción",
        "pregunta": "¿Hasta cuándo puedo generar boleta y asignarme?",
        "respuesta": "La generación de boleta de pago y la asignación se realizan desde la última semana de noviembre hasta el primer día de inicio de la Escuela de Vacaciones. Realizar el pago y confirmar la asignación es responsabilidad únicamente del estudiante; no se aceptan asignaciones fuera de las fechas autorizadas.",
        "palabras_clave": "boleta pago fecha asignacion plazo hasta cuando generar inscripcion",
    },
    {
        "categoria": "Asignación e inscripción",
        "pregunta": "¿Puedo reasignarme a otro curso?",
        "respuesta": "Puedes reasignarte en línea durante el segundo, tercer y cuarto día después de iniciado el curso. La reasignación solo procede si se suprime el curso en el que te asignaste o si aparece incompatibilidad por cambios de horario o modalidad. Después de ese periodo no se aceptan reasignaciones.",
        "palabras_clave": "reasignar reasignacion cambiar curso dias plazo cambio horario",
    },
    {
        "categoria": "Asignación e inscripción",
        "pregunta": "¿Cuántos alumnos se necesitan para abrir un curso?",
        "respuesta": "Para autorizar la apertura de un curso deben inscribirse al menos 10 alumnos, siempre que los interesados estén anuentes al pago del reajuste correspondiente cuando aplique.",
        "palabras_clave": "minimo alumnos abrir curso apertura diez 10 cupo inscritos",
    },
    {
        "categoria": "Evaluación y aprobación",
        "pregunta": "¿Cuál es la nota mínima para aprobar?",
        "respuesta": "La nota mínima para aprobar un curso es de 61 puntos sobre 100.",
        "palabras_clave": "nota minima aprobar 61 puntos promocion ganar curso",
    },
    {
        "categoria": "Evaluación y aprobación",
        "pregunta": "¿Cuánta asistencia necesito para aprobar?",
        "respuesta": "Debes cumplir con una asistencia no menor al 75% del curso.",
        "palabras_clave": "asistencia minima 75 porciento aprobar requisito presencia",
    },
    {
        "categoria": "Evaluación y aprobación",
        "pregunta": "¿Cómo se reparte la nota del curso?",
        "respuesta": "La zona equivale al 75% de la nota total del curso y el examen final equivale al 25% restante.",
        "palabras_clave": "zona examen final porcentaje 75 25 reparto nota ponderacion",
    },
    {
        "categoria": "Evaluación y aprobación",
        "pregunta": "¿Cuántos exámenes parciales hay?",
        "respuesta": "El docente debe realizar como mínimo dos evaluaciones parciales, además de tareas, hojas de trabajo y evaluaciones cortas que conforman la zona.",
        "palabras_clave": "parciales cuantos examenes dos evaluaciones zona tareas",
    },
    {
        "categoria": "Evaluación y aprobación",
        "pregunta": "¿Hay exámenes de recuperación?",
        "respuesta": "No. Los cursos de vacaciones no tienen evaluaciones de recuperación.",
        "palabras_clave": "recuperacion retrasada examen vacaciones no hay reposicion",
    },
    {
        "categoria": "Evaluación y aprobación",
        "pregunta": "¿La zona de vacaciones sirve para el curso regular?",
        "respuesta": "No. La zona obtenida en los cursos de vacaciones no es válida para los cursos regulares del semestre.",
        "palabras_clave": "zona vacaciones curso regular semestre sirve valida traslado",
    },
    {
        "categoria": "Evaluación y aprobación",
        "pregunta": "¿Qué se necesita para los exámenes virtuales?",
        "respuesta": "Cuando los exámenes parciales y finales se realizan de forma virtual en la plataforma UEDi, debe incorporarse el uso del Navegador de Examen Seguro (SEB) y cámara, para reducir el mal uso de herramientas externas.",
        "palabras_clave": "examen virtual seb navegador seguro camara uedi requisitos",
    },
    {
        "categoria": "Pagos, cuotas y reembolsos",
        "pregunta": "¿Cuánto cuesta un curso simple de 2 horas?",
        "respuesta": "Un curso de 2 horas diarias (curso simple) tiene una cuota de Q115.00.",
        "palabras_clave": "costo precio cuota curso simple dos horas 115 pago",
    },
    {
        "categoria": "Pagos, cuotas y reembolsos",
        "pregunta": "¿Cuánto cuesta un curso doble de 4 horas?",
        "respuesta": "Un curso de 4 horas diarias (curso doble) tiene una cuota de Q230.00.",
        "palabras_clave": "costo precio cuota curso doble cuatro horas 230 pago",
    },
    {
        "categoria": "Pagos, cuotas y reembolsos",
        "pregunta": "¿Cuánto cuesta el laboratorio de Ciencias y Sistemas?",
        "respuesta": "El laboratorio de la Escuela de Ingeniería en Ciencias y Sistemas tiene una cuota de Q80.00.",
        "palabras_clave": "costo laboratorio sistemas ciencias 80 cuota precio",
    },
    {
        "categoria": "Pagos, cuotas y reembolsos",
        "pregunta": "¿Los estudiantes no inscritos pagan más?",
        "respuesta": "Los estudiantes que no estén inscritos en el ciclo académico regular deben cancelar una cuota igual al doble del valor de las asignaturas. Lo mismo aplica a estudiantes de los Centros Regionales y de otras Facultades. Los estudiantes de otras universidades pagan una cuota igual a tres veces el valor.",
        "palabras_clave": "no inscritos pago doble triple regionales otras facultades universidades cuota",
    },
    {
        "categoria": "Pagos, cuotas y reembolsos",
        "pregunta": "¿Hay becas o descuentos?",
        "respuesta": "No. Al ser la Escuela de Vacaciones un proyecto autofinanciable, no se autorizan descuentos, becas, ayudas económicas ni similares.",
        "palabras_clave": "becas descuentos ayuda economica autofinanciable no hay",
    },
    {
        "categoria": "Pagos, cuotas y reembolsos",
        "pregunta": "¿Cuándo aplica un reembolso?",
        "respuesta": "Se autoriza reembolso cuando el curso o laboratorio se cierra por falta de docente o por no cumplir el cupo mínimo, o cuando existe incompatibilidad de horarios por una modificación hecha por la Coordinación. Además, el monto debe ser mayor a Q60.00.",
        "palabras_clave": "reembolso devolucion dinero cuando aplica cierre cupo horario 60",
    },
    {
        "categoria": "Pagos, cuotas y reembolsos",
        "pregunta": "¿Cuándo no se autoriza un reembolso?",
        "respuesta": "No se autoriza reembolso si te niegan el permiso en tu trabajo, si dejas de asistir por enfermedad, viajes, becas u otros compromisos personales, si pierdes el prerrequisito de la asignación condicionada, o si generas boleta y no completas tu proceso de asignación.",
        "palabras_clave": "reembolso no devolucion negado trabajo enfermedad viaje prerrequisito boleta",
    },
    {
        "categoria": "Pagos, cuotas y reembolsos",
        "pregunta": "¿Qué es el reajuste y cuándo se paga?",
        "respuesta": "El reajuste se paga cuando un curso o laboratorio no llena el cupo mínimo de estudiantes y los interesados aceptan completar el costo total. Se calcula restando del costo total lo pagado por los inscritos y prorrateando el resto entre ellos. Debe cancelarse dentro de los primeros 6 días hábiles posteriores al inicio de la Escuela de Vacaciones.",
        "palabras_clave": "reajuste pago cupo minimo prorrateo costo total seis dias",
    },
    {
        "categoria": "Modalidad y desarrollo",
        "pregunta": "¿En qué modalidad se imparte la Escuela de Vacaciones?",
        "respuesta": "La Escuela de Vacaciones se desarrolla exclusivamente en modalidad virtual, apoyándose en la plataforma UEDi mediante espacios sincrónicos y asincrónicos.",
        "palabras_clave": "modalidad virtual uedi presencial en linea sincronico asincronico",
    },
    {
        "categoria": "Modalidad y desarrollo",
        "pregunta": "¿Qué días y cuántas horas se imparten los cursos?",
        "respuesta": "Los cursos se imparten de lunes a viernes. Los cursos simples son de 2 horas diarias con una duración mínima de 40 horas, y los cursos dobles de 4 horas diarias con una duración mínima de 80 horas.",
        "palabras_clave": "dias horario lunes viernes horas duracion 40 80 simple doble",
    },
    {
        "categoria": "Modalidad y desarrollo",
        "pregunta": "¿Cuándo publican los horarios de los cursos?",
        "respuesta": "La Coordinación de Escuela de Vacaciones publica los horarios de los cursos, ya aprobados por Junta Directiva, quince días antes del inicio de cada Escuela de Vacaciones.",
        "palabras_clave": "horarios publicacion quince dias antes inicio cuando publican",
    },
    {
        "categoria": "Modalidad y desarrollo",
        "pregunta": "¿Cuándo cargan las notas de laboratorio?",
        "respuesta": "Las notas de laboratorio se cargan un día hábil después de finalizada la Escuela de Vacaciones, una vez que Centro de Cálculo habilita el sistema. Las notas de clase magistral se cargan cinco días hábiles después.",
        "palabras_clave": "notas laboratorio carga ingreso dias habiles finalizar magistral",
    },
]


def seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        if db.query(Categoria).count() > 0:
            print("La base de datos ya contiene datos. Seed omitido.")
            return

        categorias = {}
        for c in CATEGORIAS:
            obj = Categoria(nombre=c["nombre"], descripcion=c["descripcion"])
            db.add(obj)
            categorias[c["nombre"]] = obj
        db.flush()

        for p in PREGUNTAS:
            db.add(
                Pregunta(
                    categoria_id=categorias[p["categoria"]].id,
                    pregunta=p["pregunta"],
                    respuesta=p["respuesta"],
                    palabras_clave=p["palabras_clave"],
                )
            )

        db.add(
            UsuarioAdmin(
                username="IA1-User",
                password_hash=hash_password("IA1-password@_new"),
            )
        )
        db.add(Configuracion(clave="telegram_chat_id", valor=""))
        db.add(
            Configuracion(
                clave="mensaje_no_encontrado",
                valor=(
                    "Lo siento, no encontré información sobre tu consulta. "
                    "Intenta reformular la pregunta o contacta a la "
                    "Coordinación de Escuela de Vacaciones."
                ),
            )
        )

        db.commit()
        print(
            f"Seed completado: {len(CATEGORIAS)} categorias, "
            f"{len(PREGUNTAS)} preguntas, 1 usuario admin."
        )
    finally:
        db.close()


if __name__ == "__main__":
    seed()
