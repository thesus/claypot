# claypot

A simple cooking recipe manager.


Install your javascript via `yarn`.


# Sample database

Use this command to load some sample data to your database.

```shell
$ ./manage.py loaddata ingredients_de.yaml units_de.yaml units_de_de.yaml test_recipes_de.yaml
```

# Running tests

````shell
$ pytest --cov=claypot
````

## Javascript setup

````
yarn
````

### Compile Javascript for development
```
yarn build --mode development --watch --dest ../claypot/contrib
```


### Compiles and minifies for production
```
yarn run build
```

### Lints and fixes files
```
yarn run lint
```

# Deployment

1. Generate sufficiently long random `DJANGO_SECRET_KEY` and `POSTGRES_PASSWORD`.
2. Create `.env`:

   ```env
   DJANGO_SECRET_KEY=quite-secret
   POSTGRES_PASSWORD=very-secret
   ```

3. Optional: Set `CLAYPOT_VERSION` environment variable to a specific versions Docker image tag. If you do not set a specific version, the compose file will default to `master` tagged image.

   ```shell
   $ export CLAYPOT_VERSION=1.0.0
   ```

4. Run Docker compose file:

   ```shell
   $ docker-compose up -d
   ```

5. Run database migrations:

   ```shell
   $ docker-compose run --rm claypot python manage.py migrate
   ```
