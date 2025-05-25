import logging
from typing import Tuple, Dict, Any
from utils.security import verify_password
from model.models import db, User

logger = logging.getLogger(__name__)


class LoginService:
    """登录服务类（与注册功能兼容版）"""

    def authenticate_user(self, login_data: dict) -> Tuple[bool, Dict[str, Any], str]:
        """
        验证用户登录（使用SQLAlchemy ORM）

        Args:
            login_data: 包含 username 和 password 的字典

        Returns:
            Tuple[bool, Dict[str, Any], str]: (成功状态, 用户数据, 消息)
        """
        try:
            logger.info(f"开始验证用户: {login_data.get('username')}")

            # 验证必要字段
            if 'username' not in login_data or 'password' not in login_data:
                return False, {}, "必须提供用户名和密码"

            # 查询用户
            user = User.query.filter_by(username=login_data['username']).first()

            if not user:
                logger.warning(f"用户不存在: {login_data['username']}")
                return False, {}, "用户不存在"

            # 验证密码（使用werkzeug的安全验证）
            if not verify_password(user.password, login_data['password']):
                logger.warning(f"密码验证失败: {login_data['username']}")
                return False, {}, "用户名或密码错误"

            # 构造返回数据
            user_data = {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "phone": user.phone,
                "role": user.role,
                "create_time": user.create_time.isoformat(),
                "update_time": user.update_time.isoformat()
            }

            logger.info(f"用户登录成功: {user.username}")
            return True, user_data, "登录成功"

        except Exception as e:
            logger.error(f"登录过程出错: {str(e)}", exc_info=True)
            db.session.rollback()
            return False, {}, "服务器内部错误"


# 使用示例
if __name__ == "__main__":
    from utils.security import get_password_hash

    # 测试用户数据（需先创建测试用户）
    test_user = {
        "username": "testuser",
        "password": get_password_hash("Test123!"),  # 假设数据库中已存储此哈希
        "email": "test@example.com",
        "phone": "13812345678",
        "role": 0
    }

    service = LoginService()
    # 模拟登录请求
    print(service.authenticate_user({
        "username": "testuser",
        "password": "Test123!"  # 正确密码
    }))  # 应返回(True, user_data, "登录成功")

    print(service.authenticate_user({
        "username": "wronguser",
        "password": "Test123!"
    }))  # 应返回(False, {}, "用户不存在")