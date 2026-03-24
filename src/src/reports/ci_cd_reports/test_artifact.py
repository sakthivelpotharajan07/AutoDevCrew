import pytest
from src.reports.ci_cd_reports.build_artifact import User, LoginPage

def test_user_initialization():
    user = User("test_user", "test_password")
    assert user.username == "test_user"
    assert user.password == "test_password"

def test_login_page_initialization():
    login_page = LoginPage()
    assert login_page.users == {}

def test_register_user_new_user():
    login_page = LoginPage()
    login_page.register_user("new_user", "new_password")
    assert "new_user" in login_page.users
    assert login_page.users["new_user"].username == "new_user"
    assert login_page.users["new_user"].password == "new_password"

def test_register_user_existing_user(capsys):
    login_page = LoginPage()
    login_page.register_user("existing_user", "existing_password")
    login_page.register_user("existing_user", "new_password")
    captured = capsys.readouterr()
    assert "Username already exists." in captured.out

def test_login_user_valid_credentials():
    login_page = LoginPage()
    login_page.register_user("test_user", "test_password")
    assert login_page.login_user("test_user", "test_password")

def test_login_user_invalid_password(capsys):
    login_page = LoginPage()
    login_page.register_user("test_user", "test_password")
    assert not login_page.login_user("test_user", "wrong_password")
    captured = capsys.readouterr()
    assert "Invalid password." in captured.out

def test_login_user_non_existent_user(capsys):
    login_page = LoginPage()
    assert not login_page.login_user("non_existent_user", "password")
    captured = capsys.readouterr()
    assert "Username does not exist." in captured.out