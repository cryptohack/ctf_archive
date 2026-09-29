FROM rust:1.96-slim-bookworm AS build
WORKDIR /app
COPY Cargo.toml Cargo.lock ./
COPY maestro.rs main.rs src/
RUN cargo build --release

FROM ctf-archive/python-base:3.12
COPY --from=build /app/target/release/maestro ./
USER ctf
CMD ["socat", "TCP-LISTEN:1337,reuseaddr,fork", "EXEC:./maestro"]
