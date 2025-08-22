pybabel extract -F babel.cfg -k _ -o to_translate.pot ..

pybabel update -i to_translate.pot -d . -l fr # For French language, change fr by the two letter of your own language you want to update

pybabel compile -d .