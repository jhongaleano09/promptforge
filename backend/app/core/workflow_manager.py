import aiosqlite
from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver
from app.agents.graph import get_graph

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
        await self._saver.setup()
        
        self._graph = get_graph(checkpointer=self._saver)

    async def get_graph_runnable(self):
        if self._graph is None:
            await self.initialize()
        return self._graph
    
    async def close(self):
        if self.conn:
            await self.conn.close()

workflow_manager = WorkflowManager()
