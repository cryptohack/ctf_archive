1. Build:

   ```bash
   docker build -f Dockerfile_solution . -t invalid_endomorphism_curve_solution
   ```

2. Create folder cache and change rights

   ```bash
   mkdir -p temp_cache && chmod o+rw temp_cache
   ```

3. Run (you can change the number of CPUs and the website with port)

   ```bash
   docker run --cpus=16 --mount type=bind,source="$(pwd)/temp_cache",target=/home/crypto/cache -t invalid_endomorphism_curve_solution:latest python3 solve.py cryptotraining.zone 1354
   ```

​	4. You might need to run it again, it is flimsy. It will take a long time the first time it gets the flag. Cache will speed up computation the next time.
