FROM ubuntu:24.04
ENV DEBIAN_FRONTEND=noninteractive

RUN apt update && apt install xinetd qemu-user qemu-user-static -y
RUN groupadd -r ctf && useradd -r -g ctf ctf

WORKDIR /home/ctf

COPY main .
COPY libc.so.6 .
COPY ld-2.31.so .
COPY flag .

RUN echo '#!/bin/bash\nservice xinetd restart && /bin/sleep infinity' > /etc/init.sh
RUN echo 'service ctf\n\ 
{\n\ 
    disable = no\n\ 
    socket_type = stream\n\ 
    protocol = tcp\n\ 
    wait = no\n\ 
    user = ctf\n\ 
    type = UNLISTED\n\ 
    port = 8000\n\ 
    bind = 0.0.0.0\n\ 
    server = /home/ctf/run\n\ 
}' > /etc/xinetd.d/ctf
RUN echo '#!/bin/bash\ncd /home/ctf && qemu-aarch64 ./main' > /home/ctf/run

RUN chmod 400 /etc/xinetd.d/ctf
RUN chmod 550 /home/ctf/main /home/ctf/run /etc/init.sh

RUN chown -R root:ctf /home/ctf
RUN service xinetd restart
