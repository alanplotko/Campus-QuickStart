all:
	git add .
	git commit -m "LoginPage"
	git push heroku master
ea:
	foreman start; ps -fA | grep python;
