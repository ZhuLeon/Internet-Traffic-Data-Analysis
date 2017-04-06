Dear Reader, there are some issues with encoding in log.txt

When reading the file with encoding set to `utf-8`, it will read up to line 27617  
```with open(sys.argv[1], encoding="utf-8") as inlog:```

When reading the file with encoding set to `windows-1252`, it will read up to line 2401515  
`with open(sys.argv[1], encoding="windows-1252") as inlog:`

When reading the file with `errors="ignore"`, it complete successfully  
`with open(sys.argv[1], encoding="utf-8", errors="ignore") as inlog:`
