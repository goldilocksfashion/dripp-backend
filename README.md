# Dripp AI backend
P2P Social Network focussed on fashion.

## Basic Flows

### Group creation flow:

```mermaid
graph TD
    A[Flutter UI] -->|FFI| B[Rust Backend]
    B -->|1. Create| C[Local RocksDB]
    B -->|2. Generate| D[Group Keys]
    B -->|3. Iroh Announce| E[P2P Network]
    B -->|4. Backup| F[AI Bot/S3]
    
    C -->|Store| G[Group Metadata]
    C -->|Store| H[Member List]
    C -->|Store| I[Permissions]
    
    E -->|Sync| J[Online Peers]
    J -->|Store| K[Their RocksDB]
    
    F -->|Backup| L[Persistent Storage]
```

2A. Only OP online (everyone in group offline)

```mermaid
graph TD
    A[Post Content] -->|FFI| B[Rust Backend]
    B -->|1. Store| C[Local RocksDB]
    B -->|2. Generate| D[Content CID]
    B -->|3. Try Iroh| E[No Peers]
    B -->|4. Backup| F[AI Bot]
    
    F -->|Store| G[S3 Backup]
    F -->|Queue| H[Pending Distribution]
    
    I[OP Goes Offline] -.->|Later| J[Peers Come Online]
    J -->|Sync From| F
    J -->|Update| K[Their RocksDB]
```

2B All online

```mermaid
graph TD
    A[Post Content] -->|FFI| B[Rust Backend]
    B -->|1. Store| C[Local RocksDB]
    B -->|2. Iroh Share| D[P2P Network]
    
    D -->|Sync| E[Online Peers]
    E -->|Store| F[Their RocksDB]
    
    D -->|Backup| G[AI Bot]
    G -->|Archive| H[S3 Storage]
    
    subgraph "CRDT Handling"
        I[Vector Clock] -->|Update| J[Version Vector]
        J -->|Resolve| K[Conflicts]
    end

```
2C Posting Partial Online

```mermaid

graph TD
    A[Post Content] -->|FFI| B[Rust Backend]
    B -->|1. Store| C[Local RocksDB]
    B -->|2. Iroh Share| D[Online Peers]
    B -->|3. Backup| E[AI Bot]
    
    D -->|Sync| F[Their RocksDB]
    E -->|Store| G[S3 Storage]
    
    H[Offline Peers] -.->|Come Online| I[Sync Request]
    I -->|Get Updates| D
    I -->|Fallback| E

```

3 Interactions: Comments, likes, dislikes


```mermaid


graph TD
    A[User Interaction] -->|FFI| B[Rust Backend]
    B -->|1. Store| C[Local RocksDB]
    B -->|2. CRDT Update| D[Create Operation]
    
    D -->|Iroh Share| E[P2P Network]
    D -->|Backup| F[AI Bot]
    
    subgraph "CRDT Resolution"
        G[Merge Operations] -->|Apply| H[Local State]
        G -->|Resolve| I[Conflicts]
        I -->|Update| J[Vector Clock]
    end
    
    E -->|Sync| K[Online Peers]
    K -->|Update| L[Their RocksDB]

```

## Key Considerations for Implementation:

### CRDT Management:
- Use operation-based CRDTs for interactions
- Vector clocks for causality tracking
- Conflict resolution strategies


## FFI Layer:

```mermaid

graph TD
    A[Flutter/Dart] -->|FFI Bridge| B[Rust Backend]
    B -->|Platform Paths| C{OS Check}
    C -->|iOS| D[iOS Storage]
    C -->|Android| E[Android Storage]

```
## Storage Strategy forks
- RocksDB per group
- Platform-specific paths
- Efficient indexing


## Peer to Peer direct sync

```mermaid
graph TD
    A[Peer Comes Online] -->|1. Announce Presence| B[Iroh Network]
    B -->|2. Discover Peers| C[Get Peer List]
    C -->|3. For Each Peer| D[Request Vector Clock]
    D -->|4. Compare States| E{Need Updates?}
    
    E -->|Yes| F[Request Missing]
    E -->|No| G[Up to Date]
    
    F -->|5. Stream Updates| H[Apply CRDT Ops]
    H -->|6. Update| I[Local RocksDB]
```

## Backup node AI Bot flow

```mermaid
 graph TD
    A[Peer Online] -->|1. No Peers Found| B[Contact Bot]
    B -->|2. Send State| C[Bot Compares]
    
    C -->|3a. Missing Local| D[Get Updates]
    C -->|3b. Missing Remote| E[Send Updates]
    
    D -->|4. Apply| F[Local RocksDB]
    E -->|4. Store| G[Bot Storage]
    
    subgraph "Bot Validation"
        H[Check Permissions]
        I[Verify Group Keys]
        J[Validate Operations]
    end
```
## Mixed node sync

```mermaid
graph TD
    A[Need Sync] -->|1. Try Peers| B{Peers Available?}
    
    B -->|Yes| C[P2P Sync]
    B -->|Partial| D[Hybrid Sync]
    B -->|No| E[Bot Sync]
    
    C -->|Fast Path| F[Direct Updates]
    D -->|Split Sync| G[Get Some P2P]
    D --> H[Get Rest Bot]
    E -->|Slow Path| I[Full Bot Sync]
```

## key sync strategies
1. Priority order for sync

```mermaid
graph LR
    A[Sync Request] --> B{Try Local Network}
    B -->|Success| C[P2P Sync]
    B -->|Fail| D{Try Known Peers}
    D -->|Success| E[Remote P2P]
    D -->|Fail| F[Bot Sync]
```
## CRDT Update flow

```mermaid
graph TD
    A[New Operation] -->|1. Local| B[Apply Op]
    B -->|2. Update| C[Vector Clock]
    C -->|3. Broadcast| D[Available Peers]
    C -->|4. Backup| E[Bot Storage]
    
    D -->|5. Merge| F[Their State]
    F -->|6. Propagate| G[Other Peers]
```
## Recovery Scenarios

```mermaid
graph TD
    A[Peer Offline] -->|Comes Online| B[Check Last Sync]
    B -->|Get Updates| C{Sync Source}
    
    C -->|Fast| D[Local Peers]
    C -->|Medium| E[Remote Peers]
    C -->|Slow| F[Bot Backup]
    
    D -->|Merge| G[Local State]
    E -->|Merge| G
    F -->|Merge| G
```

## Confict Resolution

```mermaid
graph TD
    A[Detect Conflict] -->|Compare Vector Clocks| B{Conflict Type}
    
    B -->|Post Edit| C[Post Resolution]
    B -->|Comments| D[Comment Resolution]
    B -->|Likes/Dislikes| E[Counter Resolution]
    
    subgraph "Post Resolution"
        C -->|Compare Timestamps| C1[Latest Wins]
        C -->|Keep History| C2[Version Chain]
    end
    
    subgraph "Comment Resolution"
        D -->|Ordered Set| D1[Merge Comments]
        D -->|Update Refs| D2[Link to Post]
    end
    
    subgraph "Counter Resolution"
        E -->|Add Operation| E1[Combine Counts]
        E -->|De-duplicate| E2[User Actions]
    end
```
