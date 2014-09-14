all:
	git add .
	git commit -m "About"
	git push heroku master
ea:
	foreman start; ps -fA | grep python;
