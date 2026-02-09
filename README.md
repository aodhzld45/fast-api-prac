# 📌 Wishlist API 통합 테스트 케이스 (.md)

## 🧩 사전 준비 데이터

### 1) 사용자 생성

**POST** `/users`

```json
{
  "nickname": "tester1"
}
```

예상 응답:

```json
{
  "id": 1,
  "nickname": "tester1"
}
```

---

### 2) 카테고리 생성 (DB 직접 입력)

```sql
INSERT INTO categories (name) VALUES ('전자기기');
```

---

### 3) 상품 생성

**POST** `/products`

```json
{
  "name": "무선 이어폰",
  "price": 99000,
  "discount_price": 79000,
  "stock": 10,
  "category_id": 1
}
```

예상 응답:

```json
{
  "id": 1,
  "name": "무선 이어폰",
  "price": 99000,
  "discount_price": 79000,
  "stock": 10,
  "category_id": 1
}
```

---

# 1️⃣ 찜하기

## [POST] `/users/{user_id}/wishlist/{product_id}`

### 정상 케이스

```
POST /users/1/wishlist/1
```

응답:

```json
{
  "user_id": 1,
  "product_id": 1,
  "created_at": "2026-02-09T20:12:11"
}
```

---

### 중복 찜 시도

```
POST /users/1/wishlist/1
```

응답:

```json
{
  "detail": "이미 찜한 상품입니다. user_id=1, product_id=1"
}
```

---

### 존재하지 않는 유저

```
POST /users/999/wishlist/1
```

응답:

```json
{
  "detail": "유저가 없습니다. user_id=999"
}
```

---

### 존재하지 않는 상품

```
POST /users/1/wishlist/999
```

응답:

```json
{
  "detail": "상품이 없습니다. product_id=999"
}
```

---

# 2️⃣ 특정 유저의 위시리스트 조회

## [GET] `/users/{user_id}/wishlist`

```
GET /users/1/wishlist
```

응답:

```json
[
  {
    "created_at": "2026-02-09T20:12:11",
    "product": {
      "id": 1,
      "name": "무선 이어폰",
      "price": 99000,
      "discount_price": 79000,
      "stock": 10,
      "category_id": 1
    }
  }
]
```

---

### 존재하지 않는 유저 조회

```
GET /users/999/wishlist
```

응답:

```json
{
  "detail": "유저가 없습니다. user_id=999"
}
```

---

# 3️⃣ 찜 취소

## [DELETE] `/users/{user_id}/wishlist/{product_id}`

### 정상 삭제

```
DELETE /users/1/wishlist/1
```

응답:

```
204 No Content
```

---

### 삭제 후 다시 조회

```
GET /users/1/wishlist
```

응답:

```json
[]
```

---

### 존재하지 않는 찜 삭제

```
DELETE /users/1/wishlist/1
```

응답:

```json
{
  "detail": "찜 내역이 없습니다. user_id=1, product_id=1"
}
```

---

# 🔥 전체 통합 테스트 시나리오

1. 사용자 생성
2. 카테고리 생성
3. 상품 생성
4. 찜하기
5. 찜 목록 조회
6. 찜 취소
7. 다시 조회 → 빈 리스트 확인

---

# 💡 검증 포인트 체크리스트

* 같은 상품은 1번만 찜 가능해야 함
* 삭제 후 다시 찜 가능해야 함
* `created_at` 자동 생성 확인
* FK 제약 정상 동작 확인
* 존재하지 않는 user/product 예외 처리 확인

---

# 🧪 추천 테스트 순서 (Postman)

1. `POST /users`
2. `POST /products`
3. `POST /users/1/wishlist/1`
4. `GET /users/1/wishlist`
5. `DELETE /users/1/wishlist/1`
6. `GET /users/1/wishlist`
