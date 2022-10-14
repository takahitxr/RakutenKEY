import hashlib
import sqlite3
import streamlit as st
import pandas as pd
from app import mainapp

conn = sqlite3.connect('database.db')
c = conn.cursor()

def make_hashes(password):
	return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password,hashed_text):
	if make_hashes(password) == hashed_text:
		return hashed_text
	return False

def create_user():
	c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT,password TEXT)')

def add_user(username,password):
	c.execute('INSERT INTO userstable(username,password) VALUES (?,?)',(username,password))
	conn.commit()

def login_user(username,password):
	c.execute('SELECT * FROM userstable WHERE username =? AND password = ?',(username,password))
	data = c.fetchall()
	return data



def main():
	if "res" not in st.session_state:
		st.session_state.user = st.sidebar.text_input("ユーザー名を入力してください")
		st.session_state.password = st.sidebar.text_input("パスワードを入力してください",type='password')
		button = st.sidebar.button("ログイン")
		if button:
			hashed_pswd = make_hashes(st.session_state.password)
			create_user()
			result = login_user(st.session_state.user,check_hashes(st.session_state.password,hashed_pswd))
			if result:
				st.success("{}さんでログインしています".format(st.session_state.user))
				st.session_state.res = result
				button2 = st.button("データを閲覧")
			else:
				st.warning("ユーザー名かパスワードが間違っています")
	else:
		mainapp()

if __name__ == '__main__':
	main()