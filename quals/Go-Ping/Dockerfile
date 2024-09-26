ARG GO_VERSION=1.22
ARG ALPINE_VERSION=3.20

# build-stage

FROM golang:${GO_VERSION}-alpine${ALPINE_VERSION} as build-stage

WORKDIR /app

COPY go.mod .
COPY go.sum .

RUN go mod download

COPY . .

RUN go build -o main .

# roduction-stage

FROM alpine:${ALPINE_VERSION} as production-stage

RUN addgroup appgroup && adduser --disabled-password --no-create-home appuser -G appgroup

RUN chmod 1733 /tmp /var/tmp /dev/shm

RUN echo "slashroot8{Rc3_W1Th_c0mM4Nd_1Nj3cT1On_1S V3Ry_v3rY_N1Ce}" > /flag_$(cat /dev/urandom | tr -dc "a-zA-Z0-9" | fold -w 16 | head -n 1).txt

WORKDIR /app

COPY --from=build-stage /app/main ./main

COPY --from=build-stage /app/template ./template

RUN chmod +x ./main

USER appuser

CMD ./main
