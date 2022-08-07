# CryptoHack CTF Archive

There are so many CTFs these days and CTFs often have cool cryptography challenges. This repo contains past CTF cryptography challenges that are so good we want to host them permanently.

You can play the challenges at [CryptoHack.org CTF Archive category](https://cryptohack.org/challenges/ctf-archive/).

## License

Please be aware that all challenges submitted to this repository are released under the terms of the MIT license. Challenges will appear on CryptoHack with credit given to the author and the original CTF the challenge came from.

## Submission

We want to see great cryptography challenges submitted to this repository. To submit a challenge, all you need to do is open a pull request that adds a directory to this repo that respects the following formats:

### Static Challenge

To submit a static challenge to the archive, you must use the following directory structure:

```
your_challenge
├── description.yml
├── release_files
│   ├── your_files.py
│   └── go_in_here.sage
```

 - `description.yml`
   - Data in `description.yml` is used to set metadata for the challenge
   - Please ensure to **base64 encode** your flag
 - `release_files/YOUR_CHALLENGE_FILES`
   - All files within `release_files` will be made available to the players of your challenge

For an example of a static challenge to copy, see: [ICC Athens: Unbalanced](https://github.com/cryptohack/ctf-archive/tree/main/icc2022_unbalanced). 


### Dynamic Challenge

To submit a dynamic challenge to the archive, you must use the following directory structure:

```
your_challenge
├── description.yml
├── server_files
│   ├── secret_server_file.py
|   ├── public_file.py
│   └── Dockerfile
├── release_files
│   ├── public_file.py@ -> server_files/public_file.py
│   └── maybe_another_one.py@ -> server_files/maybe_another_one.py
```

 - `description.yml`
   - Data in this file is used to set the metadata for the challenge
   - Please ensure to **base64 encode** your flag
   - Please pick a **random port** between 1024-65535 - to generate a random port, you can run the file `random_port.py`.
 - `Dockerfile`
   - All dynamic challenges must be built from a Dockerfile. `socat` or `xinetd` can be used to bind a challenge file to a port.
   - For the Dockerfile base image, please use a specific version not latest, e.g. use `ubuntu:22.04` not `ubuntu:latest` - this ensures the challenge will still work in the future.
   - Ensure the port the challenge is run on matches the port specified in the `description.yml`.
   - The flag within `description.yml` is decoded and set as the environment variable `FLAG` within the container automatically. So you can load the flag using `flag = os.environ["FLAG"]` instead of importing a file.
 - `server_files/YOUR_CHALLENGE_FILES`
   - The files in `server_files` will be hosted within a Docker container
 - `release_files/YOUR_CHALLENGE_FILES`
   - All files within `release_files` will be those which you want shared with the players
   - Files in this directory which are also on the server-side should be symlinked

For an example of a dynamic challenge to copy, see: [ICC Athens: ed25519](https://github.com/cryptohack/ctf-archive/tree/main/icc2022_ed25519-magic).
