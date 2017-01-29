from app import app
app.run(host=app.config['IP_ADDRESS'],debug=app.config['DEBUG'],port=app.config['PORT'])
