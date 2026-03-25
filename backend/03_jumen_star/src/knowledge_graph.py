"""
巨门星（记忆层）- 知识图谱引擎
版本: v2.0
负责人: 韩巨亮 (121)
功能: 实体关系管理、图算法、推理系统
"""

from typing import Dict, List, Optional, Any, Tuple, Set
from dataclasses import dataclass, field
from datetime import datetime
import asyncio
from enum import Enum

class EntityType(Enum):
    """实体类型"""
    PERSON = "person"
    ORGANIZATION = "organization"
    LOCATION = "location"
    PRODUCT = "product"
    EVENT = "event"
    CONCEPT = "concept"

class RelationType(Enum):
    """关系类型"""
    IS_A = "is_a"             # 是一种
    HAS_A = "has_a"           # 有一个
    PART_OF = "part_of"       # 部分
    RELATED_TO = "related_to" # 相关
    CAUSED_BY = "caused_by"   # 由...引起
    DEPENDS_ON = "depends_on" # 依赖

@dataclass
class Entity:
    """实体"""
    entity_id: str
    name: str
    entity_type: EntityType
    properties: Dict[str, Any] = field(default_factory=dict)
    embeddings: List[float] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)

@dataclass
class Relation:
    """关系"""
    relation_id: str
    source_id: str
    target_id: str
    relation_type: RelationType
    properties: Dict[str, Any] = field(default_factory=dict)
    weight: float = 1.0

class GraphDatabase:
    """图数据库"""
    
    def __init__(self):
        self.entities: Dict[str, Entity] = {}
        self.relations: Dict[str, Relation] = {}
        self.adjacency: Dict[str, Set[str]] = {}  # 邻接表
    
    async def add_entity(self, entity: Entity) -> str:
        """添加实体"""
        self.entities[entity.entity_id] = entity
        if entity.entity_id not in self.adjacency:
            self.adjacency[entity.entity_id] = set()
        return entity.entity_id
    
    async def add_relation(self, relation: Relation) -> str:
        """添加关系"""
        self.relations[relation.relation_id] = relation
        
        # 更新邻接表
        if relation.source_id not in self.adjacency:
            self.adjacency[relation.source_id] = set()
        self.adjacency[relation.source_id].add(relation.target_id)
        
        return relation.relation_id
    
    async def get_entity(self, entity_id: str) -> Optional[Entity]:
        """获取实体"""
        return self.entities.get(entity_id)
    
    async def get_neighbors(
        self,
        entity_id: str,
        relation_type: Optional[RelationType] = None
    ) -> List[Entity]:
        """获取邻居"""
        neighbor_ids = self.adjacency.get(entity_id, set())
        neighbors = []
        
        for nid in neighbor_ids:
            entity = self.entities.get(nid)
            if entity:
                if relation_type:
                    # 检查关系类型
                    for rel in self.relations.values():
                        if rel.source_id == entity_id and rel.target_id == nid:
                            if rel.relation_type == relation_type:
                                neighbors.append(entity)
                                break
                else:
                    neighbors.append(entity)
        
        return neighbors

class GraphAlgorithm:
    """图算法"""
    
    @staticmethod
    async def bfs(
        graph: GraphDatabase,
        start_id: str,
        max_depth: int = 3
    ) -> List[Entity]:
        """广度优先搜索"""
        visited = {start_id}
        queue = [(start_id, 0)]
        results = []
        
        while queue:
            current_id, depth = queue.pop(0)
            
            if depth >= max_depth:
                continue
            
            entity = graph.entities.get(current_id)
            if entity and current_id != start_id:
                results.append(entity)
            
            for neighbor_id in graph.adjacency.get(current_id, []):
                if neighbor_id not in visited:
                    visited.add(neighbor_id)
                    queue.append((neighbor_id, depth + 1))
        
        return results
    
    @staticmethod
    async def dijkstra(
        graph: GraphDatabase,
        start_id: str,
        end_id: str
    ) -> Optional[Tuple[List[str], float]]:
        """Dijkstra最短路径"""
        import heapq
        
        distances = {start_id: 0}
        previous = {start_id: None}
        queue = [(0, start_id)]
        visited = set()
        
        while queue:
            current_dist, current_id = heapq.heappop(queue)
            
            if current_id in visited:
                continue
            visited.add(current_id)
            
            if current_id == end_id:
                break
            
            for neighbor_id in graph.adjacency.get(current_id, []):
                # 获取关系权重
                weight = 1.0
                for rel in graph.relations.values():
                    if rel.source_id == current_id and rel.target_id == neighbor_id:
                        weight = rel.weight
                        break
                
                distance = current_dist + weight
                if distance < distances.get(neighbor_id, float('inf')):
                    distances[neighbor_id] = distance
                    previous[neighbor_id] = current_id
                    heapq.heappush(queue, (distance, neighbor_id))
        
        # 重建路径
        if end_id not in previous:
            return None
        
        path = []
        current = end_id
        while current:
            path.append(current)
            current = previous[current]
        
        path.reverse()
        return path, distances.get(end_id, float('inf'))

class ReasoningEngine:
    """推理引擎"""
    
    def __init__(self):
        self.graph = GraphDatabase()
        self.rules = []
    
    async def add_rule(self, premise: str, conclusion: str):
        """添加推理规则"""
        self.rules.append({"premise": premise, "conclusion": conclusion})
    
    async def reason(
        self,
        query: str,
        context: Optional[Dict] = None
    ) -> List[str]:
        """推理"""
        # TODO: 实现推理算法
        # 1. 匹配规则
        # 2. 演绎推理
        # 3. 返回结论
        return []

class KnowledgeGraphEngine:
    """知识图谱引擎"""
    
    def __init__(self):
        self.graph = GraphDatabase()
        self.algorithm = GraphAlgorithm()
        self.reasoning = ReasoningEngine()
    
    async def create_entity(
        self,
        name: str,
        entity_type: EntityType,
        properties: Optional[Dict] = None
    ) -> Entity:
        """创建实体"""
        import uuid
        entity = Entity(
            entity_id=f"ent_{uuid.uuid4().hex[:8]}",
            name=name,
            entity_type=entity_type,
            properties=properties or {}
        )
        await self.graph.add_entity(entity)
        return entity
    
    async def create_relation(
        self,
        source_id: str,
        target_id: str,
        relation_type: RelationType,
        weight: float = 1.0
    ) -> Relation:
        """创建关系"""
        import uuid
        relation = Relation(
            relation_id=f"rel_{uuid.uuid4().hex[:8]}",
            source_id=source_id,
            target_id=target_id,
            relation_type=relation_type,
            weight=weight
        )
        await self.graph.add_relation(relation)
        return relation
    
    async def query_path(
        self,
        start_entity: str,
        end_entity: str
    ) -> Optional[Tuple[List[str], float]]:
        """查询路径"""
        return await self.algorithm.dijkstra(self.graph, start_entity, end_entity)
    
    async def get_insights(
        self,
        entity_id: str
    ) -> Dict[str, Any]:
        """获取洞察"""
        neighbors = await self.graph.get_neighbors(entity_id)
        
        return {
            "entity_id": entity_id,
            "neighbor_count": len(neighbors),
            "neighbors": [n.name for n in neighbors]
        }

# 导出
__all__ = ["EntityType", "RelationType", "Entity", "Relation", "GraphDatabase", "GraphAlgorithm", "ReasoningEngine", "KnowledgeGraphEngine"]
