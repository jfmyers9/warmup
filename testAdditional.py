import unittest
import os
import testLib

class TestAddUser(testLib.RestTestCase):

	def testAdd2(self):
		respData = self.makeRequest("/users/add", method="POST", data = { 'user' : 'user1', 'password' : 'password1'} )
		self.assertResponse(respData, count = 1)
		respData = self.makeRequest("/users/add", method="POST", data = { 'user' : 'user2', 'password' : 'password2'} )
		self.assertResponse(respData, count = 1)
		respData = self.makeRequest("/users/add", method="POST", data = { 'user' : 'user3', 'password' : 'password3'} )
		self.assertResponse(respData, count = 1)
		respData = self.makeRequest("/users/add", method="POST", data = { 'user' : 'user4', 'password' : 'password4'} )
		self.assertResponse(respData, count = 1)

	def testAddBadUserName(self):
		user = 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
		respData = self.makeRequest("/users/add", method="POST", data = { 'user' : '', 'password' : 'password'})
		self.assertResponse(respData, count = None, errCode = testLib.RestTestCase.ERR_BAD_USERNAME)
		respData = self.makeRequest("/users/add", method="POST", data = { 'user' : user, 'password' : 'password'})
		self.assertResponse(respData, count = None, errCode = testLib.RestTestCase.ERR_BAD_USERNAME)

	def testAddBadPassword(self):
		password = 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
		respData = self.makeRequest("/users/add", method="POST", data = { 'user' : 'jfmyers', 'password' : password})
		self.assertResponse(respData, count = None, errCode = testLib.RestTestCase.ERR_BAD_PASSWORD)
		respData = self.makeRequest("/users/add", method="POST", data = { 'user' : 'jfmyers', 'password' : ""})
		self.assertResponse(respData, count = 1)

	def testAddAlreadyExisting(self):
		respData = self.makeRequest("/users/add", method="POST", data = { 'user' : 'jfmyers', 'password' : "hi"})
		self.assertResponse(respData, count = 1)
		respData = self.makeRequest("/users/add", method="POST", data = { 'user' : 'jfmyers', 'password' : "hi"})
		self.assertResponse(respData, count = None, errCode = testLib.RestTestCase.ERR_USER_EXISTS)

	def assertResponse(self, respData, count = 1, errCode = testLib.RestTestCase.SUCCESS):
		expected = { 'errCode' : errCode }
		if count is not None:
			expected['count'] = count
		self.assertDictEqual(expected, respData)

class TestLoginUser(testLib.RestTestCase):

	def assertResponse(self, respData, count = 1, errCode = testLib.RestTestCase.SUCCESS):
		expected = { 'errCode' : errCode }
		if count is not None:
			expected['count']  = count
		self.assertDictEqual(expected, respData)

	def testLogin(self):
		respData = self.makeRequest("/users/add", method="POST", data = { 'user' : 'jfmyers9', 'password' : 'hi'})
		self.assertResponse(respData, count = 1)
		respData = self.makeRequest("/users/login", method="POST", data = { 'user' : 'jfmyers9', 'password' : 'hi'})
		self.assertResponse(respData, count = 2)
		respData = self.makeRequest("/users/login", method="POST", data = { 'user' : 'jfmyers9', 'password' : 'hi'})
		self.assertResponse(respData, count = 3)

	def testincorrectLogin(self):
		respData = self.makeRequest("/users/add", method="POST", data = { 'user' : 'jfmyers9', 'password' : 'hi'})
		self.assertResponse(respData, count = 1)
		respData = self.makeRequest("/users/login", method="POST", data = { 'user' : 'jfmyers', 'password' : "hello"})
		self.assertResponse(respData, count = None, errCode = testLib.RestTestCase.ERR_BAD_CREDENTIALS)

class TestTestAPIResetFixture(testLib.RestTestCase):

	def assertResponse(self, respData, count = 1, errCode = testLib.RestTestCase.SUCCESS):
		expected = { 'errCode' : errCode }
		if count is not None:
			expected['count']  = count
		self.assertDictEqual(expected, respData)

	def testTestAPIReset(self):
		respData = self.makeRequest("/users/add", method="POST", data = { 'user' : 'user1', 'password' : 'password1'} )
		self.assertResponse(respData, count = 1)
		respData = self.makeRequest("/users/add", method="POST", data = { 'user' : 'user2', 'password' : 'password2'} )
		self.assertResponse(respData, count = 1)
		respData = self.makeRequest("/users/add", method="POST", data = { 'user' : 'user3', 'password' : 'password3'} )
		self.assertResponse(respData, count = 1)
		respData = self.makeRequest("/users/add", method="POST", data = { 'user' : 'user4', 'password' : 'password4'} )
		self.assertResponse(respData, count = 1)
		respData = self.makeRequest("/TESTAPI/resetFixture", method="POST", data = {} )
		respData = self.makeRequest("/users/login", method="POST", data = { 'user' : 'user1', 'password' : 'password1'} )
		self.assertResponse(respData, count = None, errCode = testLib.RestTestCase.ERR_BAD_CREDENTIALS)
		respData = self.makeRequest("/users/login", method="POST", data = { 'user' : 'user2', 'password' : 'password2'} )
		self.assertResponse(respData, count = None, errCode = testLib.RestTestCase.ERR_BAD_CREDENTIALS)
		respData = self.makeRequest("/users/login", method="POST", data = { 'user' : 'user3', 'password' : 'password3'} )
		self.assertResponse(respData, count = None, errCode = testLib.RestTestCase.ERR_BAD_CREDENTIALS)
		respData = self.makeRequest("/users/login", method="POST", data = { 'user' : 'user4', 'password' : 'password4'} )
		self.assertResponse(respData, count = None, errCode = testLib.RestTestCase.ERR_BAD_CREDENTIALS)
