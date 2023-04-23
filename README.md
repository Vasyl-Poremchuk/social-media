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

### Heroku deployment.

If you want to deploy this application on **Heroku**, follow the steps below:

- Sing in to your Heroku account or sign up using this [LINK](https://www.heroku.com).
- Install the Heroku Command Line Interface (CLI) from this [LINK](https://devcenter.heroku.com/articles/getting-started-with-python#set-up).

**NOTE**: Before installing the CLI, I strongly recommend that you close the IDE and any open terminals. This can save you from possible problems in the future.
- Use the command below to log in to the Heroku CLI.
```shell
heroku login
```
- Then fill in you credentials in the tab that opens in your browser.
- Create an app on Heroku using the command below.
```shell
heroku create <unique_name_of_your_app>
```
- Create a Procfile with a command that run our application on Heroku, you can use the command below.
```shell
web: uvicorn src.main:app --host=0.0.0.0 --port=${PORT:-5000}
```
**NOTE**: The Procfile is located at the root of the folder.
- Push your application on Heroku using the command below.
```shell
git push heroku master
```
- Create a PostgreSQL instance using the command below.
```shell
heroku addons:create heroku-postgresql:mini
```
**NOTE**: You can use any available PostgreSQL instance on Heroku.
- Add all necessary config variables on Heroku (App Dashboard -> Settings -> Config Vars -> Reveal Config Vars). You must add all the variables that exist in the **.env.sample** file on Heroku.
- Connect to the PostgreSQL instance using pgAdmin. Create a new instance in pgAdmin and fill in all the fields using the credentials available on Heroku (Datastores -> your_postgresql_instance -> Settings -> Database Credentials -> View Credentials).
- Update your Heroku PostgreSQL instance using the command below.
```shell
heroku run "alembic upgrade head"
```
- Restart the instance by running the following command.
```shell
heroku ps:restart
```
