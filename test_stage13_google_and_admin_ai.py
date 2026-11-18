import unittest
import json
from app import app, get_db

class TestAuthAndAdminAi(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_01_google_auth_config(self):
        res = self.client.get('/api/auth/google/config')
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data.get('success'))
        self.assertIn('configured', data)
        self.assertIn('client_id', data)

    def test_02_google_auth_demo(self):
        res = self.client.post('/api/auth/google', json={
            'demo': True,
            'name': 'Aarav Sharma',
            'email': 'aarav.sharma@gmail.com'
        })
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data.get('success'))
        self.assertEqual(data.get('user', {}).get('email'), 'aarav.sharma@gmail.com')
        self.assertEqual(data.get('user', {}).get('user_type'), 'customer')

    def test_03_admin_ai_chat_with_token(self):
        # 1. Login as admin to get token
        res_login = self.client.post('/api/admin/login', json={
            'email': 'admin@locallift.com',
            'password': 'admin123'
        })
        login_data = res_login.get_json()
        token = login_data.get('token')
        self.assertTrue(token, "Admin login must return token")

        # 2. Simulate browser having customer session while sending Admin Token header
        with self.client.session_transaction() as sess:
            sess['user_type'] = 'customer'
            sess['user_id'] = 999

        # 3. Call /api/ai/admin/chat with Bearer token
        res_chat = self.client.post(
            '/api/ai/admin/chat',
            headers={'Authorization': f'Bearer {token}'},
            json={'message': 'Show marketplace KPIs & GMV', 'history': []}
        )
        self.assertEqual(res_chat.status_code, 200, f"Expected 200, got {res_chat.status_code}: {res_chat.data}")
        chat_data = res_chat.get_json()
        self.assertTrue(chat_data.get('success'), f"Expected success: true, got {chat_data}")
        self.assertIn('reply', chat_data)

    def test_04_admin_ai_chat_with_x_admin_token(self):
        # Login
        res_login = self.client.post('/api/admin/login', json={
            'email': 'admin@locallift.com',
            'password': 'admin123'
        })
        token = res_login.get_json().get('token')

        # Call with X-Admin-Token
        res_chat = self.client.post(
            '/api/ai/admin/chat',
            headers={'X-Admin-Token': token},
            json={'message': 'Show marketplace KPIs & GMV', 'history': []}
        )
        self.assertEqual(res_chat.status_code, 200)
        self.assertTrue(res_chat.get_json().get('success'))

if __name__ == '__main__':
    unittest.main()
