import pytest
import sqlite3
from pathlib import Path
from llm_platform.utils.database import Database

@pytest.fixture
def db_path(test_data_dir):
    """Create a test database path."""
    return test_data_dir / 'test.db'

@pytest.fixture
def db(db_path):
    """Create a test database."""
    database = Database(db_path)
    database.init_db()
    yield database
    database.close()
    if db_path.exists():
        db_path.unlink()

def test_init_db(db):
    """Test database initialization."""
    # Check if tables exist
    tables = db.execute('SELECT name FROM sqlite_master WHERE type="table"').fetchall()
    table_names = [table[0] for table in tables]
    
    assert 'documents' in table_names
    assert 'collections' in table_names
    assert 'tasks' in table_names
    assert 'workers' in table_names

def test_document_operations(db):
    """Test document database operations."""
    # Test document insertion
    doc_id = db.insert_document({
        'name': 'test.txt',
        'path': 'data/test.txt',
        'size': 1000,
        'type': 'text/plain',
        'collection_id': None
    })
    assert doc_id is not None
    
    # Test document retrieval
    doc = db.get_document(doc_id)
    assert doc['name'] == 'test.txt'
    assert doc['path'] == 'data/test.txt'
    assert doc['size'] == 1000
    assert doc['type'] == 'text/plain'
    
    # Test document update
    db.update_document(doc_id, {'size': 2000})
    doc = db.get_document(doc_id)
    assert doc['size'] == 2000
    
    # Test document deletion
    db.delete_document(doc_id)
    doc = db.get_document(doc_id)
    assert doc is None

def test_collection_operations(db):
    """Test collection database operations."""
    # Test collection insertion
    coll_id = db.insert_collection({
        'name': 'test_collection',
        'description': 'Test collection'
    })
    assert coll_id is not None
    
    # Test collection retrieval
    coll = db.get_collection(coll_id)
    assert coll['name'] == 'test_collection'
    assert coll['description'] == 'Test collection'
    
    # Test collection update
    db.update_collection(coll_id, {'description': 'Updated description'})
    coll = db.get_collection(coll_id)
    assert coll['description'] == 'Updated description'
    
    # Test collection deletion
    db.delete_collection(coll_id)
    coll = db.get_collection(coll_id)
    assert coll is None

def test_task_operations(db):
    """Test task database operations."""
    # Test task insertion
    task_id = db.insert_task({
        'type': 'chat',
        'status': 'pending',
        'parameters': {'messages': [{'role': 'user', 'content': 'Hello'}]},
        'result': None,
        'worker_id': None
    })
    assert task_id is not None
    
    # Test task retrieval
    task = db.get_task(task_id)
    assert task['type'] == 'chat'
    assert task['status'] == 'pending'
    assert task['parameters']['messages'][0]['content'] == 'Hello'
    
    # Test task update
    db.update_task(task_id, {
        'status': 'completed',
        'result': {'response': 'Hi there!'}
    })
    task = db.get_task(task_id)
    assert task['status'] == 'completed'
    assert task['result']['response'] == 'Hi there!'
    
    # Test task deletion
    db.delete_task(task_id)
    task = db.get_task(task_id)
    assert task is None

def test_worker_operations(db):
    """Test worker database operations."""
    # Test worker insertion
    worker_id = db.insert_worker({
        'name': 'test_worker',
        'status': 'idle',
        'capabilities': ['chat', 'embedding'],
        'last_heartbeat': None
    })
    assert worker_id is not None
    
    # Test worker retrieval
    worker = db.get_worker(worker_id)
    assert worker['name'] == 'test_worker'
    assert worker['status'] == 'idle'
    assert 'chat' in worker['capabilities']
    
    # Test worker update
    db.update_worker(worker_id, {
        'status': 'busy',
        'last_heartbeat': '2024-01-01 00:00:00'
    })
    worker = db.get_worker(worker_id)
    assert worker['status'] == 'busy'
    assert worker['last_heartbeat'] == '2024-01-01 00:00:00'
    
    # Test worker deletion
    db.delete_worker(worker_id)
    worker = db.get_worker(worker_id)
    assert worker is None

def test_transaction_rollback(db):
    """Test database transaction rollback."""
    # Start a transaction
    db.begin_transaction()
    
    try:
        # Insert a document
        doc_id = db.insert_document({
            'name': 'test.txt',
            'path': 'data/test.txt',
            'size': 1000,
            'type': 'text/plain'
        })
        
        # Force an error
        raise ValueError('Test error')
        
    except ValueError:
        # Rollback the transaction
        db.rollback()
    
    # Verify document was not inserted
    doc = db.get_document(doc_id)
    assert doc is None

def test_transaction_commit(db):
    """Test database transaction commit."""
    # Start a transaction
    db.begin_transaction()
    
    # Insert a document
    doc_id = db.insert_document({
        'name': 'test.txt',
        'path': 'data/test.txt',
        'size': 1000,
        'type': 'text/plain'
    })
    
    # Commit the transaction
    db.commit()
    
    # Verify document was inserted
    doc = db.get_document(doc_id)
    assert doc is not None
    assert doc['name'] == 'test.txt'

def test_connection_pooling(db):
    """Test database connection pooling."""
    # Create multiple connections
    conn1 = db.get_connection()
    conn2 = db.get_connection()
    
    # Verify connections are different
    assert conn1 is not conn2
    
    # Return connections to pool
    db.return_connection(conn1)
    db.return_connection(conn2)
    
    # Get connections again
    conn3 = db.get_connection()
    conn4 = db.get_connection()
    
    # Verify connections are reused
    assert conn3 is conn1 or conn3 is conn2
    assert conn4 is conn1 or conn4 is conn2 