from graphql import GraphQLError


def admin_required(func):
    def wrapper(info, request, *args, **kwargs):
        user = request.context.user
        if not user.is_anonymous and user.user_type == "admin":
            return func(*args, **kwargs)
        raise GraphQLError("Permission denied")
    return wrapper
