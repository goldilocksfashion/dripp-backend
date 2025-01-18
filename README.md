# Dripp AI backend
P2P Social Network focussed on fashion.

```
  graph TD
    subgraph "Post Creation & Distribution"
        A[Peer A Poster] -->|1. Store Locally| A1[Local Cache]
        A -->|2. Share CID| D[AI Bot Super Peer]
        A -->|2. Share CID| B[Peer B Online]
        D -->|3. Process & Score| D1[AI Processing]
    end

    subgraph "Content Replication"
        B -->|4. Fetch via QUIC| A
        B -->|5. Store Post| B1[Local Cache]
        D -->|Store Temporarily| D2[Temp Storage]
    end

    subgraph "Offline Peer Sync"
        C[Peer C Offline] -.->|6. Come Online| B
        C -.->|7. Get Updates| D
        C -.->|8. Fetch Posts| D
        C -.->|9. Local Storage| C1[Local Cache]
    end

    subgraph "Media Handling"
        A -->|QUIC Streaming| B
        B -->|QUIC Streaming| D
        D -->|QUIC Streaming| C
    end

    style D fill:#f9f,stroke:#333,stroke-width:4px
    style A fill:#bbf,stroke:#333
    style B fill:#bbf,stroke:#333
    style C fill:#ddd,stroke:#333
```