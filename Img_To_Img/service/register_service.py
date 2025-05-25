import logging
from typing import Tuple, Dict, Any
from datetime import datetime
from utils.security import get_password_hash
from model.models import db, User

logger = logging.getLogger(__name__)


class RegisterService:
    """注册服务类"""

    def create_user(self, user_data: dict) -> Tuple[bool, Dict[str, Any], str]:
        """
        创建新用户 (直接使用SQLAlchemy)

        :param user_data: 包含 username, password, email, phone, role 的字典
        :return: (成功状态, 用户数据, 消息)
        """
        try:
            logger.info(f"开始创建用户: {user_data['username']}")

            # 验证数据唯一性
            if User.query.filter_by(username=user_data['username']).first():
                return False, {}, "用户名已存在"

            if User.query.filter_by(email=user_data['email']).first():
                return False, {}, "邮箱已被注册"

            if User.query.filter_by(phone=user_data['phone']).first():
                return False, {}, "手机号已被注册"

            # 生成密码哈希（使用更安全的BCRYPT）
            hashed_password = get_password_hash(user_data['password'])

            # 创建用户对象
            new_user = User(
                username=user_data['username'],
                password=hashed_password,
                email=user_data['email'],
                phone=user_data['phone'],
                role=user_data.get('role', 0)
            )

            # 添加到数据库
            db.session.add(new_user)
            db.session.commit()

            # 返回结果
            user_info = {
                "id": new_user.id,
                "username": new_user.username,
                "email": new_user.email,
                "phone": new_user.phone,
                "role": new_user.role,
                "create_time": new_user.create_time.isoformat()
            }

            return True, user_info, "注册成功"

        except Exception as e:
            db.session.rollback()
            logger.error(f"注册失败: {str(e)}", exc_info=True)
            return False, {}, f"注册失败: {str(e)}"