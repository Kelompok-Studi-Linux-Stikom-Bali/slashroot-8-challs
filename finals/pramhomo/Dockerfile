FROM ubuntu:20.04

RUN apt-get update && apt-get install -y xinetd && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* /etc/xinetd.d/*
RUN useradd -U -m pramhomo && mkdir -p /home/pramhomo
RUN chown -R root:pramhomo /home/pramhomo && chmod 750 /home/pramhomo

CMD /home/pramhomo/startchall
