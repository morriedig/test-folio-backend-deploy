# folio-backend

### Docker virtual environment
```
docker-compose build # 建立 Django Image
docker-compose up # run server
docker-compose run --rm web sh -c "python manage.py makemigrations" # 進到 Django container 執行指令
```
### 如何進到 psql ?
1. 輸入 `docker ps -a` 確認 db 的 container 有在 run。
    ![](docs/docker-readme/ps-a.png)

2. 進到 db container 的 shell
    ```shell
    $ docker exec -it folio-tmp_db_1 /bin/sh # db image name may be different
    ```
3. 進到 psql，會要你輸入密碼：範例是 secret1234
    ```
    / # psql -d folio -U root -W
    ```
4. 再看看 public 底下的 Django tables 應該都匯入了。
    ```
    folio=# \dt public.*
    ```
5. 輸入 `quit` 離開 psql 並按 `ctrl+D` 離開 db container 的 shell
    ![](docs/docker-readme/psql.png)


### Enable pre-commit hooks
```
pre-commit install
pre-commit install -t pre-push
pre-commit install -t commit-msg
```
## deploy to Heroku

```shell=
# Add the heroku remote repo(do it once)
heroku git:remote -a folio-backend-staging
heroku container:push web
heroku container:release web
```
