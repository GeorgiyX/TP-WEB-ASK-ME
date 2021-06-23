from app.models import Tag, Profile
from app import constants


def get_right_col_data(request):
    return {"right_col": {"top_tags": Tag.objects.get_top(), "tag_url": constants.TAG_URL,
                          "top_users": Profile.objects.get_top()}}
