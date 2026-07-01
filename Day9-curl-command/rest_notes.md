# Day 9 — HTTP, REST & Web Networking
## Commands Used Today

### 1. GET — Single post fetch
curl.exe https://jsonplaceholder.typicode.com/posts/1

Purpose: Oru specific post data fetch pannuvom
When to use: Data read pannanum na GET use pannuvom
Real world: User profile, product details fetch pannuvom

---

### 2. GET — Query params with filter
curl.exe "https://jsonplaceholder.typicode.com/posts?userId=1"

Purpose: Filter panni data fetch pannuvom
When to use: Search, filter, pagination pannanum na
Real world: "Show only my posts", "Filter by category"

---

### 3. POST — New data create
$body = '{"title": "my post", "body": "hello world", "userId": 1}'
curl.exe -X POST https://jsonplaceholder.typicode.com/posts \
  -H "Content-Type: application/json" \
  -d $body

Purpose: Server ku new data anuppi create pannuvom
When to use: Form submit, new record create pannanum na
Real world: Register new user, create new order
Response: Server id: 101 assign pannuchu — auto generated!

---

### 4. View Headers only
curl.exe -I https://jsonplaceholder.typicode.com/posts/1

Purpose: Response headers mattum paakanum — body vendam
When to use: Status code, content-type, cache check pannanum na
Real world: API debugging, performance check

Important headers seen:
- HTTP/1.1 200 OK      → Request successful
- Content-Type         → application/json (JSON data)
- Content-Length       → 292 bytes (response size)
- Cache-Control        → max-age=43200 (12 hours cache)
- X-Ratelimit-Limit    → 1000 (max requests allowed)
- X-Ratelimit-Remaining→ 999 (remaining requests)
- X-Powered-By         → Express (Node.js backend)
- Server               → cloudflare (CDN used)

---

### 5. Localhost connection test
curl.exe http://localhost:8000

Purpose: Local server running aa nu check pannuvom
Result today: "Could not connect" — because no server running yet
When it works: Day 14 la FastAPI build pannuvom, then same
             command run pannuvom — response varum!

---

### 6. Check open ports
netstat -an | findstr "LISTENING"

Purpose: Machine la endha ports currently open nu paakanum
When to use: Which services running, port conflict check
Today found:
- Port 5432 → PostgreSQL already installed! (Day 10 use aagum)
- Port 445  → Windows File Sharing
- Port 135  → Windows RPC service

---

## HTTP Methods Summary
| Method | Purpose        | Real example              |
|--------|---------------|---------------------------|
| GET    | Fetch data    | Load a webpage            |
| POST   | Create data   | Submit a form             |
| PUT    | Update data   | Edit your profile         |
| DELETE | Delete data   | Delete a tweet            |

---

## Status Codes Summary
| Code | Meaning      | When you see it           |
|------|-------------|---------------------------|
| 200  | OK           | Successful GET            |
| 201  | Created      | Successful POST           |
| 400  | Bad Request  | Wrong data sent           |
| 401  | Unauthorized | Wrong API key             |
| 404  | Not Found    | Wrong URL                 |
| 500  | Server Error | Server crashed            |

---

## REST Conventions
GET    /posts      → list all posts
GET    /posts/1    → get one post (id=1)
POST   /posts      → create new post
PUT    /posts/1    → update post (id=1)
DELETE /posts/1    → delete post (id=1)

---

## Localhost + Ports
- localhost = 127.0.0.1 = your own computer
- Port 8000 = FastAPI default (Day 14!)
- Port 3000 = Node.js default
- Port 5432 = PostgreSQL default (already on your machine!)
- Port 80   = HTTP default
- Port 443  = HTTPS default