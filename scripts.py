from random import choice
from datacenter.models import (
    Schoolkid,
    Mark,
    Chastisement,
    Commendation,
    Lesson,
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


def get_schoolkid(name: str) -> [Schoolkid, None]:
    name_parts = name.split()
    queryset = Schoolkid.objects.all()
    for name_part in name_parts:
        queryset = queryset.filter(full_name__contains=name_part)
    if len(queryset) != 1:
        return
    return queryset.first()


def fix_marks(name: str) -> [None, str]:
    schoolkid = get_schoolkid(name)
    if not schoolkid:
        return 'Уточните имя ученика'
    Mark.objects.filter(
        schoolkid=schoolkid,
        points__in=[2, 3]
    ).update(points=5)


def remove_chastisements(name: str) -> [None, str]:
    schoolkid = get_schoolkid(name)
    if not schoolkid:
        return 'Уточните имя ученика'
    Chastisement.objects.filter(schoolkid=schoolkid).delete()


def create_commendation(name: str, subject_title: str) -> [None, str]:
    schoolkid = get_schoolkid(name)
    if not schoolkid:
        return 'Уточните имя ученика'
    lesson = Lesson.objects.filter(
        year_of_study=schoolkid.year_of_study,
        group_letter=schoolkid.group_letter,
        subject__title=subject_title
    ).order_by('date').last()
    if not lesson:
        return 'Предмет/урок не найден'
    Commendation.objects.create(
        text=get_commendation_text(),
        created=lesson.date,
        schoolkid=schoolkid,
        subject=lesson.subject,
        teacher=lesson.teacher,
    )
