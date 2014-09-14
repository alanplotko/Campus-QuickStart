all:
	git add .
	git commit -m "zip/tar work"
	git push heroku master
ea:
	foreman start; ps -fA | grep python;
