Fast-Firex
======================

 A simple project template with fastapi, firebase database, pydantic. sutiable to small and medium web apps and micro services architecture. 

#### Services Included:
* RESTful API Design Strcutre with Intaractive API Docs.
* A Simple User jwt authentication system
* A Simple Blog articles model with crud.
* A Simple Docker File Attached to run the application.

#### Requirements:
* FastAPI -  to make rest api service
* Firebase-Admin - to store data into database
* Pydantic - to handle data models
* PyJwt - to Handle Jwt Authentication

#### To Run:
* Rename .env.example to .env and edit .env file
* Add your Google Service key path in .env file
* Install Requirements
```python
pip install -r requirements.txt
```
* Run Application
```python
python main.py 
(or)
uvicorn main:app --host=0.0.0.0 --port=8000
```
* If you use Docker, then just build a image and run it.
```conf
docker build --tag fastfirex .

docker run --name fastfirex -p 8000:8000 fastfirex
```
* Application Endpoints
```sh
127.0.0.1:8000/docs    - to Interactive API Docs and API Testing
```
#### Possible Services:
* we can run this service in firebase hosting easily with google cloud build service.
* we can also attach all other firebase service like firebase hosting, friebase realtiem database, firebase ML services, firebase Functions etc.

