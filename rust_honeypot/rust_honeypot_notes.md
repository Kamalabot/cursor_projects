# Rust Honeypot Project Notes

## Architecture
- **Honeypot Type**: Custom Rust-based honeypot
- **Deployment Environment**: Oracle VM (Always-on)
- **Target Architecture**: x86_64 (or ARM, depending on your VM)

## Required Packages
1. **Rust Toolchain**
   - Install Rust using `rustup`:
     ```bash
     curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
     ```
   - Ensure you have the latest stable version:
     ```bash
     rustup update stable
     ```

2. **Cross-Compilation Tools**
   - For cross-compiling, you may need additional target architectures:
     ```bash
     rustup target add x86_64-unknown-linux-gnu
     ```

3. **Dependencies**
   - Include necessary crates in your `Cargo.toml`:
     ```toml
     [dependencies]
     tokio = { version = "1", features = ["full"] }
     log = "0.4"
     env_logger = "0.9"
     ```

## Setup Instructions
1. **Local Development**
   - Clone the repository:
     ```bash
     git clone <your-repo-url>
     cd <your-repo-directory>
     ```
   - Build the project:
     ```bash
     cargo build --release
     ```

2. **Cross-Compile for Deployment**
   - Use the following command to cross-compile:
     ```bash
     cargo build --target=x86_64-unknown-linux-gnu --release
     ```

3. **Deploying to Oracle VM**
   - Use `scp` or any other file transfer method to upload the compiled binary to your Oracle VM:
     ```bash
     scp target/x86_64-unknown-linux-gnu/release/your_honeypot_binary user@your_vm_ip:/path/to/deploy/
     ```

4. **Running the Honeypot**
   - SSH into your Oracle VM and run the honeypot:
     ```bash
     ssh user@your_vm_ip
     cd /path/to/deploy/
     ./your_honeypot_binary
     ```

## Additional Notes
- Ensure your Oracle VM has the necessary firewall rules to allow traffic to your honeypot.
- Monitor logs and performance to adjust configurations as needed.

## Systemd Setup and Monitoring

1. **Install Service File**
   ```bash
   # Copy the honeypot binary to the system directory
   sudo cp target/release/rust_honeypot /usr/local/bin/
   sudo chmod +x /usr/local/bin/rust_honeypot

   # Copy the service file to systemd directory
   sudo cp rust_honeypot.service /etc/systemd/system/
   sudo chmod 644 /etc/systemd/system/rust_honeypot.service
   ```

2. **Create Log Files**
   ```bash
   sudo touch /var/log/honeypot.log
   sudo touch /var/log/honeypot.error.log
   sudo chmod 644 /var/log/honeypot.log
   sudo chmod 644 /var/log/honeypot.error.log
   ```

3. **Enable and Start Service**
   ```bash
   # Reload systemd to recognize new service
   sudo systemctl daemon-reload

   # Enable service to start on boot
   sudo systemctl enable rust_honeypot

   # Start the service
   sudo systemctl start rust_honeypot
   ```

4. **Monitoring Commands**
   ```bash
   # Check service status
   sudo systemctl status rust_honeypot

   # View real-time logs
   sudo journalctl -u rust_honeypot -f

   # View service logs
   sudo tail -f /var/log/honeypot.log
   sudo tail -f /var/log/honeypot.error.log

   # Restart service if needed
   sudo systemctl restart rust_honeypot

   # Stop service
   sudo systemctl stop rust_honeypot
   ```

5. **Troubleshooting**
   ```bash
   # Check for any systemd errors
   sudo journalctl -xe

   # Check service configuration
   sudo systemctl show rust_honeypot

   # Verify service file syntax
   sudo systemd-analyze verify /etc/systemd/system/rust_honeypot.service
   ```

## Important Notes
- The service runs as root for access to lower-level ports
- Logs are stored in `/var/log/honeypot.log` and `/var/log/honeypot.error.log`
- Service automatically restarts after 3 seconds if it crashes
- Monitor system resources:
  ```bash
  # Check CPU and memory usage
  top -p $(pgrep rust_honeypot)
  
  # Check open ports
  sudo lsof -i -P -n | grep rust_honeypot
  ```

## Implementation Details

### Core Components
1. **Main Structures**
   - `ConnectionLog`: Serializable struct for logging connection details
   - `HoneypotState`: Tracks connection statistics
   - `Honeypot`: Main service implementation with async functionality

