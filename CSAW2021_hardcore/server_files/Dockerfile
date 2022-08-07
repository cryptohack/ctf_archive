FROM rust:slim-buster as builder
WORKDIR /app
COPY Cargo.toml Cargo.lock /app/
COPY src/lib.rs src/main.rs /app/src/
RUN apt-get -y update && apt-get -y install build-essential m4 && cargo build --release

FROM debian:buster-slim
RUN apt-get -y update && apt-get -y install xinetd
RUN useradd ctf
WORKDIR /app
COPY --from=builder /app/target/release/hardcore /app/
COPY hardcore.xinetd /etc/xinetd.d/hardcore
RUN chown -R ctf /app

CMD xinetd -dontfork
