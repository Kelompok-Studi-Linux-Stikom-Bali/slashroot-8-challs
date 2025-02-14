FROM alpine:latest AS build

FROM pwn.red/jail
COPY --from=build --chmod=755 / /srv

COPY --chmod=755 chall /srv/app/run
COPY --chmod=755 execute_me /srv/execute_me

ENV JAIL_MEM=20M
