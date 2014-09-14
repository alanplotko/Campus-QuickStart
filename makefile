all:
	git add .
	git commit -m "templates"
	git push heroku master
ea:
	foreman start; ps -fA | grep python;
