# CLI Contract: prospect-agent

## Command

`prospect-agent --input <csv> --output <dir> [--date-start <YYYY-MM-DD>] [--date-end <YYYY-MM-DD>] [--sample <n>]`

## Input
- CSV with columns: `First Name,Last Name,URL,Email Address,Company,Position,Connected On`

## Output
- Write CSV to output directory with columns: original columns + `generated_message`, `confidence`, `source_summary`, `processed_at`

## Exit codes
- `0` success
- `1` invalid input/path
- `2` runtime error (see logs)

## Errors
- Error responses (CLI prints machine-readable JSON to stderr when `--json-errors` flag set):

```
{ "error_code": "INVALID_CSV", "message": "Missing required column: First Name" }
```


