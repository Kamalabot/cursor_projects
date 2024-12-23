use chrono::Utc;
use log::{error, info, warn};
use serde::Serialize;
use std::sync::Arc;
use tokio::io::{AsyncReadExt, AsyncWriteExt};
use tokio::net::TcpListener;
use tokio::sync::Mutex;

#[derive(Serialize)]
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

impl Honeypot {
    fn new() -> Self {
        Honeypot {
            state: Arc::new(Mutex::new(HoneypotState {
                connection_count: 0,
            })),
        }
    }

    async fn start(&self, port: u16) -> Result<(), Box<dyn std::error::Error>> {
        let listener = TcpListener::bind(("0.0.0.0", port)).await?;
        info!("Honeypot listening on port {}", port);

        loop {
            match listener.accept().await {
                Ok((mut socket, addr)) => {
                    let state = Arc::clone(&self.state);
                    
                    tokio::spawn(async move {
                        let mut state = state.lock().await;
                        state.connection_count += 1;
                        let conn_count = state.connection_count;
                        drop(state);

                        info!("New connection from: {} (Total: {})", addr, conn_count);

                        let mut buffer = [0; 1024];
                        let mut received_data = String::new();

                        // Fake SSH banner
                        let banner = "SSH-2.0-OpenSSH_8.2p1 Ubuntu-4ubuntu0.5\r\n";
                        if let Err(e) = socket.write_all(banner.as_bytes()).await {
                            error!("Failed to send banner: {}", e);
                            return;
                        }

                        // Read incoming data
                        match socket.read(&mut buffer).await {
                            Ok(n) if n > 0 => {
                                received_data = String::from_utf8_lossy(&buffer[..n]).to_string();
                                warn!("Received data from {}: {}", addr, received_data);
                            }
                            Ok(_) => info!("Connection closed by client: {}", addr),
                            Err(e) => error!("Failed to read from socket: {}", e),
                        }

                        // Log the connection
                        let log = ConnectionLog {
                            timestamp: Utc::now().to_rfc3339(),
                            ip_address: addr.ip().to_string(),
                            port: addr.port(),
                            data: received_data,
                        };

                        // Write to log file
                        if let Ok(log_str) = serde_json::to_string(&log) {
                            tokio::fs::OpenOptions::new()
                                .create(true)
                                .append(true)
                                .open("/var/log/honeypot.log")
                                .await
                                .map(|mut file| {
                                    tokio::spawn(async move {
                                        if let Err(e) = file.write_all(format!("{}\n", log_str).as_bytes()).await {
                                            error!("Failed to write to log file: {}", e);
                                        }
                                    });
                                })
                                .unwrap_or_else(|e| error!("Failed to open log file: {}", e));
                        }
                    });
                }
                Err(e) => error!("Failed to accept connection: {}", e),
            }
        }
    }
}

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    // Initialize logger
    env_logger::init();

    let honeypot = Honeypot::new();
    
    // Start multiple listeners for different services
    let ports = vec![22, 23, 80, 443, 3306, 5432];
    
    let handles: Vec<_> = ports
        .into_iter()
        .map(|port| {
            let honeypot = Honeypot::new();
            tokio::spawn(async move {
                if let Err(e) = honeypot.start(port).await {
                    error!("Honeypot on port {} failed: {}", port, e);
                }
            })
        })
        .collect();

    // Wait for all honeypot instances
    for handle in handles {
        handle.await?;
    }

    Ok(())
} 