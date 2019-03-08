import datetime
from custom_exceptions import ExcesoDeLikes, TagNulo


def tiempo_trending(publish_date, trending_date):

    fecha_sin_puntos = publish_date.replace(".", "")
    if not (fecha_sin_puntos.isdigit() and len(fecha_sin_puntos) == 6):
        raise ValueError("la fecha debe venir con el formato apropiado")
    elif not (publish_date[2] is '.' and publish_date[5] is '.'):
        raise ValueError("la fecha debe venir con el formato apropiado")
    publish_d = datetime.datetime.strptime(publish_date, "%y.%d.%m")
    trending_d = datetime.datetime.strptime(trending_date, "%y.%d.%m")
    days = (trending_d - publish_d).days

    return days


def like_dislike_ratio(likes, dislikes):
    if not (likes.isdigit() and dislikes.isdigit()):
        raise TypeError("Debe ingresar números apropiados")

    if int(dislikes) == 0:
        raise ZeroDivisionError("El denominador del ratio no puede ser cero")

    return int(likes) / int(dislikes)


def info_video(title, views, likes, dislikes, tags):

    if not (likes.isdigit() and views.isdigit()):
        raise TypeError("likes y views deben ser números enteros")
    if not int(views) >= int(likes):
        raise ExcesoDeLikes
    if tags is None  or len(tags) == 0:
        raise TagNulo
    print("El video {0} ha tenido {1} views, con {2} likes y {3} dislikes"
          .format(title, views, likes, dislikes))
