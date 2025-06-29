# Windows-specific Neo4j configuration helper
import os
import sys
import logging
import re
import shutil

def setup_logging():
    log_format = "[INFO] %(message)s"
    logging.basicConfig(level=logging.INFO, format=log_format)
    logger = logging.getLogger()
    return logger

logger = setup_logging()

# Only run this on Windows
if sys.platform == 'win32' and getattr(sys, 'frozen', False):
    logger.info("Initializing Windows-specific Neo4j configuration helper")
    
    # Get the application path
    APP_PATH = os.path.normpath(os.path.dirname(sys.executable))
    NEO4J_PATH = os.path.normpath(os.path.join(APP_PATH, 'Neo4jDB'))
    
    # Function to fix Neo4j configuration paths
    def fix_config_paths():
        # Define the Neo4j configuration file paths
        neo4j_server_dir = os.path.join(NEO4J_PATH, 'neo4j-server')
        neo4j_conf_dir = os.path.join(neo4j_server_dir, 'conf')
        neo4j_conf_file = os.path.join(neo4j_conf_dir, 'neo4j.conf')
        
        # Create directories if they don't exist
        os.makedirs(neo4j_conf_dir, exist_ok=True)
        logger.info(f"Created Neo4j config directory: {neo4j_conf_dir}")
        
        # Create configuration with relative paths
        config_content = """# Neo4j configuration - auto-generated for Windows
# Using relative paths for better portability

# Database directory configuration
dbms.directories.data=../data
dbms.directories.plugins=../plugins
dbms.directories.logs=../logs
dbms.directories.import=../import
dbms.directories.lib=../lib
dbms.directories.run=../run
dbms.directories.metrics=../metrics
dbms.directories.transaction.logs.root=../data/transactions

# Default database settings
dbms.default_database=neo4j

# Memory settings
dbms.memory.heap.initial_size=512m
dbms.memory.heap.max_size=1g
dbms.memory.pagecache.size=512m

# Network connector configuration
dbms.connector.bolt.enabled=true
dbms.connector.bolt.listen_address=localhost:7687
dbms.connector.http.enabled=true
dbms.connector.http.listen_address=localhost:7474
dbms.connector.https.enabled=false

# Security configuration
dbms.security.auth_enabled=false
dbms.security.allow_csv_import_from_file_urls=true
dbms.security.procedures.unrestricted=apoc.*
dbms.security.procedures.allowlist=apoc.*
dbms.security.procedures.whitelist=apoc.*

# Authentication settings
dbms.security.auth_enabled=false
dbms.security.authentication_providers=native
dbms.security.authorization_providers=native

# Performance settings
dbms.tx_state.memory_allocation=ON_HEAP
dbms.memory.pagecache.flush.buffer.enabled=true
dbms.memory.pagecache.flush.buffer.size_in_pages=100
dbms.transaction.concurrent.maximum=16
dbms.memory.transaction.global_max_size=512m
dbms.transaction.timeout=600s
dbms.connector.bolt.thread_pool_min_size=10
dbms.connector.bolt.thread_pool_max_size=40
"""
        
        try:
            # Write the configuration file
            with open(neo4j_conf_file, 'w') as f:
                f.write(config_content)
            logger.info(f"Created Neo4j configuration at {neo4j_conf_file}")
            
            # Also create necessary directories
            os.makedirs(os.path.join(NEO4J_PATH, 'data'), exist_ok=True)
            os.makedirs(os.path.join(NEO4J_PATH, 'plugins'), exist_ok=True)
            os.makedirs(os.path.join(NEO4J_PATH, 'logs'), exist_ok=True)
            os.makedirs(os.path.join(NEO4J_PATH, 'import'), exist_ok=True)
            os.makedirs(os.path.join(NEO4J_PATH, 'lib'), exist_ok=True)
            os.makedirs(os.path.join(NEO4J_PATH, 'run'), exist_ok=True)
            os.makedirs(os.path.join(NEO4J_PATH, 'metrics'), exist_ok=True)
            os.makedirs(os.path.join(NEO4J_PATH, 'data', 'transactions'), exist_ok=True)
            
            logger.info("Created all required Neo4j directories")
            
        except Exception as e:
            logger.info(f"Error fixing Neo4j configuration: {e}")
    
    # Register the function to be called when Neo4j is first configured
    fix_config_paths()
