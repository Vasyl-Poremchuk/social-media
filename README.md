## Social Media.

### Description.

The social media application provides users with the ability to create, modify, update, delete, and view a variety of posts.

### Installation.

**NOTE**: Python3 must be already installed.

```shell
git clone https://github.com/Vasyl-Poremchuk/social-media
cd social_media
python -m venv venv
venv\Scripts\activate (Windows) or sourse venv/bin/activate (Linux or macOS)
pip install -r requirements.txt
```

**NOTE**: Before running the application, you must create an **.env** file and fill it using the template in the **.env.sample** file.

### Running the application on the local machine.

```shell
uvicorn src.main:app --reload
```

### Running the application via the docker container.

If you want to run the development version of the docker container, use the command below:

```shell
docker-compse -f docker-compose-dev.yml up -d
```

If you want to run the production version of the docker container, use the command below:

```shell
docker-compose -f docker-compose-prod.yml up -d
```

### Swagger documentation.

The social media app has several endpoints available, which you can check out in the swagger documentation (use **/docs** to check).

![swagger](demo/images/swagger_docs.png)

### Heroku deployment.

Check it out: [LINK](https://social-media-fastapi-app.herokuapp.com/docs).
