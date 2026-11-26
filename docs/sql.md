# SQL

`run_sql_query` returns rows as dictionaries and never raises; on an AXL error it returns `num_rows: 0`
and stores the exception on `ucm.last_exception`. `sql_query` and `sql_update` return the raw AXL result
and raise `zeep.exceptions.Fault` on error.

```python
result = ucm.run_sql_query("select name, description from device")
for row in result.get("rows", []):
    print(row["name"], row["description"])

ucm.sql_update("update device set description = 'Lobby' where name = 'SEP001122334455'")
```

::: ciscoaxl.axl.axl
    options:
      members:
        - run_sql_query
        - sql_query
        - sql_update
      show_root_heading: false
      show_source: false
      heading_level: 3
