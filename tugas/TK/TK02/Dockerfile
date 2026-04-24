FROM ubuntu:20.04

# Install necessary packages
RUN apt-get update && apt-get install -y \
    socat \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy source and flag
COPY kantin.c flag.txt ./

# Compile inside the container so libc matches
RUN gcc -o kantin kantin.c -fno-stack-protector -z execstack -no-pie -m64 \
    && chmod +x kantin

# Create run script (ONLY ONCE, with PTY)
RUN echo '#!/bin/bash\n\
    socat TCP-LISTEN:1337,reuseaddr,fork EXEC:"./kantin"' > run.sh \
    && chmod +x run.sh

# Expose port
EXPOSE 1337

# Run server
CMD ["./run.sh"]