

## MONGO

From mongo shell, convert results to a valid json list of objects
```
> print(JSON.stringify(db.<collection>.find({...}).toArray()))
```
