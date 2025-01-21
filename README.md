# Dripp AI backend
P2P Social Network focussed on fashion.


# Flows

## Identity / cloudless DID based

1. Group Creation Flow (from identity perspective)
```mermaid
graph TD
    A[User Creates Group] -->|Generate| B[Group Genesis Block]
    B -->|Contains| C[Admin DID + Keys]
    B --> D[Group Settings]
    
    E[New User] -->|Request Join| F[Create Local DID]
    F -->|Generate| G[KeyPair]
    F -->|Store| H[Local Chain]
    
    G -->|Sign| I[Join Request]
    I -->|Via Iroh| J[Group Admin]
    
    J -->|Verify| K[Phone + DID]
    K -->|If Approved| L[Member Block]
    L -->|Sync via Iroh| M[All Group Members]
    
    M -->|Each Member| N[Verify Member Block]
    N -->|If Valid| O[Update Local Chain]
```

2. Request to join groups flow (DID)
```mermaid
graph TD
    subgraph "User Side: Join Request"
        A[User Requests Join] -->|1| B[Generate DID/KeyPair]
        B -->|2| C[Store in Local Chain]
        C -->|3| D[Create Join Request]
        D -->|4| E[Sign with New DID]
    end

    subgraph "Admin Side: Verification"
        E -->|5| F[Admin Receives Request]
        F -->|6| G[Verify Phone Number]
        G -->|7| H[Create Verification Block]
        H -->|8| I[Sign with Admin DID]
        I -->|9| J[Add to Group Chain]
    end

    subgraph "Peer Side: Member Acceptance"
        J -->|10| K[Peers Receive Block]
        K -->|11| L[Verify Admin Signature]
        L -->|12| M[Verify DID Structure]
        M -->|13| N[Verify Phone Proof]
        N -->|14| O[Add to Members List]
    end

    J -->|via Iroh| K
    O -->|15| P[Update Local Chain]
```
3. Post creation and verification flow
```mermaid
graph TD
    subgraph "Post Creation"
        A[User Creates Post] -->|Store| B[Local SQLite]
        A -->|Get Identity| C[Local Blockchain]
        C -->|Sign with DID| D[Create Signature]
        D -->|Attach to| E[Post Metadata]
    end

    subgraph "Sync Process"
        E -->|Announce via Iroh| F[Group Peers]
        F -->|Each Peer| G{Verify Signature}
        G -->|Valid| H[Check Local Chain]
        H -->|Verify Membership| I{Vote}
        
        I -->|>50% Yes| J[Pin Content]
        I -->|<50%| K[Remain Unpinned]
        
        J -->|Store| L[Peer's SQLite]
    end

    subgraph "Storage Structure"
        M[SQLite] --> N[Posts]
        M --> O[Comments]
        M --> P[Likes/Dislikes]
        
        Q[Blockchain] --> R[Identity Only]
        Q --> S[Membership Proof]
    end

```
4. Interactions (Like/Comment) Flow: (DID perspective)
```mermaid
graph TD
    A[User Interaction] -->|Create| B[Interaction Block]
    
    subgraph "Interaction Creation"
        B -->|Include| C[Original Post CID]
        B -->|Sign with| D[User DID]
        B -->|Add| E[Timestamp]
    end
    
    E -->|Store| F[Local Chain]
    E -->|Share via Iroh| G[Group Members]
    
    subgraph "Peer Processing"
        G -->|Verify| H[Author DID]
        H -->|Check| I[Group Membership]
        I -->|Verify| J[Original Post Exists]
        J -->|If Valid| K[Add to Chain]
    end
```

## Non-Identity flows (actual data)
### Group creation flow:

```mermaid
graph TD
    A[Flutter UI] -->|FFI| B[Rust Backend]
    B -->|1. Create| C[Local SQLLite]
    B -->|2. Generate| D[Group Keys]
    B -->|3. Iroh Announce| E[P2P Network]
    B -->|4. Backup| F[AI Bot/S3]
    
    C -->|Store| G[Group Metadata]
    C -->|Store| H[Member List]
    C -->|Store| I[Permissions]
    
    E -->|Sync| J[Online Peers]
    J -->|Store| K[Their SQLLite]
    
    F -->|Backup| L[Persistent Storage]
```

2A. Only OP online (everyone in group offline)

```mermaid
graph TD
    A[Flutter UI] -->|FFI| B[Rust Backend]
    B -->|Create| C[Local SQLLite]
    B -->|Generate Group Keys| D[Group Keys]
    B -->|Announce to P2P| E[P2P Network]
    B -->|Backup Data| F[AI Bot/S3]    
    C -->|Store Metadata| G[Group Metadata]
    C -->|Store Member List| H[Member List]
    C -->|Store Permissions| I[Permissions]
    E -->|Sync with Peers| J[Online Peers]
    J -->|Store Data| K[Their SQLLite]    
    F -->|Backup to Persistent| L[Persistent Storage]
```

2B All online

```mermaid
graph TD
    A[Post Content] -->|FFI| B[Rust Backend]
    B -->|1. Store| C[Local SQLLite]
    B -->|2. Iroh Share| D[P2P Network]
    
    D -->|Sync| E[Online Peers]
    E -->|Store| F[Their SQLLite]
    
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
    B -->|1. Store| C[Local SQLLite]
    B -->|2. Iroh Share| D[Online Peers]
    B -->|3. Backup| E[AI Bot]
    
    D -->|Sync| F[Their SQLLite]
    E -->|Store| G[S3 Storage]
    
    H[Offline Peers] -.->|Come Online| I[Sync Request]
    I -->|Get Updates| D
    I -->|Fallback| E

```

3 Interactions: Comments, likes, dislikes


```mermaid


graph TD
    A[User Interaction] -->|FFI| B[Rust Backend]
    B -->|1. Store| C[Local SQLLite]
    B -->|2. CRDT Update| D[Create Operation]
    
    D -->|Iroh Share| E[P2P Network]
    D -->|Backup| F[AI Bot]
    
    subgraph "CRDT Resolution"
        G[Merge Operations] -->|Apply| H[Local State]
        G -->|Resolve| I[Conflicts]
        I -->|Update| J[Vector Clock]
    end
    
    E -->|Sync| K[Online Peers]
    K -->|Update| L[Their SQLLite]

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
- SQLLite per group
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
    H -->|6. Update| I[Local SQLLite]
```

## Backup node AI Bot flow

```mermaid
 graph TD
    A[Peer Online] -->|1. No Peers Found| B[Contact Bot]
    B -->|2. Send State| C[Bot Compares]
    
    C -->|3a. Missing Local| D[Get Updates]
    C -->|3b. Missing Remote| E[Send Updates]
    
    D -->|4. Apply| F[Local SQLLite]
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
