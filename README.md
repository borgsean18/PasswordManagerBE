# READ ME


### How to modify schema locally

Install the golang-migrations tool : [Installation commands](https://github.com/golang-migrate/migrate/tree/master/cmd/migrate#download-pre-built-binary-windows-macos-or-linux)

Create a new migration:
```
migrate create -ext sql -dir migrate/db_migrations {title of update}
```

This will create empty up/down files.

Populate these files with idempotent schema modifications, UP will contain changes while
DOWN will undo them


apply new changes to your local/test DB: 
```
migrate -database {DATABASE_URL} -path ./db_migrations up
```
test if changes can be reversed:
```
migrate -database {DATABASE_URL} -path ./db_migrations down
```