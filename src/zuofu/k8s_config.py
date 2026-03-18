"""
左辅星 - K8s配置模块
系统底座、容器编排、多租户
"""

import yaml
from typing import Dict, List, Optional
from pydantic import BaseModel, Field


class ContainerConfig(BaseModel):
    """容器配置"""
    name: str
    image: str
    ports: List[int] = Field(default_factory=list)
    env: Dict[str, str] = Field(default_factory=dict)
    resources: Dict[str, str] = Field(default_factory=dict)


class DeploymentConfig(BaseModel):
    """部署配置"""
    name: str
    replicas: int = Field(default=1)
    containers: List[ContainerConfig]
    service_type: str = Field(default="ClusterIP")


class K8sManifestGenerator:
    """K8s清单生成器"""
    
    def __init__(self, namespace: str = "xuanji"):
        self.namespace = namespace
    
    def generate_deployment(self, config: DeploymentConfig) -> dict:
        """生成Deployment YAML"""
        containers = []
        for c in config.containers:
            container = {
                "name": c.name,
                "image": c.image,
                "ports": [{"containerPort": p} for p in c.ports],
                "env": [{"name": k, "value": v} for k, v in c.env.items()]
            }
            if c.resources:
                container["resources"] = c.resources
            containers.append(container)
        
        return {
            "apiVersion": "apps/v1",
            "kind": "Deployment",
            "metadata": {
                "name": config.name,
                "namespace": self.namespace
            },
            "spec": {
                "replicas": config.replicas,
                "selector": {
                    "matchLabels": {"app": config.name}
                },
                "template": {
                    "metadata": {
                        "labels": {"app": config.name}
                    },
                    "spec": {"containers": containers}
                }
            }
        }
    
    def generate_service(self, name: str, service_type: str = "ClusterIP") -> dict:
        """生成Service YAML"""
        return {
            "apiVersion": "v1",
            "kind": "Service",
            "metadata": {
                "name": f"{name}-service",
                "namespace": self.namespace
            },
            "spec": {
                "selector": {"app": name},
                "ports": [{"port": 80, "targetPort": 80}],
                "type": service_type
            }
        }
    
    def generate_ingress(self, name: str, host: str) -> dict:
        """生成Ingress YAML"""
        return {
            "apiVersion": "networking.k8s.io/v1",
            "kind": "Ingress",
            "metadata": {
                "name": f"{name}-ingress",
                "namespace": self.namespace
            },
            "spec": {
                "rules": [{
                    "host": host,
                    "http": {
                        "paths": [{
                            "path": "/",
                            "pathType": "Prefix",
                            "backend": {
                                "service": {
                                    "name": f"{name}-service",
                                    "port": {"number": 80}
                                }
                            }
                        }]
                    }
                }]
            }
        }
    
    def generate_configmap(self, name: str, data: Dict[str, str]) -> dict:
        """生成ConfigMap"""
        return {
            "apiVersion": "v1",
            "kind": "ConfigMap",
            "metadata": {
                "name": name,
                "namespace": self.namespace
            },
            "data": data
        }


class MultiTenantManager:
    """多租户管理器"""
    
    def __init__(self):
        self.tenants: Dict[str, dict] = {}
    
    def create_tenant(self, tenant_id: str, name: str, quota: dict = None) -> dict:
        """创建租户"""
        tenant = {
            "id": tenant_id,
            "name": name,
            "quota": quota or {
                "cpu": "2",
                "memory": "4Gi",
                "storage": "10Gi"
            },
            "namespaces": []
        }
        self.tenants[tenant_id] = tenant
        return tenant
    
    def create_namespace(self, tenant_id: str, namespace: str) -> bool:
        """为租户创建命名空间"""
        if tenant_id not in self.tenants:
            return False
        self.tenants[tenant_id]["namespaces"].append(namespace)
        return True
    
    def get_tenant(self, tenant_id: str) -> Optional[dict]:
        """获取租户信息"""
        return self.tenants.get(tenant_id)


# 测试代码
if __name__ == "__main__":
    gen = K8sManifestGenerator()
    
    # 生成Deployment
    deployment = DeploymentConfig(
        name="xuanji-engine",
        replicas=3,
        containers=[
            ContainerConfig(
                name="api",
                image="xuanji/api:latest",
                ports=[8000],
                env={"ENV": "production"}
            )
        ]
    )
    
    manifest = gen.generate_deployment(deployment)
    print(yaml.dump(manifest, default_flow_style=False))
