FROM ubuntu:22.04

# install rust and socat
RUN apt-get update && apt-get install -y curl socat build-essential 
RUN curl https://sh.rustup.rs -sSf | sh -s -- -y
ENV PATH="/root/.cargo/bin:${PATH}"

# Cargo.toml and Cargo.lock are copied first to cache dependencies
COPY Cargo.toml Cargo.lock /app/

RUN mkdir /app/src

# copy the source code
COPY maestro.rs /app/src/maestro.rs
COPY main.rs /app/src/main.rs

WORKDIR /app

# build the source code
RUN cargo build --release

# run the server
CMD socat TCP-LISTEN:1337,reuseaddr,fork EXEC:"target/release/maestro"
