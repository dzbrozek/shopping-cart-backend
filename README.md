## Shopping cart

Simple REST API for shopping cart implemented in Django & DRF. For frontend part visit [shopping-cart-frontend](https://github.com/dzbrozek/shopping-cart-frontend)



[![codecov](https://codecov.io/gh/dzbrozek/shopping-cart-backend/branch/master/graph/badge.svg)](https://codecov.io/gh/dzbrozek/shopping-cart-backend)


### Running

#### Requirements

This app is using Docker so make sure you have both: [Docker](https://docs.docker.com/install/)
and [Docker Compose](https://docs.docker.com/compose/install/)

#### Bootstrap

To bootstrap the app move to the app directory and call

```
make build
make bootstrap
```


Once it's done the app should be up app and running. You can verify that visiting [http://127.0.0.1:8000/](http://127.0.0.1:8000/).

#### Running

Next time you want to start or stop the the app use `up` or `down` command.

```
make up
```

```
make down
```

#### Users

Test users created during bootstrapping the project.

| Login          | Password | Role  |
|----------------|----------|-------|
| admin@test.com | password | admin |
| user@test.com  | password | user  |

### Tests

To run the tests use `make test` command

### Features

* Adding/Removing products to/from basket
* Adding/Removing product by admins
* Sharing basket by email
* Sending email with list of updated baskets to admins (triggered by `cart_changes` command)
