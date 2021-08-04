RUN command -v ssh-agent >/dev/null || ( apt-get update -y && apt-get install openssh-client -y )'
RUN eval $(ssh-agent -s)
RUN echo "$SSH_PRIVATE_KEY" | tr -d '\r' | ssh-add -
RUN mkdir -p ~/.ssh
RUN chmod 700 ~/.ssh
RUN git config --global user.email "boro@inuits.eu"
RUN git config --global user.name "inuits"
