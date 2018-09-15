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
