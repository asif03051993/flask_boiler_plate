"""User serializers."""

def serialize_users(users):
    return [serialize_user(user) for user in users]


def serialize_user(user):
    result = {
        'id': user.id,
        'firstName': user.first_name,
        'lastName': user.last_name,
        'emailId': user.email_id,
        'phoneNumber': user.phone_number
    }

    return result