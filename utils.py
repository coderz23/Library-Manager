from database import cursor, conn

def clean_up_requests():
    cursor.execute('''
        DELETE FROM rental_requests
        WHERE is_approved = 0
        AND book_id IN (SELECT id FROM books WHERE is_rented = 1)
    ''')
    conn.commit()
