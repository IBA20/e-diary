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
        schoolkid = Schoolkid.objects.get(full_name__contains=name)
    except MultipleObjectsReturned:
        return 'Найдено несколько учеников. Уточните поиск'
    except Schoolkid.DoesNotExist:
        return 'Ученик не найден'
    Mark.objects.filter(
        schoolkid=schoolkid,
        points__in=[2, 3]
    ).update(points=5)


def remove_chastisements(name: str) -> [None, str]:
    try:
        schoolkid = Schoolkid.objects.get(full_name__contains=name)
    except MultipleObjectsReturned:
        return 'Найдено несколько учеников. Уточните поиск'
    except Schoolkid.DoesNotExist:
        return 'Ученик не найден'
    Chastisement.objects.filter(schoolkid=schoolkid).delete()


def create_commendation(name: str, subject_title: str) -> [None, str]:
    try:
        schoolkid = Schoolkid.objects.get(full_name__contains=name)
    except MultipleObjectsReturned:
        return 'Найдено несколько учеников. Уточните поиск'
    except Schoolkid.DoesNotExist:
        return 'Ученик не найден'

    try:
        subject = Subject.objects.get(
            title=subject_title,
            year_of_study=schoolkid.year_of_study
        )
    except Subject.DoesNotExist:
        return 'Предмет не найден'

    lesson = Lesson.objects.filter(
        year_of_study=schoolkid.year_of_study,
        group_letter=schoolkid.group_letter,
        subject=subject
    ).order_by('date').last()
    if not lesson:
        return 'Урок не найден'

    Commendation.objects.create(
        text=get_commendation_text(),
        created=lesson.date,
        schoolkid=schoolkid,
        subject=lesson.subject,
        teacher=lesson.teacher,
    )
