import aiosqlite
import logging
from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver
from app.agents.graph import get_graph

logger = logging.getLogger(__name__)

# Monkey-patch AsyncSqliteSaver.setup() to handle AttributeError with aiosqlite 0.22.1
original_setup = AsyncSqliteSaver.setup

async def patched_setup(self):
    """Patched setup method that handles AttributeError for older aiosqlite versions."""
    async with self.lock:
        if self.is_setup:
            return
        # Skip the is_alive() check for aiosqlite 0.22.1 which doesn't have this method
        # Instead, try to execute a simple query to check if connection is alive
        try:
            if hasattr(self.conn, 'is_alive') and not self.conn.is_alive():
                await self.conn
        except AttributeError:
            # aiosqlite 0.22.1 doesn't have is_alive(), assume connection is alive
            pass

        async with self.conn.executescript(
            """
            PRAGMA journal_mode=WAL;
            CREATE TABLE IF NOT EXISTS checkpoints (
                thread_id TEXT NOT NULL,
                checkpoint_ns TEXT NOT NULL DEFAULT '',
                checkpoint_id TEXT NOT NULL,
                parent_checkpoint_id TEXT,
                type TEXT,
                checkpoint BLOB,
                metadata BLOB,
                PRIMARY KEY (thread_id, checkpoint_ns, checkpoint_id)
            );
            CREATE TABLE IF NOT EXISTS writes (
                thread_id TEXT NOT NULL,
                checkpoint_ns TEXT NOT NULL DEFAULT '',
                checkpoint_id TEXT NOT NULL,
                idx INTEGER NOT NULL,
                task_id TEXT NOT NULL,
                channel TEXT NOT NULL,
                type TEXT,
                value BLOB,
                PRIMARY KEY (thread_id, checkpoint_ns, checkpoint_id, idx, task_id)
            );
            CREATE TABLE IF NOT EXISTS blobs (
                thread_id TEXT NOT NULL,
                checkpoint_ns TEXT NOT NULL DEFAULT '',
                checkpoint_id TEXT NOT NULL,
                task_id TEXT NOT NULL,
                channel TEXT NOT NULL,
                idx INTEGER NOT NULL,
                BLOB BLOB,
                PRIMARY KEY (thread_id, checkpoint_ns, checkpoint_id, task_id, channel, idx)
            );
            CREATE TABLE IF NOT EXISTS blobs_multipart (
                thread_id TEXT NOT NULL,
                checkpoint_ns TEXT NOT NULL DEFAULT '',
                checkpoint_id TEXT NOT NULL,
                task_id TEXT NOT NULL,
                channel TEXT NOT NULL,
                idx INTEGER NOT NULL,
                chunk_idx INTEGER NOT NULL,
                BLOB BLOB,
                PRIMARY KEY (thread_id, checkpoint_ns, checkpoint_id, task_id, channel, idx, chunk_idx)
            );
            """
        ) as cursor:
            pass
        self.is_setup = True

# Apply the monkey-patch
AsyncSqliteSaver.setup = patched_setup

class WorkflowManager:
    _instance = None
    _graph = None
    _saver = None

    @classmethod
    async def get_instance(cls):
        if cls._instance is None:
            cls._instance = WorkflowManager()
            await cls._instance.initialize()
        return cls._instance

    async def initialize(self):
        # Initialize persistence
        self.conn = await aiosqlite.connect("workflow_state.sqlite")
        self._saver = AsyncSqliteSaver(self.conn)
        # Note: In newer LangGraph versions setup is often automatic or handled by the saver
        # But AsyncSqliteSaver usually needs explicit setup for tables if they don't exist
        # Handle AttributeError for older aiosqlite versions that don't have is_alive()
        try:
            await self._saver.setup()
        except AttributeError:
            # Older versions of aiosqlite don't have is_alive() method
            # This is expected with aiosqlite 0.22.1
            logger.warning("AsyncSqliteSaver.setup() raised AttributeError, skipping (aiosqlite 0.22.1)")
            pass

        self._graph = get_graph(checkpointer=self._saver)

    async def get_graph_runnable(self):
        if self._graph is None:
            await self.initialize()
        return self._graph
    
    async def close(self):
        if hasattr(self, 'conn') and self.conn:
            await self.conn.close()

workflow_manager = WorkflowManager()
