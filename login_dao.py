from base.com.vo.login_vo import LoginVO


class LoginDAO:

    def view_login(self):
        login_vo_list = LoginVO.query.all()
        return login_vo_list







