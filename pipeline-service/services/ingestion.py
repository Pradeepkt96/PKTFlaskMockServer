import requests
from sqlalchemy.dialects.postgresql import insert
from models.customer import Customer

MOCK_URL = "http://mock-server:5000/api/customers"

def ingest_all(db):
    page = 1
    limit = 10
    total_processed = 0

    while True:
        r = requests.get(MOCK_URL, params={"page": page, "limit": limit})
        r.raise_for_status()
        payload = r.json()

        data = payload["data"]
        if not data:
            break

        for record in data:
            stmt = insert(Customer).values(**record)
            stmt = stmt.on_conflict_do_update(
                index_elements=["customer_id"],
                set_={k: stmt.excluded[k] for k in record.keys()}
            )
            db.execute(stmt)

        total_processed += len(data)

        if total_processed >= payload["total"]:
            break

        page += 1

    db.commit()
    return total_processed
