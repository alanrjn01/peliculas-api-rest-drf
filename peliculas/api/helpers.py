from django.utils import timezone


def delete_sessions(user, session_class):
    all_sessions = session_class.objects.filter(expire_date__gte=timezone.now())
    if all_sessions.exists():
        for session in all_sessions:
            session_data = session.get_decoded()
            if user.id == int(session_data.get('_auth_user_id')):
                session.delete()
                return True
    return False


def return_characters_list(queryset):
    character_list = []
    for character in queryset:
        character_list.append(
            {
                'name': character.name
            }
        )
    return character_list
