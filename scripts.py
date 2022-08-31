from random import choice

from django.core.exceptions import MultipleObjectsReturned

from datacenter.models import (
    Schoolkid,
    Mark,
    Chastisement,
    Commendation,
    Lesson,
    Subject
)


class DbSearchError(RuntimeError):
    pass


def get_schoolkid(name):
    try:
        return Schoolkid.objects.get(full_name__contains=name)
    except MultipleObjectsReturned:
        raise DbSearchError('Найдено несколько учеников. Уточните поиск')
    except Schoolkid.DoesNotExist:
        raise DbSearchError('Ученик не найден')


def get_commendation_text() -> str:
    return choice(
        (
            'Молодец!',
            'Отлично!',
            'Хорошо!',
            'Гораздо лучше, чем я ожидал!',
            'Ты меня приятно удивил!',
        )
    )


def fix_marks(name: str) -> [None, str]:
    try:
        schoolkid = get_schoolkid(name)
        Mark.objects.filter(
            schoolkid=schoolkid,
            points__in=[2, 3]
        ).update(points=5)
    except DbSearchError as err:
        return err.args[0]


def remove_chastisements(name: str) -> [None, str]:
    try:
        schoolkid = get_schoolkid(name)
        Chastisement.objects.filter(schoolkid=schoolkid).delete()
    except DbSearchError as err:
        return err.args[0]


def create_commendation(name: str, subject_title: str) -> [None, str]:
    try:
        schoolkid = get_schoolkid(name)
        subject = Subject.objects.get(
            title=subject_title,
            year_of_study=schoolkid.year_of_study
        )
    except DbSearchError as err:
        print(err.args[0])
        return
    except Subject.DoesNotExist:
        print('Предмет не найден')
        return

    lesson = Lesson.objects.filter(
        year_of_study=schoolkid.year_of_study,
        group_letter=schoolkid.group_letter,
        subject=subject
    ).order_by('date').last()
    if not lesson:
        print('Урок не найден')
        return

    Commendation.objects.create(
        text=get_commendation_text(),
        created=lesson.date,
        schoolkid=schoolkid,
        subject=lesson.subject,
        teacher=lesson.teacher,
    )