2. **Features**
   - Multi-port monitoring (22, 23, 80, 443, 3306, 5432)
   - Async I/O using Tokio
   - JSON-formatted logging
   - Thread-safe state management
   - Service emulation (currently SSH)
   - Concurrent connection handling

3. **Monitored Ports**
   - 22 (SSH)
   - 23 (Telnet)
   - 80 (HTTP)
   - 443 (HTTPS)
   - 3306 (MySQL)
   - 5432 (PostgreSQL)

### Code Structure
```rust
// Main structures
struct ConnectionLog {
    timestamp: String,
    ip_address: String,
    port: u16,
    data: String,
}

struct HoneypotState {
    connection_count: u64,
}

struct Honeypot {
    state: Arc<Mutex<HoneypotState>>,
}
```

### Logging Format
The honeypot logs connections in JSON format:
```json
{
    "timestamp": "2024-XX-XX:XX:XX:XXZ",
    "ip_address": "X.X.X.X",
    "port": XXXX,
    "data": "received data"
}
```

### Dependencies
```toml
[dependencies]
tokio = { version = "1.28", features = ["full"] }
chrono = "0.4"
serde = { version = "1.0", features = ["derive"] }
serde_json = "1.0"
log = "0.4"
env_logger = "0.10"
async-trait = "0.1"
sqlx = { version = "0.7", features = ["runtime-tokio-native-tls", "sqlite"] }
```

## Development Roadmap

### Current Implementation
- [x] Basic TCP listener setup
- [x] Multi-port monitoring
- [x] JSON logging system
- [x] SSH service emulation
- [x] Connection tracking
- [x] Async operation

### Planned Features
1. **Service Emulation**
   - [ ] HTTP/HTTPS server responses
   - [ ] FTP service emulation
   - [ ] Telnet interaction
   - [ ] Database service emulation

2. **Monitoring & Analysis**
   - [ ] Real-time attack pattern detection
   - [ ] IP geolocation tracking
   - [ ] Statistical analysis of attacks
   - [ ] Web dashboard for monitoring

3. **Security Features**
   - [ ] Rate limiting
   - [ ] IP blacklisting
   - [ ] Attack signature detection
   - [ ] Automated reporting

4. **Data Storage**
   - [ ] SQLite integration
   - [ ] Attack pattern database
   - [ ] Long-term statistics storage

## Building and Running

1. **Development Build**
   ```bash
   cargo build
   ```

2. **Production Build**
   ```bash
   cargo build --release
   ```

3. **Running with Logging**
   ```bash
   RUST_LOG=info ./target/release/rust_honeypot
   ```

## Monitoring Tips

1. **View Live Logs**
   ```bash
   tail -f /var/log/honeypot.log | jq '.'
   ```

2. **Check Active Ports**
   ```bash
   sudo netstat -tulpn | grep rust_honeypot
   ```

3. **Monitor System Resource Usage**
   ```bash
   top -p $(pgrep rust_honeypot)
   ```

## Security Considerations
- The honeypot runs as root to bind to privileged ports
- All connections are logged with timestamps and source IPs
- The service emulates vulnerable services but is not actually vulnerable
- Monitor system resources as concurrent connections can impact performance

## Backup and Maintenance
1. **Log Rotation**
   - Configure logrotate for `/var/log/honeypot.log`
   - Keep logs for analysis and pattern recognition

2. **Regular Updates**
   - Update dependencies monthly
   - Check for security advisories
   - Monitor system performance

3. **Data Analysis**
   - Regular backup of logs
   - Analyze attack patterns
   - Update emulated services based on trends

   Yes, there are alternatives to `TcpListener` in Rust, especially when working with asynchronous networking. Here are a few options you might consider:

1. **`UdpSocket`**: If you want to handle UDP connections instead of TCP, you can use `UdpSocket`. This is useful for applications that do not require a connection-oriented protocol.

2. **`UnixListener`**: If you're working in a Unix-like environment and want to use Unix domain sockets, you can use `UnixListener`. This is suitable for inter-process communication on the same machine.

3. **`HttpServer` from `warp` or `actix-web`**: If you're building a web server, you might consider using higher-level abstractions like `warp` or `actix-web`, which provide more features and easier handling of HTTP requests.

4. **`tokio-tungstenite`**: If you're looking to handle WebSocket connections, you can use `tokio-tungstenite`, which provides an easy way to work with WebSockets in an asynchronous context.

If you want to see how to implement one of these alternatives in your existing code, please let me know!
