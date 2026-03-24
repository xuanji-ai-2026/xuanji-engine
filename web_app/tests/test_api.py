"""
后端 - 支付API - API测试
任务ID: TASK-0004
"""

import pytest
from fastapi.testclient import TestClient
from api import app

client = TestClient(app)

def test_register():
    """测试用户注册"""
    response = client.post(
        "/register",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpass123"
        }
    )
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"

def test_login():
    """测试用户登录"""
    response = client.post(
        "/login",
        params={
            "username": "testuser",
            "password": "testpass123"
        }
    )
    assert response.status_code == 200

def test_get_users():
    """测试获取用户列表"""
    response = client.get("/users")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
