# Automail

*Use python to send emails about market liquidity automatically, just for fun*



### Setup

- set sender, password & receiver in mail.py 

- deploy it to heroku or sth. else 

  - install heroku CLI

  - ```shell
    heroku login
    ```

  - ```shell
    heroku git:clone -a your_heroku_repository_name
    cd your_heroku_repository_name
    ```

  - ```shell
    git add .
    git commit -am "make it better"
    git push heroku master
    ```

  - ```shell
    heroku ps:scale clock=1
    ```

    

