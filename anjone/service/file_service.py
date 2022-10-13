import os
import uuid

from anjone.common import Response
from anjone.common.Constant import UPLOAD_AVATAR_PATH
from anjone.database import db_session
from anjone.models.sqlite.LocalUser import LocalUser
from anjone.models.vo.UserInfoVo import UserInfoVo


def upload_avatar(avatar, username):
    local_user = LocalUser.query.filter(LocalUser.username == username).first()
    # 保存图片
    last = os.path.splitext(avatar.filename)[-1]
    random_str = uuid.uuid1().hex
    avatar.save(os.path.join(UPLOAD_AVATAR_PATH, random_str + last))
    # 保存到数据库
    local_user.avatar = random_str + last
    db_session.commit()
    user_info_vo = UserInfoVo(local_user.username, local_user.phone, local_user.avatar, local_user.role, local_user.create_time)
    return Response.create_success(user_info_vo.to_json())
