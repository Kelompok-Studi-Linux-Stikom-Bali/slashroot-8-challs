FROM ubuntu:20.04

RUN apt-get update && apt-get install -y xinetd && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* /etc/xinetd.d/*
RUN useradd -U -m babypwn && mkdir -p /home/babypwn
RUN chown -R root:babypwn /home/babypwn && chmod 750 /home/babypwn

CMD /home/babypwn/startchall
