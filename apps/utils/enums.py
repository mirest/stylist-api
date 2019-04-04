
class UserEnum():
    STYLIST = 'stylist'
    CLIENT = 'client'
    ADMIN = 'admin'
    USER_TYPES = (
        (CLIENT, 'client'),
        (STYLIST, 'stylist'),
        (ADMIN, 'admin'),
    )

    @classmethod
    def get_user_types(cls):
        return [cls.CLIENT, cls.STYLIST,cls.ADMIN]